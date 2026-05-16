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

# Tests for cabi.py - the hand-written libc / VFIO ABI module. These pin the
# VFIO ioctl encodings and struct layouts so a future edit cannot silently
# drift from the kernel ABI.

import ctypes
import unittest

import cabi


class TestVfioIoctls(unittest.TestCase):
    def test_io_encoding(self):
        # _IO(type, nr) = (type << 8) | nr   -- direction and size are zero.
        base = (ord(';') << 8) | 100
        self.assertEqual(cabi.VFIO_GET_API_VERSION, base + 0)
        self.assertEqual(cabi.VFIO_CHECK_EXTENSION, base + 1)
        self.assertEqual(cabi.VFIO_GROUP_GET_DEVICE_FD, base + 6)
        self.assertEqual(cabi.VFIO_DEVICE_SET_IRQS, base + 10)
        self.assertEqual(cabi.VFIO_IOMMU_MAP_DMA, base + 13)

    def test_indices(self):
        self.assertEqual(cabi.VFIO_PCI_BAR0_REGION_INDEX, 0)
        self.assertEqual(cabi.VFIO_PCI_CONFIG_REGION_INDEX, 7)
        self.assertEqual(cabi.VFIO_PCI_MSIX_IRQ_INDEX, 2)


class TestVfioStructs(unittest.TestCase):
    def test_sizes(self):
        # Byte-exact against linux/vfio.h.
        self.assertEqual(ctypes.sizeof(cabi.vfio_group_status), 8)
        self.assertEqual(ctypes.sizeof(cabi.vfio_device_info), 16)
        self.assertEqual(ctypes.sizeof(cabi.vfio_region_info), 32)
        self.assertEqual(ctypes.sizeof(cabi.vfio_irq_info), 16)
        self.assertEqual(ctypes.sizeof(cabi.vfio_iommu_type1_info), 16)
        self.assertEqual(ctypes.sizeof(cabi.vfio_iommu_type1_dma_map), 32)

    def test_irq_set_flexible_array(self):
        # vfio_irq_set ends in a flexible 'data' member; callers resize the
        # instance to append an eventfd descriptor after 'count'.
        self.assertEqual(ctypes.sizeof(cabi.vfio_irq_set), 20)
        s = cabi.vfio_irq_set()
        ctypes.resize(s, ctypes.sizeof(cabi.vfio_irq_set) + ctypes.sizeof(ctypes.c_uint))
        self.assertGreaterEqual(ctypes.sizeof(s), 24)
        # the 'data' field begins right after the five u32 header fields
        self.assertEqual(ctypes.addressof(s.data) - ctypes.addressof(s), 20)


class TestConstants(unittest.TestCase):
    def test_map_failed(self):
        self.assertEqual(cabi.MAP_FAILED, ctypes.c_void_p(-1).value)

    def test_flag_bits(self):
        self.assertEqual(cabi.VFIO_IRQ_SET_DATA_EVENTFD, 1 << 2)
        self.assertEqual(cabi.VFIO_IRQ_SET_ACTION_TRIGGER, 1 << 5)
        self.assertEqual(cabi.VFIO_DMA_MAP_FLAG_READ | cabi.VFIO_DMA_MAP_FLAG_WRITE, 3)


if __name__ == '__main__':
    unittest.main()
