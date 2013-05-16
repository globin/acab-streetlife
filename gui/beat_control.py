#!/usr/bin/env python

import wx
import threading
from acabx import *
from beat_thread import *

from hosts import *

MIN_BPM=6
MAX_BPM=240
START_BPM=120

STROBO_BPM=400

class BeatControl(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Status
        self.live = False
        self.skip = 0
        self.bpm = START_BPM
        self.beat_data = init_beat_server(AUDIO_CLIENT_HOST, 6001)
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
        t = wx.StaticText(self, wx.ID_ANY, "Beat control")
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

        # Skip beat
        # Text: BPM
        t_skip = wx.StaticText(self, wx.ID_ANY, "Skip beat:")
        sizer_live.Add(t_skip, 0, flag=wx.ALIGN_CENTER_VERTICAL)

        # Slider
        self.spin_skip = wx.SpinCtrl(self, initial=0, min=0, max=3, size=(60, -1))

        self.Bind(wx.EVT_SPINCTRL, self.OnSpinSkip, self.spin_skip)

        sizer_live.Add(self.spin_skip, 0, wx.EXPAND)


        # Text: BPM
        t_bpm = wx.StaticText(self, wx.ID_ANY, "BPM:")
        sizer_manually.Add(t_bpm, 0, flag=wx.ALIGN_CENTER_VERTICAL)

        # Slider
        self.slider = wx.Slider(self, value=START_BPM, minValue=MIN_BPM, maxValue=MAX_BPM, size=(300,-1))
        self.spin = wx.SpinCtrl(self, initial=START_BPM, min=MIN_BPM, max=MAX_BPM, size=(60, -1))

        self.Bind(wx.EVT_SCROLL, self.OnScroll, self.slider)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin, self.spin)

        sizer_manually.Add(self.slider, 0, wx.EXPAND)
        sizer_manually.Add(self.spin, 0, wx.EXPAND)

        # Strobo button
        self.strobo_button = wx.ToggleButton(self, wx.ID_ANY, "STROBO!")
        sizer_live.Add(self.strobo_button, 0, wx.EXPAND)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnStrobo, self.strobo_button)

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

    def OnStrobo(self, e):
        if self.strobo_button.GetValue(): # Strobo on
            self.beat_lock.acquire()
            self.bpm_old = self.bpm
            self.bpm = STROBO_BPM
            self.beat_lock.release()

            self.button_live.Enable(False)
            self.button_manually.Enable(False)
            self.spin_skip.Enable(False)
            self.spin.Enable(False)
            self.slider.Enable(False)

        else: # Strobo off
            self.beat_lock.acquire()
            self.bpm = self.bpm_old
            self.beat_lock.release()

            self.button_live.Enable(True)
            self.button_manually.Enable(True)
            self.spin_skip.Enable(True)
            self.spin.Enable(True)
            self.slider.Enable(True)

    def OnSpinSkip(self, e):
        self.skip = self.spin_skip.GetValue()

    def RestartTimer(self):
        self.beat_lock.acquire()

        self.timer.Stop()
        self.timer.Start((60.0/self.bpm)*1000, True)

        self.beat_lock.release()

    def GetLive(self):
        return self.live
    
    def GetSkip(self):
        return self.skip
