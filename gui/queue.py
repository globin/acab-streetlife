#!/usr/bin/env python

import wx
import subprocess

from queueitem import *

class Queue(wx.ScrolledWindow):
    def __init__(self, parent, animations_list, color_control):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(10,10)

        self.animations_list = animations_list
        self.color_control = color_control

        # Sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # Title
        t = wx.StaticText(self, wx.ID_ANY, "Queue", style=wx.ALIGN_CENTRE)
        f = t.GetFont()
        f.SetWeight(wx.BOLD)
        t.SetFont(f)
        self.sizer.Add(t, 0, wx.EXPAND)

        # Auto refill
        self.check_auto_refill = wx.CheckBox(self, wx.ID_ANY, "Auto refill")
        self.check_auto_refill.SetValue(True)
        self.sizer.Add(self.check_auto_refill, 0, wx.EXPAND)

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

        # Init random number generator
        random.seed()

    def __del__(self):
        self.timer.Stop()

        if self.process != None:
            self.KillProcess()

    def Insert(self, animation, pos = -1, do_not_start = False):
        empty = self.IsEmpty()

        if pos == -1:
            pos = len(self.queue)

        # Remove items behind new item from sizer
        for i in range(pos, len(self.queue)):
            self.items_sizer.Detach(self.queue[i])

        # Add new item
        tmp = QueueItem(self, animation, self)
        self.items_sizer.Add(tmp, 0, wx.EXPAND)

        self.queue.insert(pos, tmp)

        # Add removed items behind new item to sizer
        for i in range(pos+1, len(self.queue)):
            self.items_sizer.Add(self.queue[i], 0, wx.EXPAND)

        self.Layout()
        self.FitInside()

        if empty and not do_not_start:
            self.PlayNext()

    def InsertFirst(self, animation):
        self.Insert(animation, 0)
        self.PlayNext(no_remove = True)

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

    def PlayNext(self, no_remove = False):
        # Kill last process
        if self.process != None:
            self.KillProcess()
            if not no_remove:
                self.RemoveCurrent()

        # Add random animation
        if self.IsEmpty() and self.check_auto_refill.GetValue():
            tmp = self.animations_list[random.randint(0, len(self.animations_list)-1)]
            tmp.color = self.color_control.color
            self.Insert(tmp, do_not_start = True)

        # Start next process
        if not self.IsEmpty():
            animation = self.CurrentAnimation()
            cmd = ["python", animation.file]
            cmd.extend(animation.parsedConfig)
            cmd.append(animation.fadetime)
            self.process=subprocess.Popen(cmd)

            print "[" + str(self.process.pid) + "] " + animation.file + "".join(str(" " + i) for i in animation.parsedConfig)

            self.timer.Start(animation.time*1000, True)

    def OnNextTimer(self, e):
        self.PlayNext()
