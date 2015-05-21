#!/usr/bin/env python

import random
import wx

class QueueItem(wx.Panel):
    def __init__(self, parent, animation, queue):
        wx.Panel.__init__(self, parent)

        self.animation = animation

        self.queue = queue

        # Horizontal Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Name
        name_str = self.animation.name
        name = wx.StaticText(self, wx.ID_ANY, name_str, size=(200,-1))
        sizer.Add(name, flag=wx.ALIGN_CENTER_VERTICAL)

        # Color
        color_values = self.animation.color
        print self.animation.color
        if color_values:
            color_str = self.ColorToStr(color_values)
        else:
            color_str = ""
        color = wx.StaticText(self, wx.ID_ANY, color_str, size=(100, -1))
        sizer.Add(color, flag=wx.ALIGN_CENTER_VERTICAL)

        # Delete button
        delete_button = wx.Button(self, wx.ID_ANY, "Delete")
        sizer.Add(delete_button, flag=wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDelete, delete_button)

        self.SetSizer(sizer)

    def GetAnimation(self):
        return self.animation

    def OnButtonDelete(self, e):
        self.queue.Remove(self)

    def ColorToStr(self, c):
        if c == (255, 0, 0):
            return "red"
        elif c == (0, 255, 0):
            return "green"
        elif c == (0, 0, 255):
            return "blue"
        elif c == (0, 255, 255):
            return "cyan"
        elif c == (255, 0, 255):
            return "magenta"
        elif c == (255, 255, 0):
            return "yellow"
        else:
            return str(color_values[0]) + " " + str(color_values[1]) + " " + str(color_values[2])
