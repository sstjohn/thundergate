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
import tty
import sys
import termios

class TapLinuxInterface(object):
    def __init__(self, dev):
        self.dev = dev
        self.mm = dev.interface.mm
        self.serial = 0

    def __enter__(self):
        fd = os.open("/dev/net/tun", os.O_RDWR)
        ifr = struct.pack('16sH', "", IFF_TAP | IFF_NO_PI)
        self.tap_name = struct.unpack('16sH', fcntl.ioctl(fd, TUNSETIFF, ifr))[0]
        self.tfd = fd
        self.confd = sys.stdin.fileno()
        self._old_con_settings = termios.tcgetattr(self.confd)
        tty.setraw(self.confd)
        self.read_fds = [self.dev.interface.eventfd, self.tfd, self.confd]
        self.ready = []
        return self

    def __exit__(self):
        termios.tcsetattr(self.confd, termios.TCSADRAIN, self._old_con_settings)
        os.close(self.tfd)

    def _wait_for_something(self):
        self.ready, _, _ = select.select(self.read_fds, [], [])
        if self.dev.interface.eventfd in self.ready:
            return 0
        if self.tfd in self.ready:
            return 1
        if self.confd in self.ready:
            return 2

    def _get_serial(self):
        self.serial += struct.unpack("L", os.read(self.dev.interface.eventfd, 8))
        return self.serial

    def _get_packet(self):
        b = self.mm.alloc(0x800)
        l = c.read(self.tfd, b, 0x800)
        return (b, l)

    def _get_key(self):
        return sys.stdin.read(1)

    def _write_pkt(self, pkt, length):
        os.write(self.tfd, pkt)

    def _set_tapdev_status(self, connected):
       ifr = struct.pack('16sH', self.tap_name, 0)
       flags = struct.unpack('16sH', fcntl.ioctl(self.tfd, SIOCGIFFLAGS, ifr))[1]
       
       if connected:
           flags |= IFF_UP
       else:
           flags &= ~IFF_UP

       ifr = struct.pack('16sH', self.tap_name, flags)
       fcntl.ioctl(self.tfd, SIOCSIFFLAGS, ifreq)
            
