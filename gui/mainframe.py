#!/usr/bin/env python

import wx

from selection import *
from queue import *
from beat_control import *

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

            self.queue = Queue(splitter)
            self.selection = Selection(splitter, self.animations_list, self.queue)

            splitter.SplitVertically(self.selection, self.queue)

            beat_control = BeatControl(panel)

            # Layout
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(beat_control, 0, wx.EXPAND)
            sizer.Add(splitter, 1, wx.EXPAND)
            panel.SetSizer(sizer)

            # Show window
            self.Show(True)

    def OnExit(self, e):
        self.Close(True)
