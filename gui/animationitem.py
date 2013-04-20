#!/usr/bin/env python

import wx

class AnimationItem(wx.Panel):
    def __init__(self, parent, animation, queue):
        wx.Panel.__init__(self, parent)

        self.animation = animation

        self.queue = queue

        # Horizontal Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Name
        name = wx.StaticText(self, wx.ID_ANY, self.animation.GetName(), (20,20), (200, -1))
        sizer.Add(name, flag=wx.ALIGN_CENTER_VERTICAL)

        # Queue button
        queue_button = wx.Button(self, wx.ID_ANY, "Queue")
        sizer.Add(queue_button, flag=wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.OnButtonQueue, queue_button)

        self.SetSizer(sizer)

    def OnButtonQueue(self, e):
        self.queue.Insert(self.animation)
