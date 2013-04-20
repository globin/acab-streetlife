#!/usr/bin/env python

import wx

class QueueItem(wx.Panel):
    def __init__(self, parent, animation, queue):
        wx.Panel.__init__(self, parent)

        self.animation = animation

        self.queue = queue

        # Horizontal Layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Name
        if animation == None:
            name_str = ""
        else:
            name_str = self.animation.GetName()
        name = wx.StaticText(self, wx.ID_ANY, name_str, (20,20), (200,-1))
        sizer.Add(name, flag=wx.ALIGN_CENTER_VERTICAL)

        # Delete button
        delete_button = wx.Button(self, wx.ID_ANY, "Delete")
        sizer.Add(delete_button, flag=wx.ALIGN_CENTER_VERTICAL)
        self.Bind(wx.EVT_BUTTON, self.OnButtonDelete, delete_button)

        self.SetSizer(sizer)

    def GetAnimation(self):
        return self.animation

    def OnButtonDelete(self, e):
        self.queue.Remove(self)
