#!/usr/bin/env python

import pyaudio
import numpy
import struct
import time
from acabx import *

DEBUG = True

BEAT_PORT=6002

# Setup
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

THRESHOLD = 120
MIN_OFFSET = 0.5

NOOF_BPM_VALUES = 5

# FFT
def calculate_levels(data):
    # Convert raw sound data to Numpy array
    fmt = "%dH"%(len(data)/2)
    data2 = struct.unpack(fmt, data)
    data2 = numpy.array(data2, dtype='h')

    # Apply FFT
    fourier = numpy.fft.fft(data2)
    ffty = numpy.abs(fourier[0:len(fourier)/2])/1000
    ffty1=ffty[:len(ffty)/2]
    ffty2=ffty[len(ffty)/2::]+2
    ffty2=ffty2[::-1]
    ffty=ffty1+ffty2
    ffty=numpy.log(ffty)-2
    fourier = list(ffty)[4:-4]
    fourier = fourier[:len(fourier)/2]
    size = len(fourier)

    # Add up for 6 lights
    levels = [sum(fourier[i:(i+size/6)]) for i in xrange(0, size, size/6)][:6]
    return levels

def add_offset(offset_list, new_value):
    if len(offset_list) > 0 and len(offset_list) > NOOF_BPM_VALUES:
        offset_list.pop(0)

    offset_list.append(new_value)

def calc_bpm(offset_list):
    avg = sum(offset_list) / float(len(offset_list))

    return 60.0/avg

# Main
def read():
    beat_data = init_beat_server(BEAT_PORT)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Interesting values :)
    last_beat = 0
    offset_list = []
    bpm = 0

    if DEBUG:
        print("Start recording...")

    try:
        while True:
            data = stream.read(CHUNK)

            levels = calculate_levels(data)

            current_beat = time.time()

            if levels[0] > THRESHOLD and current_beat - last_beat > MIN_OFFSET:
                if last_beat != 0:
                    add_offset(offset_list, current_beat - last_beat)
                    bpm = calc_bpm(offset_list)

                last_beat = current_beat

                if DEBUG:
                    print(bpm)

                send_beat(beat_data)

    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    read()
