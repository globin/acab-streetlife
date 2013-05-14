#!/usr/bin/env python

import wx

from selection import *
from queue import *
from beat_control import *
from color_control import *

class MainFrame(wx.Frame):
    """ Window for selection of next animations and queue """
    def __init__(self, animations_list):
            wx.Frame.__init__(self, None, title="ACAB Control", size=(700, 400))
            self.SetMinSize((600,300))

            self.animations_list = animations_list

            # Menu
            filemenu = wx.Menu()
            exitItem = filemenu.Append(wx.ID_EXIT, "Exit", "Exit program")

            menu = wx.MenuBar()
            menu.Append(filemenu, "File")

            self.SetMenuBar(menu)

            self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

            # Panel with notebook
            panel = wx.Panel(self)

            splitter = wx.SplitterWindow(panel)
            splitter.SetSashGravity(0.5)
            splitter.SetMinimumPaneSize(250)

            self.beat_control = BeatControl(panel)

            self.color_control = ColorControl(panel)

            self.queue = Queue(splitter, self.animations_list, self.color_control)
            self.selection = Selection(splitter, self.animations_list, self.queue, self.color_control)

            splitter.SplitVertically(self.selection, self.queue)

            # Layout
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer_control = wx.BoxSizer(wx.HORIZONTAL)

            sizer_control.Add(self.beat_control, 0, wx.EXPAND)
            sizer_control.Add(self.color_control, 0, wx.EXPAND)

            sizer.Add(sizer_control, 0, wx.EXPAND)
            sizer.Add(splitter, 1, wx.EXPAND)
            panel.SetSizer(sizer)

            # Show window
            self.Show(True)

    def OnExit(self, e):
        self.Close(True)
