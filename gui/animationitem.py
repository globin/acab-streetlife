#!/usr/bin/env python

import wx

class AnimationItem(wx.Panel):
    def __init__(self, parent, animation):
        wx.Panel.__init__(self, parent)

        self.animation = animation

        t = wx.StaticText(self, wx.ID_ANY, self.animation.GetFile(), (20,20))
