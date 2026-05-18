#!/usr/bin/env python3
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

# leechbridge.py -- expose a ThunderGate NIC's host-memory DMA to
# LeechCore / MemProcFS.
#
# ThunderGate's control protocol (raw Ethernet, EtherType 0x88b5) needs
# AF_PACKET, so this daemon runs on a Linux host on the same segment as
# the target's NIC. LeechCore -- typically elsewhere, e.g. an Apple
# Silicon Mac -- reaches it through the companion C plugin
# (leechcore_device_thundergate) over the TCP protocol below.
#
#   request  -- 16 bytes, little-endian:
#       op:u8  flags:u8  pad:u16  addr:u64  len:u32
#       op 0 READ, 1 WRITE, 2 INFO; a WRITE appends `len` data bytes.
#       flags and pad are reserved -- send 0.
#   response -- little-endian:
#       READ   ok:u8 followed by exactly `len` bytes (zeroed on failure)
#       WRITE  ok:u8
#       INFO   ok:u8 followed by max_address:u64
#   ok is 1 on success, 0 on failure.

import argparse
import os
import socket
import struct
import sys

# leechbridge.py lives in py/ next to client.py -- make that import work
# no matter what directory the daemon is launched from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from client import ThunderGateInterface

OP_READ, OP_WRITE, OP_INFO = 0, 1, 2
_REQ = struct.Struct("<BBHQI")          # op, flags, pad, addr, len
MAX_XFER = 16 * 1024 * 1024             # cap one transfer (len is untrusted)


def _recv_exact(conn, n):
    buf = b''
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def _serve(conn, tg, max_address):
    while True:
        hdr = _recv_exact(conn, _REQ.size)
        if hdr is None:
            return
        op, _flags, _pad, addr, length = _REQ.unpack(hdr)

        if op not in (OP_READ, OP_WRITE, OP_INFO):
            sys.stderr.write("unknown op %d\n" % op)
            return

        # addr/length come straight off an untrusted socket: bound them
        # before allocating a buffer or relaying anything to the target.
        if op != OP_INFO:
            if length == 0 or length > MAX_XFER:
                sys.stderr.write("rejecting %#x-byte transfer\n" % length)
                return
            if addr + length > max_address:
                sys.stderr.write("rejecting out-of-range %#x+%#x\n"
                                 % (addr, length))
                return

        if op == OP_READ:
            try:
                data = tg.read(addr, length)
            except Exception as e:
                sys.stderr.write("read %#x+%#x failed: %s\n" % (addr, length, e))
                data = b''
            # always reply status + exactly `length` bytes so the stream
            # stays framed; a short or over-long read counts as failure.
            ok = len(data) >= length
            data = data[:length].ljust(length, b'\x00')
            conn.sendall((b'\x01' if ok else b'\x00') + data)

        elif op == OP_WRITE:
            data = _recv_exact(conn, length)
            if data is None:
                return
            try:
                tg.write(addr, data)
                conn.sendall(b'\x01')
            except Exception as e:
                sys.stderr.write("write %#x+%#x failed: %s\n" % (addr, length, e))
                conn.sendall(b'\x00')

        elif op == OP_INFO:
            conn.sendall(b'\x01' + struct.pack("<Q", max_address))


def main():
    ap = argparse.ArgumentParser(
        description="bridge a ThunderGate NIC to LeechCore / MemProcFS")
    ap.add_argument("iface", help="network interface on the target's segment")
    ap.add_argument("--listen", default="127.0.0.1:28473",
                    help="host:port to listen on. This exposes unauthenticated "
                         "arbitrary host physical-memory read/write -- keep it "
                         "on loopback or a trusted segment (default %(default)s)")
    ap.add_argument("--size", default="0x200000000",
                    help="target physical address span (default 8 GiB)")
    args = ap.parse_args()

    if ":" not in args.listen:
        ap.error("--listen must be host:port")
    host, _, port = args.listen.rpartition(":")
    host = host.strip("[]")
    max_address = int(args.size, 0)

    tg = ThunderGateInterface(args.iface)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, int(port)))
    srv.listen(1)
    print("leechbridge: listening on %s:%s, target span %#x"
          % (host, port, max_address))

    try:
        while True:
            conn, peer = srv.accept()
            print("leechbridge: leechcore connected from %s:%d" % peer)
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            conn.settimeout(300)        # a stalled peer must not wedge us
            try:
                _serve(conn, tg, max_address)
            except (ConnectionError, OSError) as e:
                print("leechbridge: connection error: %s" % e)
            finally:
                conn.close()
                print("leechbridge: leechcore disconnected")
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        tg.close()


if __name__ == "__main__":
    main()
