#!/usr/bin/env python

import threading
from acabx import *

class BeatThread(threading.Thread):
    def __init__(self, control, beat_data, beat_lock):
        threading.Thread.__init__(self)

        self.control = control
        self.beat_data = beat_data
        self.beat_lock = beat_lock

        self._stop = threading.Event()

    def run(self):
        client_data = init_beat_client(6002, 2.0)

        while not self.stopped():
            if wait_beat(client_data):
                self.beat_lock.acquire()

                if self.control.GetLive():
                   send_beat(self.beat_data)

                self.beat_lock.release()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
