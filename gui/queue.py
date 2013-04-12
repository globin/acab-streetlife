#!/usr/bin/env python

import wx

class Queue(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, wx.ID_ANY, "Queue", (20,20))
