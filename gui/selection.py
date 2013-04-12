#!/usr/bin/env python

from animationitem import *

import wx

class Selection(wx.ScrolledWindow):
    def __init__(self, parent, animations_list):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(10,10)

        self.animations_list = animations_list
        self.animations_items = []

        sizer = wx.BoxSizer(wx.VERTICAL)

        for a in self.animations_list:
            tmp = AnimationItem(self, a)
            sizer.Add(tmp, 1, wx.EXPAND)

            self.animations_items.append(tmp)

        self.SetSizer(sizer)
