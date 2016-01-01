'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016  Saul St. John

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
from ctypes import *
from ctypes.wintypes import *
import struct
from mm import _MemMgr
from winlib import *

class WinMemMgr(_MemMgr):
    def __init__(self, hdev):
        super(WinMemMgr, self).__init__()

        si = SYSTEM_INFO()
        GetSystemInfo(pointer(si))

        #self.page_sz = si.dwPageSize

        print "[.] windows system page size is %d" % self.page_sz
        add_process_privilege(SE_LOCK_MEMORY_NAME)
        self.locked_pages = {}
        self.hdev = hdev

    def read_pmem(self, paddr, count):
        ioctl_input = ULONG_PTR(paddr)
        ioctl_output = (c_char * count)()
        bytes_returned = DWORD(0)
        if not DeviceIoControl(self.hdev, IOCTL_TGWINK_READ_PHYS, 
                               pointer(ioctl_input), sizeof(ULONG_PTR), 
                               pointer(ioctl_output), count, 
                               pointer(bytes_returned), None):
            raise WinError()
        return ioctl_output.raw

    def get_paddr(self, vaddr):
        return ((self.locked_pages[vaddr & ~0xfff]) << 12) | (vaddr & 0xfff)

    def get_page(self):
        sz = ULONG_PTR(1)
        ar = ULONG_PTR(0)
        if not AllocateUserPhysicalPages(-1, pointer(sz), pointer(ar)):
            raise WinError()
        if sz.value != 1:
            raise MemoryError()
        pfn = ar.value
        va = VirtualAlloc(None, self.page_sz, MEM_RESERVE | MEM_PHYSICAL, PAGE_READWRITE)
        if 0 == va:
            raise WinError()

        if not MapUserPhysicalPages(va, sz, pointer(ar)):
            raise WinError()

        self.locked_pages[va] = pfn

        return (va, self.page_sz)