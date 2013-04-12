#!/usr/bin/env python

import wx

# TODO: MAX_LINES

class ErrorConsole(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Display text
        self.textwidget = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.textwidget.SetEditable(False)

        sizer = wx.BoxSizer()
        sizer.Add(self.textwidget, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def AddText(self, text):
        if not self.textwidget.IsEmpty():
            text = "\n" + text
        self.textwidget.AppendText(text)
