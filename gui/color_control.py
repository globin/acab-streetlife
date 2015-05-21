#!/usr/bin/env python

import wx
import random

class ColorControl(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._color = (0, 255, 0)

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_colors = wx.BoxSizer(wx.HORIZONTAL)
        sizer_rgb = wx.BoxSizer(wx.VERTICAL)
        sizer_cmy = wx.BoxSizer(wx.VERTICAL)

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

        self.button_cyan = wx.RadioButton(self, label="Cyan", size=(100,-1))
        self.button_magenta = wx.RadioButton(self, label="Magenta", size=(100,-1))
        self.button_yellow = wx.RadioButton(self, label="Yellow", size=(100,-1))
        self.button_random = wx.RadioButton(self, label="Random", size=(100,-1))

        sizer_rgb.Add(self.button_red, 0, wx.EXPAND)
        sizer_rgb.Add(self.button_green, 0, wx.EXPAND)
        sizer_rgb.Add(self.button_blue, 0, wx.EXPAND)

        sizer_cmy.Add(self.button_cyan, 0, wx.EXPAND)
        sizer_cmy.Add(self.button_magenta, 0, wx.EXPAND)
        sizer_cmy.Add(self.button_yellow, 0, wx.EXPAND)
        sizer_cmy.Add(self.button_random, 0, wx.EXPAND)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_red)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_green)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_blue)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_cyan)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_magenta)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_yellow)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnChoose, self.button_random)

        self.button_green.SetValue(True)

        # Sizer
        sizer_colors.Add(sizer_rgb, 0, wx.EXPAND)
        sizer_colors.Add(sizer_cmy, 0, wx.EXPAND)
        sizer.Add(sizer_colors, 0 , wx.EXPAND)

        self.SetSizer(sizer)

    def OnChoose(self, e):
        if self.button_red.GetValue():
            self._color = (255, 0, 0)
        elif self.button_green.GetValue():
            self._color = (0, 255, 0)
        elif self.button_blue.GetValue():
            self._color = (0, 0, 255)
        elif self.button_cyan.GetValue():
            self._color = (0, 255, 255)
        elif self.button_magenta.GetValue():
            self._color = (255, 0, 255)
        elif self.button_yellow.GetValue():
            self._color = (255, 255, 0)

        if self.button_random.GetValue():
            self._color = "random"

    @property
    def color(self):
        if self._color == "random":
            return random.choice([
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (0, 255, 255),
                (255, 0, 255),
                (255, 255, 0),
            ])

        return self._color
