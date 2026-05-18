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

# macOS host-side TAP backend for the _aiotap driver.
#
# The NIC itself is reached through the PCIDriverKit dext (see
# py/interfaces/macos.py); this module is only the *host* end, presenting
# the Tigon3's traffic to the macOS network stack. macOS has no
# /dev/net/tun, and utun / NetworkExtension are L3-only -- so an Ethernet
# tap is built from a pair of peered "feth" fake-ethernet interfaces: the
# host stack uses one end, this driver owns the other through a BPF socket
# (receive) and a PF_NDRV socket (transmit).
#
# HARDWARE-UNVERIFIED: the BPF/NDRV constants are taken from the macOS SDK
# headers (net/bpf.h, sys/ioccom.h) and the XNU sockaddr_ndrv layout; the
# feth plumbing wants checking on a Mac with the dext loaded.

import ctypes
import fcntl
import logging
import os
import struct
import subprocess
import sys
import termios

logger = logging.getLogger(__name__)

# ioctl encoding -- sys/ioccom.h
_IOC_VOID = 0x20000000
_IOC_OUT = 0x40000000
_IOC_IN = 0x80000000
_IOCPARM_MASK = 0x1fff


def _ioc(inout, group, num, length):
    return inout | ((length & _IOCPARM_MASK) << 16) | (ord(group) << 8) | num


# BPF ioctls -- net/bpf.h. struct ifreq is 32 bytes; u_int is 4.
BIOCGBLEN = _ioc(_IOC_OUT, 'B', 102, 4)
BIOCPROMISC = _ioc(_IOC_VOID, 'B', 105, 0)
BIOCSETIF = _ioc(_IOC_IN, 'B', 108, 32)
BIOCIMMEDIATE = _ioc(_IOC_IN, 'B', 112, 4)

# bpf_hdr -- net/bpf.h, LP64: a 16-byte timeval, then bh_caplen (u32) at
# offset 16, bh_datalen (u32), bh_hdrlen (u16) at offset 24. A read()
# yields one or more records; the frame starts bh_hdrlen into the record,
# and the next record is 4-byte aligned after bh_hdrlen + bh_caplen.
_BPF_CAPLEN = 16
_BPF_HDRLEN = 24

AF_NDRV = 27       # net/if_ndrv.h
SOCK_RAW = 3

_libc = ctypes.CDLL(None, use_errno=True)
_libc.socket.restype = _libc.bind.restype = _libc.connect.restype = ctypes.c_int
_libc.socket.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
_libc.bind.argtypes = _libc.connect.argtypes = \
    [ctypes.c_int, ctypes.c_void_p, ctypes.c_uint32]


def _wordalign(x):
    return (x + 3) & ~3


def _ifconfig(*args):
    subprocess.run(("ifconfig",) + args, check=True, capture_output=True)


def _create_feth_pair():
    '''Clone two feth interfaces, peer them, bring both up. Returns
    (host_end, driver_end) -- the operator configures the host end.'''
    pair = []
    for _ in range(2):
        out = subprocess.run(("ifconfig", "feth", "create"), check=True,
                             capture_output=True, text=True)
        pair.append(out.stdout.strip())
    host, nic = pair
    _ifconfig(host, "peer", nic)
    _ifconfig(host, "up")
    _ifconfig(nic, "up")
    return host, nic


def _open_bpf(ifname):
    '''Open a /dev/bpf device bound to ifname in immediate, promiscuous
    mode. Returns (fd, kernel_read_buffer_length).'''
    for i in range(256):
        try:
            fd = os.open("/dev/bpf%d" % i, os.O_RDWR)
            break
        except OSError:
            continue
    else:
        raise OSError("no free /dev/bpf device")
    fcntl.ioctl(fd, BIOCSETIF, ifname.encode().ljust(32, b'\0'))
    fcntl.ioctl(fd, BIOCIMMEDIATE, struct.pack("I", 1))
    fcntl.ioctl(fd, BIOCPROMISC, 0)
    blen = struct.unpack("I", fcntl.ioctl(fd, BIOCGBLEN,
                                          struct.pack("I", 0)))[0]
    return fd, blen


def _open_ndrv(ifname):
    '''Open a PF_NDRV socket bound and connected to ifname for L2 frame
    injection. Returns a raw fd.'''
    fd = _libc.socket(AF_NDRV, SOCK_RAW, 0)
    if fd < 0:
        raise OSError(ctypes.get_errno(), "PF_NDRV socket")
    # struct sockaddr_ndrv { u8 snd_len; u8 snd_family; u8 snd_name[16]; }
    sa = struct.pack("BB16s", 18, AF_NDRV, ifname.encode())
    for op in (_libc.bind, _libc.connect):
        if op(fd, sa, len(sa)) < 0:
            err = ctypes.get_errno()
            os.close(fd)
            raise OSError(err, "PF_NDRV %s" % op.__name__)
    return fd


class TapMacInterface(object):
    '''The host (feth) end of the _aiotap driver on macOS.'''

    def __init__(self, dev):
        self.dev = dev
        self.mm = dev.interface.mm
        self.serial = 0
        self._key = ''
        self._connected = False
        self._rxq = []

    def __enter__(self):
        self.confd = sys.stdin.fileno()
        self.host_feth, self.nic_feth = _create_feth_pair()
        logger.info("feth pair up -- configure the host stack on %s; "
                    "the driver holds %s", self.host_feth, self.nic_feth)
        self.bpf_fd, self.bpf_blen = _open_bpf(self.nic_feth)
        self.ndrv_fd = _open_ndrv(self.nic_feth)
        self._wait_for_interrupt = self._wait_on_dext_interrupt
        return self

    def __exit__(self):
        os.close(self.bpf_fd)
        os.close(self.ndrv_fd)
        for feth in (self.host_feth, self.nic_feth):
            try:
                _ifconfig(feth, "destroy")
            except subprocess.CalledProcessError:
                logger.warning("could not destroy %s", feth)

    def _wait_for_keypress(self):
        if not self.running:
            return
        orig = termios.tcgetattr(self.confd)
        raw = orig[:]
        raw[3] &= ~(termios.ICANON | termios.ECHO)
        termios.tcsetattr(self.confd, termios.TCSANOW, raw)
        try:
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(self.confd, termios.TCSANOW, orig)

    def _wait_on_dext_interrupt(self):
        self.dev.interface.wait_interrupt()

    def _get_tap_packet(self, buf, buf_len):
        '''Block for one Ethernet frame from the host and copy it into the
        DMA buffer at address buf. Returns (buf, length).'''
        while not self._rxq:
            data = os.read(self.bpf_fd, self.bpf_blen)
            off = 0
            while off + _BPF_HDRLEN + 2 <= len(data):
                caplen = struct.unpack_from("I", data, off + _BPF_CAPLEN)[0]
                hdrlen = struct.unpack_from("H", data, off + _BPF_HDRLEN)[0]
                self._rxq.append(data[off + hdrlen:off + hdrlen + caplen])
                off = _wordalign(off + hdrlen + caplen)
        frame = self._rxq.pop(0)
        n = min(len(frame), buf_len)
        ctypes.memmove(buf, frame, n)
        return (buf, n)

    def _put_tap_packet(self, pkt):
        '''Inject an Ethernet frame the NIC received onto the host stack.'''
        os.write(self.ndrv_fd, pkt)
