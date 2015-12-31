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

import os
import ctypes
import struct

class __mm_system_interface(object):
    def get_paddr(self, vaddr):
        raise NotImplementedError()
    def get_page(self):
        raise NotImplementedError()
    memset = None

class _MemMgr(__mm_system_interface):
    def __init__(self):
        self.locked_pages = []
        self.allocations = {}
        self.free_list = []

        self.page_sz = 4096


    def alloc(self, sz = None):
        if sz == None:
            sz = self.page_sz
        if sz > self.page_sz:
            raise Exception("too big")

        victim = self.get_free(sz)
        if None is victim:
            victim = self.get_page()

        if victim[1] > sz:
            self.free_list += [(victim[0] + sz, victim[1] - sz)]

        self.allocations[victim[0]] = sz

        try:
            self.memset(victim[0], 0, sz)
        except:
            pass

        return victim[0]

    def free(self, v):
        sz = self.allocations[v]
        del self.allocations[v]
        c.memset(v, 0xff, sz)
        self.free_list += [(v, sz)]


    def get_free(self, minsize):
        self.free_coal()
        candidates = [c for c in self.free_list if c[1] >= minsize]
        if len(candidates) == 0:
            return None

        choice = min(candidates, key=lambda c: c[1])
        self.free_list.remove(choice)
        return choice

    def free_coal(self):
        self.free_list.sort()
        for i in range(len(self.free_list) - 1, 0, -1):
            if self.free_list[i-1][0] + self.free_list[i-1][1] == self.free_list[i][0]:
                self.free_list[i-1] = (self.free_list[i-1][0], self.free_list[i-1][1] + self.free_list[i][1])
                self.free_list.remove(self.free_list[i])