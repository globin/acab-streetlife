#!/usr/bin/env python

from acabsl import *
import time

tick = 0.5
fade = 0.5

x = 0
y = 0

tack = True

while 1:
    for wall in range(0,NOOFWALLS):
        for col in range(WALLSIZEX):
            for row in range(WALLSIZEY):
                if col == x and row == y and tack:
                    send(wall, col, row, 0, 0, 0, fade)
                else:
                    send(wall,col,row,255,255,255,fade);
    update()

    tack = not tack

    if tack:
        x = x+1
        if x >= WALLSIZEX:
            x = 0
            y = (y+1) % WALLSIZEY

    time.sleep(tick)
