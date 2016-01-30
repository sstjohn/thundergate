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

class BFDisplay(wx.ListCtrl):
    def __init__(self, parent, block):
        super(BFDisplay, self).__init__(parent, -1, style = wx.LC_REPORT)
        self.block = block
        self.InsertColumn(0, 'Field')
        self.InsertColumn(1, 'Value')
        self.InsertStringItem(1, 'test1')
        self.InsertStringItem(2, 'test2')

class WordPicker(wx.ListCtrl):
    def __init__(self, parent, details, block):
        super(WordPicker, self).__init__(parent, -1, style = wx.LC_REPORT | wx.LC_NO_HEADER)
        self.block = block
        self.details = details
        self.InsertColumn(0, 'Word')
        self.InsertStringItem(1, "status")
        self.InsertStringItem(2, "mode")
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
    
    def onItemSelected(self, event):
        idx = event.m_itemIndex
        if idx == 1:
            lbl = "status"
        else:
            lbl = "mode"
        self.details.DeleteAllItems()

class BlockPage(wx.Panel):
    def __init__(self, parent, block):
        super(BlockPage, self).__init__(parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_panel = wx.Panel(self)
        reg_view = BFDisplay(right_panel, block)
        left_panel = wx.Panel(self)
        reg_picker = WordPicker(left_panel, reg_view, block)
        sizer.Add(left_panel, 1, wx.EXPAND)
        sizer.Add(right_panel, 1, wx.EXPAND)
        self.SetSizerAndFit(sizer)

def _show_main_frame(dev):
    frame = wx.Frame(None, -1, 'thundergate')
    
    frame.CreateStatusBar()
    
    nb = wx.Notebook(frame)
    for block_name in ['rxcpu']:
        block = getattr(dev, block_name)
        page = BlockPage(nb, block)
        nb.AddPage(page, text = block_name)

    frame.Show()

def _run(dev):
    app = wx.App()
    _show_main_frame(dev)
    app.MainLoop()

def run(dev):
    t = threading.Thread(target = _run, args = (dev,))
    t.start()
