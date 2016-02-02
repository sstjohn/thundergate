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
from dvm import GenDVM

class GenTree(wx.dataview.DataViewCtrl):
    def __init__(self, parent, root, model):
        super(GenTree, self).__init__(parent)
        self.AssociateModel(GenDVM(root, model))
        self.AppendTextColumn("name", 0)
        self.AppendTextColumn("value", 1)
        self.AppendTextColumn("type", 2)
