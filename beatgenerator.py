#!/usr/bin/env python

from acabx import *
from time import *

SERVER_PORT=6002
SECONDS=0.5

init_beat(SERVER_PORT)

while True:
    try:
        send_beat()
    except socket.error as e:
        if e.errno != errno.EINTR: # Interrupted system call
            print e
        sys.exit()

    sleep(SECONDS)
