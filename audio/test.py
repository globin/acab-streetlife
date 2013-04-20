#!/usr/bin/env python

import pyaudio
import numpy
import struct
import time

# Setup
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

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

# Main
def read():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    last_beat = 0

    print("Start recording...")

    try:
        while True:
            data = stream.read(CHUNK)

            levels = calculate_levels(data)

            #for level in levels:
            #    print str(level) + ",",
            #print

            current_beat = time.time()

            if levels[0] > 120 and current_beat - last_beat > 0.5:
                print "BUMM"
                last_beat = current_beat
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    read()
