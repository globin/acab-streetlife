import random
import lib_sl
import time


def rcolor():
  color=[]
  color.append(int(random.random()*255))
  color.append(int(random.random()*255))
  color.append(int(random.random()*255))
  return color

t=5.1
n=0
i=j=0

while 1:
 i=j=0
 x=int(random.random()*8)
 while (j < 6):
    c=rcolor()
    y=j
    lib_sl.send(x,y,c[0],c[1],c[2],t)
    j=j+1
    time.sleep(t/(4*t))
 j=0
 y=int(random.random()*6)
 while (i < 8):
    c=rcolor()
    x=i
    lib_sl.send(x,y,c[0],c[1],c[2],t)
    i=i+1
    time.sleep(t/(4*t))
 time.sleep(t/(4*t))


   


