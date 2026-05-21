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
import select
import struct
import subprocess
import sys
import termios
import time

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
BIOCSSEESENT = _ioc(_IOC_IN, 'B', 119, 4)

# bpf_hdr -- net/bpf.h. On LP64, BPF_TIMEVAL is timeval32 (8 bytes), so
# bh_caplen (u32) sits at offset 8 and bh_hdrlen (u16) at offset 16. A
# read() yields one or more records; the frame starts bh_hdrlen into the
# record, and the next record is 4-byte aligned after bh_hdrlen + caplen.
_BPF_CAPLEN = 8
_BPF_HDRLEN = 16

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
    # See-sent off. _put_tap_packet injects NIC-received frames onto this
    # same feth with PF_NDRV; with see-sent on, BPF replays those
    # injections and tap_watcher loops every receive straight back out.
    fcntl.ioctl(fd, BIOCSSEESENT, struct.pack("I", 0))
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
        self._inject_selftest()
        self._wait_for_interrupt = self._wait_on_dext_interrupt
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.close(self.bpf_fd)
        os.close(self.ndrv_fd)
        for feth in (self.host_feth, self.nic_feth):
            try:
                _ifconfig(feth, "destroy")
            except subprocess.CalledProcessError:
                logger.warning("could not destroy %s", feth)
        return False

    def _inject_selftest(self):
        '''Write a throwaway frame to our own NDRV socket and confirm it
        lands on the host feth. The whole receive path ends in this hop;
        if it is wedged, every frame the NIC delivers is lost in silence
        -- so check it once, loudly, before the driver runs deaf.'''
        probe_fd, probe_blen = _open_bpf(self.host_feth)
        try:
            tag = b'TG-SELFTEST-' + os.urandom(4)
            frame = (b'\xff\xff\xff\xff\xff\xff' + b'\x02tgate'
                     + b'\x88\xb5' + tag).ljust(64, b'\0')
            os.write(self.ndrv_fd, frame)
            deadline = time.time() + 1.0
            while True:
                timeout = deadline - time.time()
                if timeout <= 0:
                    break
                if not select.select([probe_fd], [], [], timeout)[0]:
                    break
                if tag in os.read(probe_fd, probe_blen):
                    logger.info("rx inject self-test passed (%s -> %s)",
                                self.nic_feth, self.host_feth)
                    return
            logger.error("rx inject self-test FAILED -- a frame written to "
                          "the NDRV socket on %s never reached %s; frames "
                          "the NIC receives will not reach the host stack",
                          self.nic_feth, self.host_feth)
        finally:
            os.close(probe_fd)

    def _set_tapdev_status(self, connected):
        '''Track the NIC link state on the host-facing feth interface.'''
        if self._connected == connected:
            return
        _ifconfig(self.host_feth, "up" if connected else "down")
        logger.info("host interface %s is %s", self.host_feth,
                    "up" if connected else "down")
        self._connected = connected

    def _adopt_nic_mac(self):
        '''Give the host feth the NIC's own MAC address. _put_tap_packet
        hands wire frames to the host feth unchanged, and those frames are
        addressed to the Tigon3 -- so unless the host feth answers to that
        address the host stack drops every unicast frame the NIC delivers,
        leaving only broadcast and multicast to get through. device_setup
        populates self.mac_addr before this runs.'''
        mac_addr = getattr(self, "mac_addr", None)
        if not mac_addr or not any(mac_addr) or mac_addr[0] & 1:
            logger.warning("no usable NIC MAC (%s) -- host feth keeps its "
                           "own address; the host will hear only broadcast "
                           "and multicast frames", mac_addr)
            return
        mac = ":".join("%02x" % b for b in mac_addr)
        try:
            _ifconfig(self.host_feth, "down")
            _ifconfig(self.host_feth, "ether", mac)
            _ifconfig(self.host_feth, "up")
        except subprocess.CalledProcessError as e:
            logger.error("could not set %s MAC to %s (%s) -- the host "
                         "stack will not receive unicast traffic",
                         self.host_feth, mac, e)
            return
        logger.info("host feth %s now answers to the NIC MAC %s",
                    self.host_feth, mac)

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
        n = os.write(self.ndrv_fd, pkt)
        if n != len(pkt):
            logger.warning("_put_tap_packet: short write %d/%d -- "
                           "frame dropped", n, len(pkt))
        elif self.verbose:
            logger.info("_put_tap_packet: %d/%d bytes -> %s",
                        n, len(pkt), self.nic_feth)
