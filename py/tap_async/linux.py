'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016 Saul St. John

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

from contextlib import closing
from ctypes import addressof
import fcntl
import logging
import os
import socket
import struct
import sys
import termios
import time

logger = logging.getLogger(__name__)

import clib as c
from tunlib import (IFF_TAP, IFF_NO_PI, TUNSETIFF)

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
        logger.info("tap device name: \"%s\"" % self.tap_name)
        self.tfd = fd
        self.confd = sys.stdin.fileno()
        try:
            self.efd = self.dev.interface.eventfd
            self._wait_for_interrupt = self.__wait_on_eventfd
            logger.debug("eventfd available")
        except:
            logger.warn("eventfd unavailable")
        return self

    def __exit__(self):
        if self._connected:
            self._set_tapdev_status(False)
        os.close(self.tfd)
    
    def _wait_for_keypress(self):
        if not self.running:
            return
        orig_term = termios.tcgetattr(self.confd)
        new_term = orig_term[:]
        new_term[3] &= ~(termios.ICANON | termios.ECHO)
        termios.tcsetattr(self.confd, termios.TCSANOW, new_term)
        try:
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(self.confd, termios.TCSANOW, orig_term)

    def _set_tapdev_status(self, connected):
        if self._connected == connected:
            return
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
        logger.info("tapdev is now %s" % "up" if connected else "down")
        self._connected = connected

    def __wait_on_eventfd(self):
        _ = os.read(self.efd, 8)

    def _get_tap_packet(self, buf, buf_len):
        l = c.read(self.tfd, buf, buf_len)
        return (buf, l)

    def _put_tap_packet(self, pkt):
        return os.write(self.tfd, pkt)
