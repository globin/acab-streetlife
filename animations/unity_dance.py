#!/usr/bin/env python

import Image
import time
import os
from acabsl import *

# setup
img = {}
frames = []
with open(os.path.join(os.path.dirname(__file__), "dance/dance")) as f:
    for line in f:
        line = line.strip()
        frames.append(line)
        if line not in img:
            img[line] = Image.open(os.path.join(os.path.dirname(__file__), "dance", line)).getdata()

for wall in range(NOOFWALLS):
    for col in range(WALLSIZEX):
        for row in range(WALLSIZEY):
            send(wall,col,row,0,0,0,0)
update()


def render_frame(data):
    for wall in range(NOOFWALLS):
        for y in range(WALLSIZEY):
            for x in range(WALLSIZEX):
                ptr = x + y * WALLSIZEX
                if type(data[ptr]) == int:
                    send(wall,x,y,data[ptr],data[ptr],data[ptr]);
                else:
                    send(wall,x,y,data[ptr][0],data[ptr][1],data[ptr][2]);
    update()


while True:
    for f in frames:
        render_frame(img[f])
        time.sleep(0.42)
