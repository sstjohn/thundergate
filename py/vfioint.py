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
from fcntl import ioctl
import clib as c
import struct
import iomem

class VfioInterface(object):
    def __init__(self, bdf):
        self.bdf = bdf
        tmp = os.readlink("/sys/bus/pci/devices/%s/iommu_group" % bdf)
        self.groupno = int(tmp.split('/')[-1])

    def _dev_close(self):
        c.munmap(self.bar0, self.bar0_sz)
        os.close(self.device)
        ioctl(self.group, c.VFIO_GROUP_UNSET_CONTAINER, struct.pack("I", self.container))
        os.close(self.group)
    
    def __exit__(self, t, v, traceback):
        self._dev_close()
        os.close(self.container)

    def show_irqs(self):
        device_info = c.vfio_device_info()
        device_info.argsz = c.sizeof(c.vfio_device_info)
        ioctl(self.device, c.VFIO_DEVICE_GET_INFO, device_info)

        print "[+] enumerating vfio device irqs"
        for i in range(device_info.num_irqs - 1):
            irq = c.vfio_irq_info()
            irq.argsz = c.sizeof(c.vfio_irq_info)
            irq.index = i
            ioctl(self.device, c.VFIO_DEVICE_GET_IRQ_INFO, irq)

            print "[*] irq %d: count %x, flags %x" % (i, irq.count, irq.flags)

    def reattach(self):
        self._dev_close()
        self._dev_open()

    def __enter__(self):
        print "[+] opening vfio container"
        container = os.open("/dev/vfio/vfio", os.O_RDWR)

        if ioctl(container, c.VFIO_GET_API_VERSION) != c.VFIO_API_VERSION:
            raise Exception("wrong vfio api version")

        if not ioctl(container, c.VFIO_CHECK_EXTENSION, c.VFIO_TYPE1_IOMMU):
            raise Exception("vfio type 1 iommu not supported")

        self.container = container

        self.mm = iomem.IOMemMgr(container)
        self._dev_open()

    def _dev_open(self):
        print "[+] opening vfio group"
        group = os.open("/dev/vfio/%d" % self.groupno, os.O_RDWR)

        group_status = c.vfio_group_status()
        group_status.argsz = c.sizeof(c.vfio_group_status)
        ioctl(group, c.VFIO_GROUP_GET_STATUS, group_status)
        if not (group_status.flags & c.VFIO_GROUP_FLAGS_VIABLE):
            raise Exception("vfio group %d is not viable" % self.groupno)

        self.group = group

        ioctl(group, c.VFIO_GROUP_SET_CONTAINER, struct.pack("I", self.container))

        ioctl(self.container, c.VFIO_SET_IOMMU, c.VFIO_TYPE1_IOMMU)

        iommu_info = c.vfio_iommu_type1_info()
        iommu_info.argsz = c.sizeof(c.vfio_iommu_type1_info)
        ioctl(self.container, c.VFIO_IOMMU_GET_INFO, iommu_info)

        self.iommu_info = iommu_info

        print "[+] opening vfio device"
        device = c.ioctl(group, c.VFIO_GROUP_GET_DEVICE_FD, self.bdf)
        self.device = device

        device_info = c.vfio_device_info()
        device_info.argsz = c.sizeof(c.vfio_device_info)
        ioctl(device, c.VFIO_DEVICE_GET_INFO, device_info)

        print "[+] enumerating vfio device regions"
        self.regions = []
        for i in range(device_info.num_regions - 1):
            r = c.vfio_region_info()
            r.argsz = c.sizeof(c.vfio_region_info)
            r.index = i

            ioctl(device, c.VFIO_DEVICE_GET_REGION_INFO, r)

            self.regions += [r]
            flags = ""
            if r.flags & c.VFIO_REGION_INFO_FLAG_READ:
                flags += "R"

            if r.flags & c.VFIO_REGION_INFO_FLAG_WRITE:
                flags += "W"

            if r.flags & c.VFIO_REGION_INFO_FLAG_MMAP:
                flags += "M"

            t = "region %d" % r.index
            if i == c.VFIO_PCI_BAR0_REGION_INDEX:
                bar0 = c.mmap(0, r.size, c.PROT_READ | c.PROT_WRITE, c.MAP_SHARED | c.MAP_LOCKED, device, r.offset)
                self.bar0 = bar0
                self.bar0_sz = r.size
                t = "pci bar 0"
            elif i == c.VFIO_PCI_CONFIG_REGION_INDEX:
                self.config_offset = r.offset
                t = "pci config"
            print "[*] %s [%s]: size %04x, ofs %x, resv %x" % (t, flags, r.size, r.offset, r.resv)

        self.show_irqs()

        print "[+] enabling msi-x"
        irq_set = c.vfio_irq_set()
        c.resize(irq_set, c.sizeof(c.vfio_irq_set) + c.sizeof(c.c_uint))
        irq_set.argsz = c.sizeof(c.vfio_irq_set) + c.sizeof(c.c_uint)
        irq_set.index = c.VFIO_PCI_MSIX_IRQ_INDEX
        irq_set.start = 0
        irq_set.count = 1
        irq_set.flags = c.VFIO_IRQ_SET_DATA_EVENTFD | c.VFIO_IRQ_SET_ACTION_TRIGGER

        self.eventfd = c.eventfd(0, 0)
        c.cast(c.addressof(irq_set.data), c.POINTER(c.c_uint))[0] = self.eventfd

        ioctl(self.device, c.VFIO_DEVICE_SET_IRQS, irq_set)

    def cfg_read(self, offset):
        assert offset >= 0 and offset < 0x400
        buf = c.create_string_buffer(4)
        c.pread(self.device, buf, 4, self.config_offset + offset)
        return struct.unpack("I", buf)[0]

    def cfg_write(self, offset, val):
        assert offset >= 0 and offset < 0x400
        buf = c.create_string_buffer(struct.pack("I", val))
        c.pwrite(self.device, buf, 4, self.config_offset + offset)
