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

import struct
import select
import os
import clib as c
import fcntl
from tunlib import *

class TapLinuxInterface(object):
    def __init__(self, dev):
        self.dev = dev
        self.mm = dev.interface.mm

    def __enter__(self):
        fd = os.open("/dev/net/tun", os.O_RDWR)
        ifr = struct.pack('16sH', 'tap0', IFF_TAP | IFF_NO_PI)
        fcntl.ioctl(fd, TUNSETIFF, ifr)
        self.tfd = fd
        self.read_fds = [self.dev.interface.eventfd, self.tfd]
        self.ready = []
        return self

    def __exit__(self):
        os.close(self.tfd)

    def _tg_is_ready(self):
        return (self.dev.interface.eventfd in self.ready) 

    def _tap_is_ready(self):
        return (self.tfd in self.ready)

    def _wait_for_something(self):
        self.ready, _, _ = select.select(self.read_fds, [], [])

    def _get_serial(self):
        return struct.unpack("L", os.read(self.dev.interface.eventfd, 8))

    def _get_packet(self):
        b = self.mm.alloc(0x800)
        l = c.read(self.tfd, b, 0x800)
        return (b, l)

    def _write_pkt(self, pkt, length):
        os.write(self.tfd, pkt)

    def _set_tapdev_status(self, connected):
        pass
