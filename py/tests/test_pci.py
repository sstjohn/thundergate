'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2026  Saul St. John

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

# Tests for pci.Config - PCI capability-list enumeration - exercised against
# the in-memory MockInterface (no hardware).

import unittest

import pci
from tests.mock import MockInterface


class TestPciConfig(unittest.TestCase):
    def test_no_capabilities(self):
        # A zeroed config space: the capability pointer at 0x34 is 0.
        cfg = pci.Config(MockInterface())
        self.assertEqual(cfg.caps, {})

    def test_msix_capability(self):
        iface = MockInterface()
        # capability pointer (0x34) -> 0x40
        iface.cfg_write(0x34, 0x40)
        # capability at 0x40: id 0x11 (MSI-X), next pointer 0 (end of list)
        iface.cfg_write(0x40, (0x00 << 8) | 0x11)
        cfg = pci.Config(iface)
        self.assertIn('msix', cfg.caps)

    def test_capability_chain(self):
        iface = MockInterface()
        iface.cfg_write(0x34, 0x40)
        # 0x40: MSI-X (0x11), next -> 0x50
        iface.cfg_write(0x40, (0x50 << 8) | 0x11)
        # 0x50: an unknown capability (0x05 = MSI), next -> 0 (end)
        iface.cfg_write(0x50, (0x00 << 8) | 0x05)
        cfg = pci.Config(iface)
        self.assertIn('msix', cfg.caps)


if __name__ == '__main__':
    unittest.main()
