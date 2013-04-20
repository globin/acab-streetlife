#!/usr/bin/env python

import wx
import subprocess

from queueitem import *

class Queue(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(10,10)

        # Sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # Title
        t = wx.StaticText(self, wx.ID_ANY, "Auswahl", style=wx.ALIGN_CENTRE)
        self.sizer.Add(t, 0, wx.EXPAND)

        # Sizer for items
        self.items_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.items_sizer, 0, wx.EXPAND)

        # Queue
        self.queue = [] # First element: plays/next to play

        # Timer for next animation
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.OnNextTimer, self.timer)

        # Process with animation
        self.process = None

    def __del__(self):
        self.timer.Stop()

        if self.process != None:
            self.KillProcess()

    def Insert(self, animation, pos = -1):
        empty = self.IsEmpty()

        if pos == -1:
            pos = len(self.queue)

        tmp = QueueItem(self, animation, self)
        self.items_sizer.Add(tmp, 0, wx.EXPAND)

        self.queue.insert(pos, tmp)

        self.Layout()
        self.FitInside()

        if empty:
            self.PlayNext()

    def InsertFirst(self, animation):
        self.Insert(animation, 0)

    def CurrentAnimation(self):
        if len(self.queue) > 0:
            return self.queue[0].GetAnimation()
        else:
            return None

    def Remove(self, queue_item):
        if len(self.queue) > 0:
            index = self.queue.index(queue_item)

            if index == 0:  # Current animation -> play next (and kill current animation process)
                self.PlayNext()
            else:           # Remove from list
                self.items_sizer.Hide(queue_item)
                self.items_sizer.Remove(queue_item)

                self.Layout()
                self.FitInside()

                self.queue.pop(index)
        else:
            return None

    def RemoveCurrent(self):
        if len(self.queue) > 0:
            self.items_sizer.Hide(0)
            self.items_sizer.Remove(0)

            self.Layout()
            self.FitInside()

            return self.queue.pop(0)
        else:
            return None

    def IsEmpty(self):
        return len(self.queue) == 0

    def KillProcess(self):
        if self.process != None:
            print "[" + str(self.process.pid) + "] Killed"
            self.process.kill()
            self.process = None

    def PlayNext(self):
        # Kill last process
        if self.process != None:
            self.KillProcess()
            self.RemoveCurrent()

        # Start next process
        if not self.IsEmpty():
            animation = self.CurrentAnimation()
            self.process=subprocess.Popen(["python", animation.GetFile()])

            print "[" + str(self.process.pid) + "] " + animation.GetFile()

            self.timer.Start(animation.GetTime()*1000, True)

    def OnNextTimer(self, e):
        self.PlayNext()
