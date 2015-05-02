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

class Client(object):
    def __init__(self, iface):
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 0x88b5)
        s.bind((iface, 0))
        self.s = s

    def send(self, payload, src = '\x00\x00\x00\x00\x00\x00', 
            dst = '\xff\xff\xff\xff\xff\xff', etype = "\x88\xb5"):
        pkt = dst+src+etype+payload
        if len(pkt) < 64:
            pkt += ('\x00' * (64 - len(pkt)))
        self.s.send(pkt)

    def run(self):
        print "Sending test packet"
        test_pkt = '\xa5\xa5' * 25
        self.send(test_pkt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='tg client')
    parser.add_argument('iface')
    args = parser.parse_args()
    Client(args.iface).run()
