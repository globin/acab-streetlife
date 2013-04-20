#!/usr/bin/env python

from animationitem import *

import wx

class Selection(wx.ScrolledWindow):
    def __init__(self, parent, animations_list, queue):
        wx.ScrolledWindow.__init__(self, parent)
        self.SetScrollRate(10,10)

        self.animations_list = animations_list
        self.animations_items = []

        self.queue = queue

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        t = wx.StaticText(self, wx.ID_ANY, "Auswahl", style=wx.ALIGN_CENTRE)
        sizer.Add(t, 0, wx.EXPAND)

        for a in self.animations_list:
            tmp = AnimationItem(self, a, self.queue)
            sizer.Add(tmp, 0, wx.EXPAND)

            self.animations_items.append(tmp)

        self.SetSizer(sizer)
