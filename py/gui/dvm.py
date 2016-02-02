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
from datamodel import get_data_value

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
            if len(o.children) == 0:
                data = get_data_value(o, self.model, self.root)
                return str(data)
            return ""
        if col == 2:
            return str(getattr(o, "val_type", ""))
