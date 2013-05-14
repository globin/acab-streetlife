#!/usr/bin/env python

import socket
import exceptions

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
dest = None

# Init port
def init_beat_client(port, timeout = None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0",port))

    if timeout != None:
        sock.settimeout(timeout)

    return (sock, None, None)

# Init port
def init_beat_server(host, port, timeout = None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if timeout != None:
        sock.settimeout(timeout)

    return (sock, host, port)

# Wait for beat
def wait_beat(data):
    try:
        data[0].recv(1)
    except socket.timeout:
        return False

    return True

# Send beat to port
def send_beat(data):
    data[0].sendto("1", (data[1], data[2]))
