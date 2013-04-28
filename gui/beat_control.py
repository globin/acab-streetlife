#!/usr/bin/env python

import wx
import threading
from acabx import *
from beat_thread import *

MIN_BPM=6
MAX_BPM=240
START_BPM=120

class BeatControl(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Status
        self.live = False
        self.bpm = START_BPM
        self.beat_data = init_beat_server(6001)
        self.beat_lock = threading.Lock()

        # Timer for next manually beat
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.OnNextBeat, self.timer)

        self.RestartTimer()

        # Thread for live beat
        self.thread = BeatThread(self, self.beat_data, self.beat_lock)
        self.thread.start()

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
        self.button_live = wx.RadioButton(self, label="Live", size=(100,-1), style=wx.RB_GROUP)
        self.button_manually = wx.RadioButton(self, label="Manually", size=(100,-1))

        sizer_live.Add(self.button_live, 0, wx.EXPAND)
        sizer_manually.Add(self.button_manually, 0, wx.EXPAND)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton, self.button_live)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton, self.button_manually)

        self.button_live.SetValue(False)
        self.button_manually.SetValue(True)

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

    def __del__(self):
        self.thread.stop()
        self.thread.join()

    def OnScroll(self, e):
        bpm = self.slider.GetValue()

        self.spin.SetValue(bpm)

        self.beat_lock.acquire()
        self.bpm = bpm
        self.beat_lock.release()

        self.RestartTimer()

    def OnSpin(self, e):
        bpm = self.spin.GetValue()

        self.slider.SetValue(bpm)

        self.beat_lock.acquire()
        self.bpm = bpm
        self.beat_lock.release()

        self.RestartTimer()

    def OnRadioButton(self, e):
        self.beat_lock.acquire()
        self.live = self.button_live.GetValue()
        self.beat_lock.release()

    def OnNextBeat(self, e):
        self.beat_lock.acquire()

        if not self.live:
            send_beat(self.beat_data)

        self.timer.Start((60.0/self.bpm)*1000, True)

        self.beat_lock.release()

    def RestartTimer(self):
        self.beat_lock.acquire()

        self.timer.Stop()
        self.timer.Start((60.0/self.bpm)*1000, True)

        self.beat_lock.release()

    def GetLive(self):
        return self.live