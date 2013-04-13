#!/usr/bin/env python

import threading
import subprocess
import time

class Scheduler:
    def __init__(self):
        # Queue for animations
        self.queue = [] # First element: plays/next to play
        self.queue_lock = threading.Lock()

        self.stop = threading.Event()

        self.thread = threading.Thread(target=self.scheduler_process)

        self.process = None

    def Insert(self, animation):
        with self.queue_lock:
            self.queue.insert(len(self.queue), animation)

    def InsertFirst(self, animation):
        with self.queue_lock:
            self.queue.insert(0, animation)

    def Current(self):
        with self.queue_lock:
            if len(self.queue) > 0:
                return self.queue[0]
            else:
                return None

    def RemoveCurrent(self):
        with self.queue_lock:
            if len(self.queue) > 0:
                return self.queue.pop(0)
            else:
                return None
    def Start(self):
        self.thread.start()

    def Stop(self):
        if self.process != None:
            print "Kill process " + str(self.process.pid)
            self.process.kill()

        self.stop.set()
        self.thread.join()

    def IsEmpty(self):
        with self.queue_lock:
            return len(self.queue) == 0

    def scheduler_process(self):
        while not self.stop.is_set():
            if not self.IsEmpty():
                animation = self.Current()
                self.process=subprocess.Popen(["python", animation.GetFile()])

                print "[" + str(self.process.pid) + "] " + animation.GetFile()
                time.sleep(animation.GetTime())

                print "Kill process " + str(self.process.pid)
                self.process.kill()
                self.RemoveCurrent()
            else:
                pass # TODO: random
