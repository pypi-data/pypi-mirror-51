# -*- coding: utf-8 -*-
"""workerpool"""

__author__  = "Adrien DELLE CAVE <adc@doowan.net>"
__license__ = """
    Copyright (C) 2015  doowan

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""


import gc
import logging
import Queue
import threading
import time


LOG = logging.getLogger('sonicprobe.workerpool')


class WorkerExit(object):
    pass


class WorkerThread(threading.Thread):
    def __init__(self, xid, pool):
        threading.Thread.__init__(self, verbose = pool.verbose)
        self.daemon     = True
        self.pool       = pool
        self.life_time  = None
        self.nb_tasks   = None
        self.xid        = xid

    def start(self):
        self.nb_tasks   = 0
        self.life_time  = time.time()
        return threading.Thread.start(self)

    def expired(self):
        if self.pool.life_time > 0 \
           and self.life_time > 0 \
           and (time.time() - self.life_time) >= self.pool.life_time:
            LOG.debug("worker expired")
            return True

        return False

    def max_tasks_reached(self):
        if self.pool.max_tasks > 0 \
           and self.nb_tasks > 0 \
           and self.nb_tasks >= self.pool.max_tasks:
            LOG.debug("worker max tasks reached")
            return True

        return False

    def run(self):
        name = None

        while True:
            if self.expired() or self.max_tasks_reached():
                if self.pool.auto_gc:
                    gc.collect()
                break

            if self.pool.tasks.empty():
                continue

            try:
                task = self.pool.tasks.get_nowait()
            except Queue.Empty:
                continue

            if isinstance(task, WorkerExit):
                break

            self.pool.count_lock.acquire()
            self.pool.working += 1
            if (not self.pool.tasks.empty() or self.pool.working >= self.pool.workers) \
               and (self.pool.workers < self.pool.max_workers):
                self.pool.count_lock.release()
                self.pool.add()
            else:
                self.pool.count_lock.release()

            func, cb, name, complete, args, kargs = task
            self.setName(self.pool.get_name(self.xid, name))

            if __debug__:
                self._note("%s.run(): starting function: %r", self, func)

            ret = None

            try:
                self.nb_tasks += 1
                ret = func(*args, **kargs)
                if cb:
                    if __debug__:
                        self._note("%s.run(): starting callback: %r", self, cb)
                    cb(ret)
            except Exception, e:
                LOG.exception("unexpected error: %r", e)
            finally:
                if complete:
                    if __debug__:
                        self._note("%s.run(): starting complete callback: %r", self, complete)
                    complete(ret)
                del func, args, kargs

            self.pool.tasks.task_done()
            self.pool.count_lock.acquire()
            self.pool.working -= 1
            self.pool.count_lock.release()

        self.pool.count_lock.acquire()
        self.pool.workers -= 1
        if not self.pool.workers:
            self.pool.kill_event.set()

        if (not self.pool.tasks.empty() \
            or (self.pool.workers > 0 and self.pool.working >= self.pool.workers)) \
           and (self.pool.workers < self.pool.max_workers):
            self.pool.count_lock.release()
            self.pool.add(name = name, xid = self.xid)
        else:
            self.pool.count_lock.release()


class WorkerPool(object):
    def __init__(self, queue = None, max_workers = 10, life_time = None, name = None, max_tasks = None, auto_gc = True, verbose = None):
        self.tasks          = queue or Queue.Queue()
        self.workers        = 0
        self.working        = 0
        self.max_workers    = max_workers
        self.life_time      = life_time
        self.name           = name
        self.max_tasks      = max_tasks
        self.auto_gc        = auto_gc
        self.verbose        = verbose

        self.kill_event     = threading.Event()
        self.count_lock     = threading.RLock()

        self.kill_event.set()

    def count_workers(self):
        self.count_lock.acquire()
        r = self.workers
        self.count_lock.release()
        return r

    def count_working(self):
        self.count_lock.acquire()
        r = self.working
        self.count_lock.release()
        return r

    def kill(self, nb = 1):
        """
        Kill one or many workers.
        """
        self.count_lock.acquire()
        if nb > self.workers:
            nb = self.workers
        self.count_lock.release()
        for x in xrange(nb):
            self.tasks.put(WorkerExit())

    def set_max_workers(self, nb):
        """
        Set the maximum workers to create.
        """
        self.count_lock.acquire()
        self.max_workers = nb
        if self.workers > self.max_workers:
            self.kill(self.workers - self.max_workers)
        self.count_lock.release()

    def get_max_workers(self):
        return self.max_workers

    def get_name(self, xid, name = None):
        if name:
            return "%s:%d" % (name, xid)
        elif self.name:
            return "%s:%d" % (self.name, xid)
        else:
            return "wpool:%d" % xid

    def add(self, nb = 1, name = None, xid = None):
        """
        Create one or many workers.
        """
        for x in xrange(nb):
            self.count_lock.acquire()
            if self.workers >= self.max_workers:
                self.count_lock.release()
                continue
            self.workers += 1
            if xid is None:
                xid = self.workers
            self.count_lock.release()
            self.kill_event.clear()
            w = WorkerThread(xid, self)
            w.setName(self.get_name(xid, name))
            w.start()

    def run(self, target, callback = None, name = None, complete = None, *args, **kargs):
        """
        Start task.
        @target: callable to run with *args and **kargs arguments.
        @callback: callable executed after target.
        @name: thread name
        @complete: complete executed after target in finally
        """
        self.count_lock.acquire()
        if not self.workers:
            self.count_lock.release()
            self.add(name = name)
        else:
            self.count_lock.release()
        self.tasks.put((target, callback, name, complete, args, kargs))

    def killall(self, wait = None):
        """
        Kill all active workers.
        @wait: Seconds to wait until last worker ends.
               If None it waits forever.
        """
        with self.tasks.mutex:
            self.tasks.queue.clear()
        self.count_lock.acquire()
        self.kill(self.workers)
        self.count_lock.release()
        self.kill_event.wait(wait)
