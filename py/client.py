#!/usr/bin/python

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

import argparse
import socket
from fcntl import ioctl
from struct import pack, unpack

from clib import SIOCGIFHWADDR

class Client(object):
    def __init__(self, iface):
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x88b5))
        info = ioctl(s.fileno(), SIOCGIFHWADDR, pack('256s', iface[:15]))
        self.local_mac = info[18:24]
        print "local if mac is %s" % ':'.join(["%02x" % ord(i) for i in self.local_mac])

        s.bind((iface, 0))
        self.s = s

    def send(self, payload, src = None,
            dst = '\xff\xff\xff\xff\xff\xff', etype = "\x88\xb5"):

        if src == None:
            src = self.local_mac

        pkt = dst+src+etype+payload
        if len(pkt) < 80:
            pkt += ('\x00' * (80 - len(pkt)))
        self.s.send(pkt)

    def run(self, cmd, args):
        print "sending ping..."
        test_pkt = '\x00\x01'
        self.send(test_pkt)
        while True:
            resp = self.s.recv(128)
            if resp[12:14] == '\x88\xb5' and resp[14:16] == '\x80\x01':
                break

        remote_mac = resp[6:12]
        print "found thundergate at %s" % ":".join(["%02x" % ord(i) for i in remote_mac]) 

        if cmd > 1:
            pkt = pack(">H", cmd)
            for a in args:
                pkt += pack(">I", a)

            print "sending cmd type 0x%04x" % cmd
            self.send(pkt, dst=remote_mac)
            while True:
                resp = self.s.recv(128)
                if resp[12:14] == '\x88\xb5' and unpack(">H", resp[14:16])[0] == (0x8000 | cmd):
                    break
            print "response recvd: %s" % ''.join(["%02x" % ord(i) for i in resp[16:]])

def auto_int(x):
   return int(x, 0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='tg client')
    parser.add_argument('iface')
    parser.add_argument('cmd', nargs='?', type=auto_int, default=0)
    parser.add_argument('args', nargs='*', type=auto_int, default=[])
    args = parser.parse_args()
    Client(args.iface).run(args.cmd, args.args)
