#!/usr/bin/env python

import wx
import subprocess

from queueitem import *

class Queue(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(10,10)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # Title
        t = wx.StaticText(self, wx.ID_ANY, "Auswahl", style=wx.ALIGN_CENTRE)
        self.sizer.Add(t, 0, wx.EXPAND)

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

    def Insert(self, animation):
        empty = self.IsEmpty()

        tmp = QueueItem(self, animation)
        self.sizer.Add(tmp, 0, wx.EXPAND)

        self.queue.insert(len(self.queue), tmp)

        self.Layout()
        self.FitInside()

        if empty:
            self.PlayNext()

    def InsertFirst(self, animation):
        empty = self.IsEmpty()

        tmp = QueueItem(self, animation)
        self.sizer.Add(tmp, 0, wx.EXPAND)

        self.queue.insert(0, tmp)

        self.Layout()
        self.FitInside()

        if empty:
            self.PlayNext()

    def CurrentAnimation(self):
        if len(self.queue) > 0:
            return self.queue[0].GetAnimation()
        else:
            return None

    def RemoveCurrent(self):
        if len(self.queue) > 0:
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
