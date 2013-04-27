#!/usr/bin/env python

import socket

UDPHOST="localhost"
UDPPORT=6001

# Color system
def _filter_data_normalize(value):
    try:
        value = int(value)
    except exceptions.ValueError:
        return 0

    if value < 0:
        return 0
    elif value > 255:
        return 255
    else:
        return value

def get_filter_data(argv):
    return (_filter_data_normalize(argv[0]), _filter_data_normalize(argv[1]), _filter_data_normalize(argv[2]))

def colorfilter(r, g, b, filter_data):
    r_out = (r/255.0) * filter_data[0]
    g_out = (g/255.0) * filter_data[1]
    b_out = (b/255.0) * filter_data[2]

    return (r_out, g_out, b_out)

# Sound system
sock = None

def init_beat(port = UDPPORT):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDPHOST,port))

def wait_beat():
    global sock
    sock.recv(1)

def send_beat(port = UDPPORT):
    global sock
    sock.sendto("1", (UDPHOST, port))
