#!/usr/bin/env python

import wx
import subprocess

class Queue(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, wx.ID_ANY, "Queue", (20,20))

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

        self.queue.insert(len(self.queue), animation)

        if empty:
            self.PlayNext()

    def InsertFirst(self, animation):
        empty = self.IsEmpty()

        self.queue.insert(0, animation)

        if empty:
            self.PlayNext()

    def Current(self):
        if len(self.queue) > 0:
            return self.queue[0]
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
            animation = self.Current()
            self.process=subprocess.Popen(["python", animation.GetFile()])

            print "[" + str(self.process.pid) + "] " + animation.GetFile()

            self.timer.Start(animation.GetTime()*1000, True)

    def OnNextTimer(self, e):
        self.PlayNext()
