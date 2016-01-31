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
import wx.dataview
import threading
from datamodel import model_registers, model_memory


class GenDVM(wx.dataview.PyDataViewModel):
    def __init__(self, root, model):
        super(GenDVM, self).__init__()
        self.root = root
        self.model = model

    def GetColumnCount(self):
        return 3

    def GetColumnType(self, col):
        return 'string'

    def GetChildren(self, parent, children):
        if not parent:
            source = self.model
        else:
            source = self.ItemToObject(parent)
        
        child_objs = getattr(source, "children", [])
        for child in child_objs:
            item = self.ObjectToItem(child)
            children.append(item)
        
        return len(child_objs)

    def IsContainer(self, item):
        if not item:
            return True

        o = self.ItemToObject(item)
        c = getattr(o, "children", [])
        return len(c) > 0

    def GetParent(self, item):
        if item:
            o = self.ItemToObject(item)
            if o.parent is not self.model:
                return self.ObjectToItem(o.parent)
        return wx.dataview.NullDataViewItem

    def GetValue(self, item, col):
        o = self.ItemToObject(item)
        if col == 0:
            return str(o.name)
        if col == 1:
            if hasattr(o, "val_type"):
                try:
                    data = self._get_data_value(o)
                    return str(data)
                except: pass
            return ""
        if col == 2:
            return str(getattr(o, "val_type", ""))

    def _get_data_value(self, o):
        if o.parent == self.model:
            return self.root
        parent_data = self._get_data_value(o.parent)
        return getattr(parent_data, o.name)

class RegDVM(GenDVM):
    def __init__(self, dev):
        super(RegDVM, self).__init__(dev, model_registers(dev))

class MemDVM(GenDVM):
    def __init__(self, dev):
        super(MemDVM, self).__init__(dev.mem, model_memory(dev))

class GenTree(wx.dataview.DataViewCtrl):
    def __init__(self, parent, root, dvm):
        super(GenTree, self).__init__(parent)
        dvm = dvm(root)
        self.AssociateModel(dvm)
        self.AppendTextColumn("name", 0)
        self.AppendTextColumn("value", 1)
        self.AppendTextColumn("type", 2)

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
