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
import socket
from contextlib import closing

class TapLinuxInterface(object):
    def __init__(self, dev):
        self.dev = dev
        self.mm = dev.interface.mm
        self.serial = 0
        self._key = ''
        self._connected = False

    def __enter__(self):
        fd = os.open("/dev/net/tun", os.O_RDWR)
        ifr = struct.pack('16sH', "", IFF_TAP | IFF_NO_PI)
        self.tap_name = struct.unpack('16sH', fcntl.ioctl(fd, TUNSETIFF, ifr))[0]
        print "[+] tap device name: \"%s\"" % self.tap_name
        self.tfd = fd
        self.confd = sys.stdin.fileno()
        self.read_fds = [self.dev.interface.eventfd, self.tfd, self.confd]
        self.ready = []
        return self

    def __exit__(self):
        if self._connected:
            self._set_tapdev_status(False)
        os.close(self.tfd)

    def _wait_for_something(self):
        old_con_settings = termios.tcgetattr(self.confd)
        try:
            tty.setraw(self.confd)
            self.ready, _, _ = select.select(self.read_fds, [], [])
            if self.dev.interface.eventfd in self.ready:
                return 1
            if self.tfd in self.ready:
                return 2
            if self.confd in self.ready:
                self._key = sys.stdin.read(1)
                return 0
        finally:
            termios.tcsetattr(self.confd, termios.TCSADRAIN, old_con_settings)

    def _get_serial(self):
        self.serial += struct.unpack("L", os.read(self.dev.interface.eventfd, 8))[0]
        return self.serial

    def _get_packet(self):
        b = self.mm.alloc(0x800)
        l = c.read(self.tfd, b, 0x800)
        return (b, l)

    def _get_key(self):
        return self._key

    def _write_pkt(self, pkt, length):
        os.write(self.tfd, pkt)
        self.mm.free(pkt)

    def _set_tapdev_status(self, connected):
        with closing(socket.socket()) as s:
           ifr = struct.pack('16sH', self.tap_name, 0)
           r = fcntl.ioctl(s, c.SIOCGIFFLAGS, ifr)
           flags = struct.unpack('16sH', r)[1]

           if connected:
               flags |= c.IFF_UP
           else:
               flags &= ~c.IFF_UP

           ifr = struct.pack('16sH', self.tap_name, flags)
           fcntl.ioctl(s, c.SIOCSIFFLAGS, ifr)
        self._connected = connected
    
            
