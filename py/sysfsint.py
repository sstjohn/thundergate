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
import struct
import clib as c
import mm

class SysfsInterface(object):
    def __init__(self, bdf):
        self.bdf = bdf
        self.dd = "/sys/bus/pci/devices/%s" % bdf

    def __enter__(self):
        self._open_device()
        self.mm = mm.MemMgr()

    def _open_device(self):
	with file(self.dd + "/enable", "w") as f:
	    f.write('1')
        self.cfgfd = os.open(self.dd + "/config", os.O_RDWR)
        try: self.barfd = os.open(self.dd + "/resource0_wc", os.O_RDWR)
        except: self.barfd = os.open(self.dd + "/resource0", os.O_RDWR)

        bar0 = c.mmap(0, 64 * 1024, c.PROT_READ | c.PROT_WRITE, c.MAP_SHARED | c.MAP_LOCKED, self.barfd, 0)
        if -1 == bar0: raise Exception("failed to mmap bar 0")
        self.bar0 = bar0

        try:
            self.barfd2 = os.open(self.dd + "/resource2_wc", os.O_RDWR)
            self.bar2 = c.mmap(0, 64 * 1024, c.PROT_READ | c.PROT_WRITE, c.MAP_SHARED | c.MAP_LOCKED, self.barfd2, 0)
        except:
            pass

    def __exit__(self, t, v, traceback):
        self._close_device()

    def _close_device(self):
        if hasattr(self, "bar2"):
            try: c.munmap(self.bar2, 64 * 1024)
            except: pass
        if hasattr(self, "barfd2"):
            try: os.close(self.barfd2)
            except: pass
        c.munmap(self.bar0, 64 * 1024)
        os.close(self.barfd)
        os.close(self.cfgfd)
    
    def reattach(self):
        self._close_device()
        self._open_device()

    def cfg_read(self, offset):
        assert offset >= 0 and offset < 0x400
        os.lseek(self.cfgfd, offset, os.SEEK_SET)
        tmp = os.read(self.cfgfd, 4)
        return struct.unpack("I", tmp)[0]

    def cfg_write(self, offset, val):
        assert offset >= 0 and offset < 0x400
        os.lseek(self.cfgfd, offset, os.SEEK_SET)
        os.write(self.cfgfd, struct.pack("I", val))
