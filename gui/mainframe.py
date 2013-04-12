#!/usr/bin/env python

import wx

from selection import *
from queue import *
from errorconsole import *

class MainFrame(wx.Frame):
    """ Window for selection of next animations and queue """
    def __init__(self):
            wx.Frame.__init__(self, None, title="LED-Wand")

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

            selection = Selection(tabs)
            queue = Queue(tabs)
            errorconsole = ErrorConsole(tabs)

            tabs.AddPage(selection, "Liste")
            tabs.AddPage(queue, "Queue")
            tabs.AddPage(errorconsole, "Fehlerkonsole")

            # Layout
            sizer = wx.BoxSizer()
            sizer.Add(tabs, wx.ID_ANY, wx.EXPAND)
            panel.SetSizer(sizer)

            # Show window
            self.Show(True)

    def OnExit(self, e):
        self.Close(True)
