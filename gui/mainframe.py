#!/usr/bin/env python

import wx

from selection import *
from queue import *
from errorconsole import *

class MainFrame(wx.Frame):
    """ Window for selection of next animations and queue """
    def __init__(self, animations_list, scheduler):
            wx.Frame.__init__(self, None, title="LED-Wand")

            self.animations_list = animations_list
            self.scheduler = scheduler

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
            tabs = wx.Notebook(panel)

            self.selection = Selection(tabs, self.animations_list, self.scheduler)
            self.queue = Queue(tabs)
            self.errorconsole = ErrorConsole(tabs)

            tabs.AddPage(self.selection, "Liste")
            tabs.AddPage(self.queue, "Queue")
            tabs.AddPage(self.errorconsole, "Fehlerkonsole")

            # Layout
            sizer = wx.BoxSizer()
            sizer.Add(tabs, 1, wx.EXPAND)
            panel.SetSizer(sizer)

            # Print list of animations
            self.PrintError("Animations:")
            for a in self.animations_list:
                self.PrintError(a.GetFile())
            self.PrintError("")

            # Show window
            self.Show(True)

    def OnExit(self, e):
        self.Close(True)

    def PrintError(self, error):
        self.errorconsole.AddText(error)
