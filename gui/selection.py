#!/usr/bin/env python

import wx

class Selection(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, wx.ID_ANY, "Select animation", (20,20))
