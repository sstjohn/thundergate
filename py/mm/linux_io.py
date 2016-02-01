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
from linux import LinuxMemMgr

class IOMemMgr(LinuxMemMgr):
    def __init__(self, container):
        super(IOMemMgr, self).__init__()
        self.container = container

    def get_page(self):
        page, page_sz = super(IOMemMgr, self).get_page()
        first_paddr = self.get_paddr(page)
        for i in range(0, page_sz, 4096):
            assert self.get_paddr(page + i) == (first_paddr + i)
        
        dma_map = c.vfio_iommu_type1_dma_map()
        dma_map.argsz = c.sizeof(c.vfio_iommu_type1_dma_map)
        dma_map.vaddr = page
        dma_map.size = page_sz
        dma_map.iova = self.get_paddr(page)
        dma_map.flags = c.VFIO_DMA_MAP_FLAG_READ | c.VFIO_DMA_MAP_FLAG_WRITE
        res = c.ioctl(self.container, c.VFIO_IOMMU_MAP_DMA, c.byref(dma_map))
        e = c.errno.value
        while res:
            if e != c.EAGAIN:
                raise Exception("iommu dma map failed, errno: %x (whereas EAGAIN is %x" % (e, c.EAGAIN))
            res = c.ioctl(self.container, c.VFIO_IOMMU_MAP_DMA, c.byref(dma_map))
            e = c.errno.value

        print "[+] mapped page sz %d at vaddr %x paddr %x for dma" % (page_sz, page, dma_map.iova)

        return page, page_sz
