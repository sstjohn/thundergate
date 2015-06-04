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

def get_bytes_strs(a):
    try:
        return ["%02x" % o for o in a]
    except:
        return ["%02x" % ord(o) for o in a]

class ThunderGateInterface:
    def __init__(self, iface):
        self._socket_setup(iface)
        self._find_gate()

    def _socket_setup(self, iface):
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x88b5))
        info = ioctl(s.fileno(), SIOCGIFHWADDR, pack('256s', iface[:15].encode('utf-8')))
        self._local_mac = info[18:24]
        print("local if mac is %s" % ':'.join(get_bytes_strs(self._local_mac)))
        
        s.bind((iface, 0))
        self._socket = s

    def _find_gate(self):
        print("sending ping...")
        self._send_cmd(1)
        resp = self._recv_resp()
        self._tg_mac = resp[6:12]
        print("found thundergate at %s" % ":".join(get_bytes_strs((self._tg_mac))))

    def _send_pkt(self, payload, src = None,
            dst = None, etype = b"\x88\xb5"):

        if src == None:
            src = self._local_mac

        if dst == None:
            try:
                dst = self._tg_mac
            except:
                dst = b'\xff' * 6

        pkt = dst+src+etype+payload
        if len(pkt) < 80:
            pkt += (b'\x00' * (80 - len(pkt)))
        self._socket.send(pkt)

    def _send_cmd(self, cmd, args = [], src = None, dst = None,
                etype = b"\x88\xb5"):
        payload = pack(">H", cmd)
        for a in args:
            payload += pack(">I", a)
        self._send_pkt(payload, src, dst, etype)
        self._last_cmd = cmd

    def _recv_resp(self, cmd_t = None, tg_mac = None):
        if tg_mac == None:
            try: tg_mac = self._tg_mac
            except: pass
        
        if tg_mac == b'\xff' * 6:
            tg_mac = None

        if cmd_t == None:
            try: cmd_t = self._last_cmd
            except: pass

        if cmd_t != None:
            cmd_t |= 0x8000

        while True:
            resp = self._socket.recv(128)
            if resp[12:14] == b'\x88\xb5':
                if tg_mac != None and resp[6:12] != tg_mac:
                    continue
                if cmd_t != None and unpack(">H", resp[14:16])[0] != cmd_t:
                    continue
                break

        return resp

    def read(self, addr, numb, buf=None):
        addr_hi = addr >> 32
        addr_lo = addr & 0xffffffff
        args = [addr_hi, addr_lo, numb]
        self._send_cmd(4, args)
        r = self._recv_resp()
        return r[16:]
    
    def readv(self, req):
        for r in req:
            yield (r[0], self.read(r[0], r[1]))
    
    def close(self):
        pass

def client_main(gate, cmd, args):
    if cmd > 1:
        print("sending cmd type 0x%04x" % cmd)
        gate._send_cmd(cmd, args)
        resp = gate._recv_resp()
        print("response recvd: %s" % ''.join(get_bytes_strs(resp[16:])))

def auto_int(x):
   return int(x, 0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='tg client')
    parser.add_argument('iface')
    parser.add_argument('cmd', nargs='?', type=auto_int, default=0)
    parser.add_argument('args', nargs='*', type=auto_int, default=[])
    args = parser.parse_args()
    client_main(ThunderGateInterface(args.iface), args.cmd, args.args)
