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

from ctypes import *

class _TEntry(Structure):
    _fields_ = [("addr_lo", c_uint32),
                ("addr_hi", c_uint32),
                ("data", c_uint32),
                ("ctrl", c_uint32)]

class Table(object):
    def __init__(self, bar, ofs, sz):
        self.bar = bar
        self.ofs = ofs
        self.sz = sz
        self._ptrs = []
        for i in range(sz):
            self._ptrs += [cast(bar + ofs, POINTER(_TEntry))[i]]

    def __len__(self):
        return self.sz

    def __getitem__(self, index):
        if index < 0 or index >= self.sz:
            raise IndexError()

        return self._ptrs[index]

class Pba(object):
    def __init__(self, bar, ofs, sz):
        self.bar = bar
        self.ofs = ofs
        self.sz = sz
