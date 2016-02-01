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

def _show_main_frame(dev):
    frame = wx.Frame(None, -1, 'thundergate')
    
    frame.CreateStatusBar()
    
    nb = wx.Notebook(frame)
    page = GenTree(nb, dev, RegDVM)
    nb.AddPage(page, text="registers")
    page = GenTree(nb, dev, MemDVM)
    nb.AddPage(page, text="memory")
    
    frame.Show()

def _run(dev):
    app = wx.App()
    _show_main_frame(dev)
    app.MainLoop()

def run(dev):
    t = threading.Thread(target = _run, args = (dev,))
    t.daemon = True
    t.start()
    return t
