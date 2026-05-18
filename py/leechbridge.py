#!/usr/bin/env python3
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
#   response -- little-endian:
#       READ   ok:u8 followed by exactly `len` bytes (zeroed on failure)
#       WRITE  ok:u8
#       INFO   ok:u8 followed by max_address:u64
#   ok is 1 on success, 0 on failure.

import argparse
import socket
import struct
import sys

from client import ThunderGateInterface

OP_READ, OP_WRITE, OP_INFO = 0, 1, 2
_REQ = struct.Struct("<BBHQI")          # op, flags, pad, addr, len


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

        if op == OP_READ:
            try:
                data = tg.read(addr, length)
            except Exception as e:
                sys.stderr.write("read %#x+%#x failed: %s\n" % (addr, length, e))
                data = b''
            if len(data) == length:
                conn.sendall(b'\x01' + data)
            else:
                # keep the stream framed: always status + `length` bytes
                conn.sendall(b'\x00' + b'\x00' * length)

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

        else:
            sys.stderr.write("unknown op %d\n" % op)
            return


def main():
    ap = argparse.ArgumentParser(
        description="bridge a ThunderGate NIC to LeechCore / MemProcFS")
    ap.add_argument("iface", help="network interface on the target's segment")
    ap.add_argument("--listen", default="0.0.0.0:28473",
                    help="host:port for the LeechCore plugin (default %(default)s)")
    ap.add_argument("--size", default="0x200000000",
                    help="target physical address span (default 8 GiB)")
    args = ap.parse_args()

    host, _, port = args.listen.rpartition(":")
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
