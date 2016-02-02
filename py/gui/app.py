'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016 Saul St. John

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import wx
import threading
from tree import GenTree
from dvm import RegDVM, MemDVM
from nved import NvramEditor

class App(wx.App):
    def __init__(self, dev):
        self.dev = dev
        super(App, self).__init__()

    def OnInit(self):
        self.toplevel = wx.Frame(None, -1)
        self.ShowMain()
        return True

    def ShowTest(self):
        frame = wx.Frame(self.toplevel, -1, 'test!')
        editor = NvramEditor(frame, self.dev)
        frame.Show()

    def ShowMain(self):
        frame = wx.Frame(self.toplevel, -1, 'thundergate')
        
        frame.CreateStatusBar()
        
        nb = wx.Notebook(frame)
        page = GenTree(nb, self.dev, RegDVM)
        nb.AddPage(page, text="registers")
        page = GenTree(nb, self.dev, MemDVM)
        nb.AddPage(page, text="memory")
        page = NvramEditor(nb, self.dev)
        nb.AddPage(page, text="nvram")
        
        frame.Show()

    def Invoke(self, fun):
        wx.CallAfter(fun)

