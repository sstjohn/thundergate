'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015  Saul St. John

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

class BlockPage(wx.NotebookPage):
    def __init__(self, parent, block):
        name = block.block_name
        super(BlockPage, self).__init__(parent)
        self.block = block
        parent.AddPage(self, text = name)

def _show_main_frame(dev):
    frame = wx.Frame(None, -1, 'thundergate')
    
    frame.CreateStatusBar()
    
    frame.control = wx.Notebook(frame)
    page = BlockPage(frame.control, dev.rxcpu)

    frame.Show()

def _run(dev):
    app = wx.App()
    _show_main_frame(dev)
    app.MainLoop()

def run(dev):
    t = threading.Thread(target = _run, args = (dev,))
    t.start()
