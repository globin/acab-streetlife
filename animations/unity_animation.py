#!/usr/bin/env python

import Image
import time
import os
import sys
from acabsl import *
from acabx import *

img_file_fallback = "dance/list"
img_file = img_file_fallback
filter_data = (255, 255, 255)
fade_time = 0

# config
if len(sys.argv) == 6:
    img_file = sys.argv[1]

    filter_data = get_filter_data(sys.argv[2:5])
    fade_time = float(sys.argv[5])

img_file = os.path.join(os.path.dirname(__file__), img_file)

if not os.path.isfile(img_file):
    img_file = os.path.join(os.path.dirname(__file__), img_file_fallback)

img_dir = os.path.dirname(img_file)

# setup
beat_data = init_beat_client(6001)

img = {}
frames = []
with open(img_file) as f:
    for line in f:
        line = line.strip()
        frames.append(line)
        if line not in img:
            img[line] = Image.open(os.path.join(img_dir, line)).getdata()

#for wall in range(NOOFWALLS):
#    for col in range(WALLSIZEX):
#        for row in range(WALLSIZEY):
#            send(wall,col,row,0,0,0,0)
#update()


def render_frame(data):
    img_x = int(data.size[0])
    img_y = int(data.size[1])

    size_x = min(WALLSIZEX, img_x)
    size_y = min(WALLSIZEY, img_y)

    for wall in range(NOOFWALLS):
        for y in range(size_y):
            for x in range(size_x):
                ptr = x + y * img_x
                if type(data[ptr]) == int:
                    colors = colorfilter(data[ptr],data[ptr],data[ptr], filter_data)
                    send(wall,x,y,colors[0],colors[1],colors[2],fade_time);
                else:
                    colors = colorfilter(data[ptr][0],data[ptr][1],data[ptr][2], filter_data)
                    send(wall,x,y,colors[0],colors[1],colors[2],fade_time);
    update()


while True:
    for f in frames:
        wait_beat(beat_data)
        render_frame(img[f])
        #time.sleep(0.42)
