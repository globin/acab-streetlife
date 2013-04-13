#!/usr/bin/env python

import Image
import time
import os
from acabsl import *

# setup
img = Image.open(os.path.join(os.path.dirname(__file__), "unity.png"))
img_width = img.size[0]
img_raw = img.getdata()

for wall in range(NOOFWALLS):
    for col in range(WALLSIZEX):
        for row in range(WALLSIZEY):
            send(wall,col,row,0,0,0,0)
update()


def render_frame(data, shift):
    ptr = 0
    for wall in range(NOOFWALLS):
        for y in range(WALLSIZEY):
            for tx in range(WALLSIZEX):
                ix = (tx + shift) % img_width
                ptr = ix + y * img_width
                if type(data[ptr]) == int:
                    send(wall,tx,y,data[ptr],data[ptr],data[ptr]);
                else:
                    send(wall,tx,y,data[ptr][0],data[ptr][1],data[ptr][2]);
    update()


while True:
    for shift in range(img_width):
        render_frame(img_raw, shift)
        time.sleep(0.2)
