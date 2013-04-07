#!/usr/bin/python

from acabsl import *
import colorsys
import random
import time

tick = 0.5

r = 0
g = 180
b = 250
shade = 3

def blank_walls():
  for col in range(WALLSIZEX):
    for row in range(WALLSIZEY):
      for wall in range(NOOFWALLS):
        send(wall,col,row,0,0,0,0);
  update()

def warp_ring(wall, row, time):
  for i in range(WALLSIZEX):
    if row < WALLSIZEY - 1: 
      send(wall,i,row+1,r/shade,g/shade,b/shade,time);
    if row <= WALLSIZEY - 1:
      send(wall,i,row,r,g,b,time);
    if row > 0 and row <= WALLSIZEY:
      send(wall,i, row-1,r/shade,g/shade,b/shade,time);

  update()


c = 0

blank_walls()

while 1:
  for i in range(0,NOOFWALLS):
    warp_ring(i, c, tick)

  c += 1
  c = c % (WALLSIZEY + 2)

  time.sleep(tick)
  
  blank_walls()


