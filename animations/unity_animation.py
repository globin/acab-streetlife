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

# config
if len(sys.argv) == 5:
    img_file = sys.argv[1]

    filter_data = get_filter_data(sys.argv[2:5])

img_file = os.path.join(os.path.dirname(__file__), img_file)

if not os.path.isfile(img_file):
    img_file = os.path.join(os.path.dirname(__file__), img_file_fallback)

img_dir = os.path.dirname(img_file)

# setup
init_beat()

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
    for wall in range(NOOFWALLS):
        for y in range(WALLSIZEY):
            for x in range(WALLSIZEX):
                ptr = x + y * WALLSIZEX
                if type(data[ptr]) == int:
                    colors = colorfilter(data[ptr],data[ptr],data[ptr], filter_data)
                    send(wall,x,y,colors[0],colors[1],colors[2]);
                else:
                    colors = colorfilter(data[ptr][0],data[ptr][1],data[ptr][2], filter_data)
                    send(wall,x,y,colors[0],colors[1],colors[2]);
    update()


while True:
    for f in frames:
        wait_beat()
        render_frame(img[f])
        #time.sleep(0.42)
