#!/usr/bin/env python

import wx

MIN_BPM=6
MAX_BPM=240
START_BPM=120

class BeatControl(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer_live = wx.BoxSizer(wx.HORIZONTAL)
        sizer_manually = wx.BoxSizer(wx.HORIZONTAL)

        # Title
        t = wx.StaticText(self, wx.ID_ANY, "Beat control", style=wx.ALIGN_CENTRE)
        f = t.GetFont()
        f.SetWeight(wx.BOLD)
        t.SetFont(f)
        sizer.Add(t, 0, wx.EXPAND)

        # Radio buttons
        button_live = wx.RadioButton(self, label="Live", size=(100,-1), style=wx.RB_GROUP)
        button_manually = wx.RadioButton(self, label="Manually", size=(100,-1))
        sizer_live.Add(button_live, 0, wx.EXPAND)
        sizer_manually.Add(button_manually, 0, wx.EXPAND)

        # Text: BPM
        t = wx.StaticText(self, wx.ID_ANY, "BPM:", style=wx.ALIGN_CENTRE)
        sizer_manually.Add(t, 0, wx.EXPAND)

        # Slider
        self.slider = wx.Slider(self, value=START_BPM, minValue=MIN_BPM, maxValue=MAX_BPM, size=(300,-1))
        self.spin = wx.SpinCtrl(self, initial=START_BPM, min=MIN_BPM, max=MAX_BPM, size=(60, -1))

        self.Bind(wx.EVT_SCROLL, self.OnScroll, self.slider)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin, self.spin)

        sizer_manually.Add(self.slider, 0, wx.EXPAND)
        sizer_manually.Add(self.spin, 0, wx.EXPAND)

        # Sizer
        sizer.Add(sizer_live, 0 , wx.EXPAND)
        sizer.Add(sizer_manually, 0 , wx.EXPAND)

        self.SetSizer(sizer)

    def OnScroll(self, e):
        bpm = self.slider.GetValue()

        self.spin.SetValue(bpm)

    def OnSpin(self, e):
        bpm = self.spin.GetValue()

        self.slider.SetValue(bpm)
