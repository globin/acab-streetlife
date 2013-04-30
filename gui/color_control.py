#!/usr/bin/env python

import wx

class ColorControl(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.color = (0, 255, 0)

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_colors = wx.BoxSizer(wx.VERTICAL)

        # Title
        t = wx.StaticText(self, wx.ID_ANY, "Color control", style=wx.ALIGN_CENTRE)
        f = t.GetFont()
        f.SetWeight(wx.BOLD)
        t.SetFont(f)
        sizer.Add(t, 0, wx.EXPAND)

        # Radio buttons
        self.button_red = wx.RadioButton(self, label="Red", size=(100,-1), style=wx.RB_GROUP)
        self.button_green = wx.RadioButton(self, label="Green", size=(100,-1))
        self.button_blue = wx.RadioButton(self, label="Blue", size=(100,-1))

        sizer_colors.Add(self.button_red, 0, wx.EXPAND)
        sizer_colors.Add(self.button_green, 0, wx.EXPAND)
        sizer_colors.Add(self.button_blue, 0, wx.EXPAND)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_red)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_green)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_blue)

        self.button_red.SetValue(False)
        self.button_green.SetValue(True)
        self.button_blue.SetValue(False)

        # Sizer
        sizer.Add(sizer_colors, 0 , wx.EXPAND)

        self.SetSizer(sizer)

    def OnChoose(self, e):
        if self.button_red.GetValue():
            self.color = (255, 0, 0)
        elif self.button_green.GetValue():
            self.color = (0, 255, 0)
        elif self.button_blue.GetValue():
            self.color = (0, 0, 255)

    def GetColor(self):
        return self.color
