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

# MockInterface - an in-memory stand-in for a hardware device interface,
# for hardware-free testing of the Python toolkit.
#
# It satisfies the same contract device.py and pci.py expect of the real
# vfio/sysfs/win interfaces: an integer `bar0` address backed by a real
# buffer, and config-space read/write over a bytearray. No hardware, no
# kernel driver, no Linux.

import ctypes


class MockInterface(object):
    def __init__(self, bar0_size=0x10000, config_size=0x1000):
        # A real ctypes buffer so `bar0` is a usable integer address that
        # device.py can cast register structures onto.
        self._bar0_buf = (ctypes.c_char * bar0_size)()
        self.bar0 = ctypes.addressof(self._bar0_buf)
        self.bar0_sz = bar0_size
        self._config = bytearray(config_size)
        self.mm = None

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        return False

    def reattach(self):
        pass

    def cfg_read(self, offset):
        assert 0 <= offset < len(self._config) - 3
        return int.from_bytes(self._config[offset:offset + 4], 'little')

    def cfg_write(self, offset, val):
        assert 0 <= offset < len(self._config) - 3
        self._config[offset:offset + 4] = int(val & 0xffffffff).to_bytes(4, 'little')
