#!/usr/bin/env python

from animationitem import *

import wx

class Selection(wx.ScrolledWindow):
    def __init__(self, parent, animations_list, queue, color):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(10,10)

        self.animations_list = animations_list
        self.animations_items = []

        self.queue = queue

        self.color = color

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        t = wx.StaticText(self, wx.ID_ANY, "Auswahl", style=wx.ALIGN_CENTRE)
        f = t.GetFont()
        f.SetWeight(wx.BOLD)
        t.SetFont(f)
        sizer.Add(t, 0, wx.EXPAND)

        for a in self.animations_list:
            tmp = AnimationItem(self, a, self.queue, self.color)
            sizer.Add(tmp, 0, wx.EXPAND | wx.BOTTOM, 15)

            self.animations_items.append(tmp)

        self.SetSizer(sizer)
