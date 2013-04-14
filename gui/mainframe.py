#!/usr/bin/env python

import wx

from selection import *
from queue import *

class MainFrame(wx.Frame):
    """ Window for selection of next animations and queue """
    def __init__(self, animations_list):
            wx.Frame.__init__(self, None, title="LED-Wand")

            self.animations_list = animations_list

            # Menu
            filemenu = wx.Menu()
            exitItem = filemenu.Append(wx.ID_EXIT, "Beenden", "Programm beenden")

            menu = wx.MenuBar()
            menu.Append(filemenu, "Datei")

            self.SetMenuBar(menu)

            self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

            # Statusbar
            self.CreateStatusBar()

            # Panel with notebook
            panel = wx.Panel(self)
            splitter = wx.SplitterWindow(panel)
            splitter.SetSashGravity(0.5)

            self.queue = Queue(splitter)
            self.selection = Selection(splitter, self.animations_list, self.queue)

            splitter.SplitVertically(self.selection, self.queue)

            # Layout
            sizer = wx.BoxSizer()
            sizer.Add(splitter, 1, wx.EXPAND)
            panel.SetSizer(sizer)

            # Show window
            self.Show(True)

    def OnExit(self, e):
        self.Close(True)
