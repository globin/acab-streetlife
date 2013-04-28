#!/usr/bin/env python

from acabx import *
from time import *

SECONDS=0.5

beat_data = init_beat_server(6002)

while True:
    try:
        send_beat(beat_data)
    except socket.error as e:
        if e.errno != errno.EINTR: # Interrupted system call
            print e
        sys.exit()

    sleep(SECONDS)
