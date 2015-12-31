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
from mm import _MemMgr
from winlib import *

class WinMemMgr(_MemMgr):
    def __init__(self):
        super(WinMemMgr, self).__init__()

        si = SYSTEM_INFO()
        GetSystemInfo(pointer(si))

        self.page_sz = si.dwPageSize

        print "[.] windows system page size is %d" % self.page_sz

    def get_paddr(self, vaddr):
        raise NotImplementedError()

    def get_page(self):
        #return (page, self.page_sz)
        raise NotImplementedError()