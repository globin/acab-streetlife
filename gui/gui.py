#!/usr/bin/env python

import wx
import sys

from mainframe import *
from animation import *
from scheduler import *

def PrintHelp(errno):
    print "LED-Wand GUI"
    print
    print "Parameter: Datei mit Liste aller Animationen"
    print "Die Angaben in der Datei sind relativ zum Pfad der Datei selbst"

    sys.exit(errno)

# Handle argvs
if len(sys.argv) != 2:
    PrintHelp(1)

if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    PrintHelp(0)

animations_file = sys.argv[1]

# Read animations
animations_list = Animation.LoadFromFile(animations_file)

# Scheduler
scheduler = Scheduler()
scheduler.Start()

# Start GUI
app = wx.App(False)
frame = MainFrame(animations_list, scheduler)
app.MainLoop()

scheduler.Stop()
