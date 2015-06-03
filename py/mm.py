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

import clib as c
import os
import ctypes
import struct

if not hasattr(c, "MAP_FAILED"):
    setattr(c, "MAP_FAILED", c.c_void_p(-1).value)

class MemMgr(object):
    def __init__(self):
        self.locked_pages = []
        self.allocations = {}
        self.free_list = []
        self._page_sz = c.sysconf(c._SC_PAGESIZE)
        self.__attempt_hugetlb()
        if self._hugetlb_available:
            self.page_sz = self._hugetlb_pgsz
        else:
            self.page_sz = self._page_sz
        try:
            self.memfd = os.open("/dev/mem", os.O_RDONLY)
        except:
            self.memfd = None

    def __attempt_hugetlb(self):
        try:
            with open("/proc/sys/vm/nr_hugepages", "r+") as hp:
                a = int(hp.read())
                if a < 20:
                    hp.seek(0)
                    hp.write('20')
        except: pass
        flags = c.MAP_ANONYMOUS | c.MAP_PRIVATE | c.MAP_LOCKED | c.MAP_HUGETLB | c.MAP_32BIT
        flags |= (21 << c.MAP_HUGE_SHIFT)
        prot = c.PROT_READ | c.PROT_WRITE
        sz = 2048 * 1024
        a = c.mmap(0, sz, prot, flags, -1, 0)
        if a != c.MAP_FAILED:
            print "[+] huge pages available"
            c.munmap(a, sz)
            self._hugetlb_available = True
            self._hugetlb_pgsz = sz
        else:
            print "[-] huge pages unavailable"
            self._hugetlb_available = False

    def read_pmem(self, paddr, count):
        if self.memfd == None:
            raise Exception("memfd not available")
        c.lseek64(self.memfd, paddr, c.SEEK_SET)
        return os.read(self.memfd, count)

    def dump_pmem(self, paddr, count):
        assert 0 == count % 4
        data = self.read_pmem(paddr, count)
        for i in range(0, count, 4):
            if 0 == i % 0x10:
                print
                print "%08x: " % (paddr + i),

            tmp, = struct.unpack('I', data[i:i+4])
            print "%04x %04x" % (tmp >> 16, tmp & 0xffff),
        print

    def get_paddr(self, vaddr):
            page_sz = self._page_sz
            page = vaddr & ~(page_sz - 1)
            offset = vaddr ^ page
            page_idx = page / page_sz

            fd = os.open("/proc/self/pagemap", os.O_RDONLY)
            os.lseek(fd, page_idx << 3, os.SEEK_SET)
            data = os.read(fd, 8)
            os.close(fd)

            data, = struct.unpack("Q", data)
            if not data & 0x8000000000000000:
                    raise Exception("page not present")
            if data & 0x4000000000000000:
                    raise Exception("page swapped")
            if data & 0x2000000000000000: 
                    raise Exception("page mapped")
            pfn = data & 0x7fffffffffffff
            return (pfn * page_sz) | offset

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

	c.memset(victim[0], 0, sz)

        return victim[0]

    def free(self, v):
        sz = self.allocations[v]
        del self.allocations[v]
        c.memset(v, 0xff, sz)
        self.free_list += [(v, sz)]

    def get_page(self):
        if self._hugetlb_available:
            assert self.page_sz == self._hugetlb_pgsz
            prot = c.PROT_READ | c.PROT_WRITE
            flags = c.MAP_ANONYMOUS | c.MAP_PRIVATE | c.MAP_LOCKED | c.MAP_HUGETLB | c.MAP_32BIT
            flags |= (21 << c.MAP_HUGE_SHIFT)
            sz = self._hugetlb_pgsz
            page = c.mmap(0, sz, prot, flags, -1, 0)
            if c.MAP_FAILED == page:
                e = c.errno.value
                raise Exception("mmap: 0x%x" % e)
        else:
            assert self.page_sz == self._page_sz
            page = c.valloc(self._page_sz)
            if 0 == page:
                    raise Exception("valloc")
            if -1 == c.mlock(page, self._page_sz):
                    raise Exception("mlock")

        c.memset(page, 0xFF, self.page_sz)

        self.locked_pages += [page]
        return (page, self.page_sz)

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
