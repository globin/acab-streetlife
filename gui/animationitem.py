#!/usr/bin/env python

import wx
from copy import copy

MIN_SECOND=5

class AnimationItem(wx.Panel):
    def __init__(self, parent, animation, queue, color):
        wx.Panel.__init__(self, parent)

        self.animation = animation
        self.time = 30

        self.queue = queue

        self.color = color

        # Horizontal Layout: Name, Buttons
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Name
        name = wx.StaticText(self, wx.ID_ANY, self.animation.name, size=(200, -1))
        hsizer.Add(name, flag=wx.ALIGN_CENTER_VERTICAL)

        # Queue button
        queue_button = wx.Button(self, wx.ID_ANY, "Add")
        hsizer.Add(queue_button, flag=wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.OnButtonQueue, queue_button)

        # Insert First button
        insert_first_button = wx.Button(self, wx.ID_ANY, "Add first")
        hsizer.Add(insert_first_button, flag=wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.OnInsertFirst, insert_first_button)

        # Time
        time_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.time_slider = wx.Slider(self, value=30, minValue=MIN_SECOND, maxValue=600, size=(300,-1))
        self.time_minute = wx.SpinCtrl(self, initial=0, min=0, max=10, size=(50, -1))
        self.time_second = wx.SpinCtrl(self, initial=30, min=0, max=59, size=(50, -1))

        self.Bind(wx.EVT_SCROLL, self.OnScroll, self.time_slider)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin, self.time_minute)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin, self.time_second)

        time_sizer.Add(self.time_slider, 0, wx.EXPAND)
        time_sizer.Add(self.time_minute, 0, wx.EXPAND)
        time_sizer.Add(self.time_second, 0, wx.EXPAND)

        # Vertical Layout: Name, Time
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer, 0, wx.EXPAND)
        vsizer.Add(time_sizer, 0, wx.EXPAND)

        self.SetSizer(vsizer)

    def OnButtonQueue(self, e):
        tmp = copy(self.animation)
        tmp.time = self.time
        tmp.color = self.color.color
        self.queue.Insert(tmp)

    def OnInsertFirst(self, e):
        tmp = copy(self.animation)
        tmp.time = self.time
        tmp.color = self.color.color
        self.queue.InsertFirst(tmp)

    def OnScroll(self, e):
        seconds = self.time_slider.GetValue()
        ms = self._from_seconds(seconds)

        self.time_minute.SetValue(ms[0])
        self.time_second.SetValue(ms[1])

        self.time = seconds

    def OnSpin(self, e):
        minute = self.time_minute.GetValue()
        second = self.time_second.GetValue()

        if minute == 0 and second < MIN_SECOND:
            second = MIN_SECOND
            self.time_second.SetValue(second)

        seconds = self._to_seconds(minute, second)

        self.time_slider.SetValue(seconds)

        self.time = seconds

    def _from_seconds(self, seconds):
        s = seconds % 60
        m = (seconds - s) / 60

        return (m,s)

    def _to_seconds(self, minutes, seconds):
        return minutes*60 + seconds
