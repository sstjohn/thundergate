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

import ctypes
import tglib as tg
import struct
import os
import select
import reutils
import platform
import functools
import sys
from stats import TapStatistics

default_verbosity = 0

sys_name = platform.system()

if sys_name == "Linux":
    import fcntl
    
    import clib as c
    from tunlib import *
    from linux import TapLinuxInterface
    TDInt = TapLinuxInterface
elif sys_name == "Windows" or sys_name == "cli":
    from winlib import *
    from win import TapWinInterface
    TDInt = TapWinInterface
else:
    raise NotImplementedError("tap driver only available on linux and windows")
   
from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

from ctypes import cast, pointer, POINTER, sizeof

from dev_fns import device_setup
from ring import init_tx_rings, init_rx_rings, init_rr_rings, populate_rx_ring
from link import link_detect

class TapDriver(TDInt):
    def __init__(self, dev):
        self.verbose = default_verbosity
        super(TapDriver, self).__init__(dev)
        self.dev = dev
        self.mm = dev.interface.mm
        self.stats = TapStatistics()

    def __enter__(self):
        print "[+] driver initialization begins"
        super(TapDriver, self).__enter__()
        self._device_setup()
        return self

    def __exit__(self, t, v, traceback):
        self.dev.close()
        super(TapDriver, self).__exit__()
        print "[+] driver terminated"

    _device_setup = device_setup
    _init_tx_rings = init_tx_rings                
    _init_rx_rings = init_rx_rings
    _init_rr_rings = init_rr_rings
    _populate_rx_ring = populate_rx_ring
    _link_detect = link_detect
    

    def _handle_interrupt(self):
        _ = self._get_serial()

        dev = self.dev
        if self.verbose:
            print "[+] handling interrupt"
        
        _ = dev.hpmb.box[tg.mb_interrupt].low
        tag = 0

        while self.status_block.updated:
            tag = self.status_block.status_tag
            if self.verbose:
                print "[+] status tag %x" % tag
            tag = tag << 24

            self.status_block.updated = 0
            if self.verbose:
                print "[+] status block updated! link: %d, attention: %d" % (self.status_block.link_status, self.status_block.attention)

            if dev.emac.status.link_state_changed:
                self._link_detect()
                dev.emac.status.link_state_changed = 1
                
            for i in range(len(dev.mem.rxrcb)):
                pi = getattr(self.status_block, "rr%d_pi" % i)
                ci = self.rr_rings_ci[i]

                if pi != ci:
                    if self.verbose:
                        print "[+] rr %d: pi is %x, ci was %x," % (i, pi, ci),

                    if pi < ci:
                        count = self.rr_rings_len - ci 
                        count += pi
                    else:
                        count = pi - ci
                    
                    if self.verbose:
                        print "%d bds received" % count
                    rbds = ctypes.cast(self.rr_rings_vaddr[i], ctypes.POINTER(tg.rbd))
                    while count > 0:
                        ci += 1
                        if ci > self.rr_rings_len:
                            ci = 1
                        rbd = rbds[ci - 1]

                        if self.verbose:
                            print "consuming bd 0x%x" % ci
                            print " addr:      %08x:%08x" % (rbd.addr_hi, rbd.addr_low)
                            print "  buf[%d] vaddr: %x, paddr: %x" % (rbd.index, self.rx_ring_buffers[rbd.index], self.mm.get_paddr(self.rx_ring_buffers[rbd.index]))
                            print " length:    %04x" % rbd.length
                            print " index:     %04x" % rbd.index
                            print " type:      %04x" % rbd.type
                            print " flags:    ",
                            for j in ["is_ipv6", "is_tcp", "l4_checksum_correct", "ip_checksum_correct", "reserved", "has_error", "has_vlan_tag", "reserved2", "reserved3", "rss_hash_valid", "packet_end", "reserved4", "reserved5"]:
                                if getattr(rbd.flags, j):
                                    print j,
                            print

                            if rbd.flags.rss_hash_type != 0:
                                print " rss hash type: %x" % rbd.flags.rss_hash_type

                            print " ip cksum:  %04x" % rbd.ip_cksum
                            print " l4 cksum: %04x" % rbd.l4_cksum
                            print " err flags:",
                            for j in ["reserved1", "reserved2", "reserved3", "reserved4", "reserved5", "reserved6", "reserved7", "giant_packet", "trunc_no_res", "len_less_64", "mac_abort", "dribble_nibble", "phy_decode_error", "link_lost", "collision", "bad_crc"]:
                                if getattr(rbd.error_flags, j):
                                    print j,
                            print
                            print " vlan_tag:  %04x" % rbd.vlan_tag
                            print " rss_hash:  %08x" % rbd.rss_hash
                            print " opaque:    %08x" % rbd.opaque

                        buf = ctypes.cast(self.rx_ring_buffers[rbd.index], ctypes.POINTER(ctypes.c_char * rbd.length))[0]
                        new_buf = self.mm.alloc(0x800)
                        new_pbuf = self.mm.get_paddr(new_buf)
                        self.rx_ring_bds[rbd.index].addr_hi = new_pbuf >> 32
                        self.rx_ring_bds[rbd.index].addr_low = new_pbuf & 0xffffffff
                        self.rx_ring_buffers[rbd.index] = new_buf

                        self._write_pkt(buf, rbd.length)
                         
                        count -= 1

                    mb = getattr(tg, "mb_rbd_rr%d_consumer" % i)
                    dev.hpmb.box[mb].low = ci
                    self.rr_rings_ci[i] = ci
            
            new_ci = self.status_block.rpci
            old_ci = self._std_rbd_ci
            count = 0
            if new_ci != old_ci:
                if self.verbose:
                    print "[+] rbdp ci now %x, was %x" % (new_ci, old_ci)
                rbds = ctypes.cast(self.rx_ring_vaddr, ctypes.POINTER(tg.rbd))
                while new_ci != old_ci:
                    count += 1
                    rbds[old_ci].flags.word = 0
                    rbds[old_ci].error_flags.word = 0
                    rbds[old_ci].length = 0x600
                    old_ci += 1
                    if old_ci == self.rx_ring_len:
                        old_ci = 0

                self._std_rbd_ci = new_ci

                self._std_rbd_pi += count
                if self._std_rbd_pi >= self.rx_ring_len:
                    self._std_rbd_pi -= self.rx_ring_len

                if self.verbose:
                    print "[+] moving std rbd pi to %x" % self._std_rbd_pi
                self.dev.hpmb.box[tg.mb_rbd_standard_producer].low = self._std_rbd_pi

            tx_ci = self.status_block.sbdci
            if tx_ci != self._tx_ci:
                if self.verbose:
                    print "[+] sbd ci: %x" % tx_ci

                if tx_ci < self._tx_ci:
                    if self.verbose:
                        if self._tx_ci + 1 == self.tx_ring_len:
                            print "[.] freeing tx buffer %02x" % self._tx_ci
                        else:
                            print "[.] freeing tx buffers %02x-%02x" % (self._tx_ci, self.tx_ring_len - 1)
                    while self._tx_ci < self.tx_ring_len:
                        self.mm.free(self._tx_buffers[self._tx_ci])
                        self._tx_ci += 1
                if self._tx_ci == self.tx_ring_len:
                    self._tx_ci = 0
                if self.verbose:
                    if tx_ci == self._tx_ci + 1:
                        print "[.] freeing tx buffer %02x" % self._tx_ci
                    elif tx_ci > self._tx_ci:
                        print "[.] freeing tx buffers %02x-%02x" % (self._tx_ci, tx_ci - 1)
                while tx_ci > self._tx_ci:
                    self.mm.free(self._tx_buffers[self._tx_ci])
                    self._tx_ci += 1



        if self.verbose:
            print "[+] interrupt handling concluded"
        self.dev.hpmb.box[tg.mb_interrupt].low = tag
        _ = self.dev.hpmb.box[tg.mb_interrupt].low

    def _write_pkt(self, pkt, length):
        super(TapDriver, self)._write_pkt(pkt, length)
        self.stats.pkt_in(length)

    def send(self, data, flags=None):
        if len(data) < 64:
            data = data + ('\x00' * (64 - len(data)))
        b_vaddr = self.mm.alloc(len(data))
        b = ctypes.cast(b_vaddr, ctypes.POINTER(ctypes.c_char * len(data)))
        b[0] = (ctypes.c_char * len(data)).from_buffer_copy(data)
        
        self._send_b(b_vaddr, len(data), flags=flags)

    def _send_b(self, buf, buf_sz, flags=None):
        i = self._tx_pi
        self._tx_buffers[i] = buf
        if self.verbose:
            print "[+] sending buffer at %x len 0x%x using sbd #%d" % (buf, buf_sz, i)
        paddr = self.mm.get_paddr(buf)
        txb = ctypes.cast(self.tx_ring_vaddr, ctypes.POINTER(tg.sbd))
        txb[i].addr_hi = paddr >> 32
        txb[i].addr_low = paddr & 0xffffffff
        txb[i].length = buf_sz
        txb[i].flags.packet_end = 1
        if flags != None:
            for j in flags:
                setattr(txb[i].flags, j, 1)

        i += 1
        if i == self.tx_ring_len:
            i = 0

        self.dev.hpmb.box[tg.mb_sbd_host_producer].low = i
        _ = self.dev.hpmb.box[tg.mb_sbd_host_producer].low
        self._tx_pi = i
        if self.verbose:
            print "[+] host sbd pi now %x" % i
        self.stats.pkt_out(buf_sz)
    
    def _handle_tap(self):
        pkt, sz = self._get_packet()
        self._send_b(pkt, sz)

    def _handle_keypress(self, handlers):
        k = self._get_key()
        if k in handlers:
            handlers[k][1]()
        elif k == '' or k == ' ' or k == None:
            pass
        else:
            print "keypress '%s' unhandled. press 'h' for help." % k

    def _help(self, handlers):
        print 
        for k in handlers:
            print "%s - %s" % (k, handlers[k][0])
        print

    def toggle_verbosity(self):
        self.verbose = not self.verbose
        print "[+] verbosity %s" % ("enabled" if self.verbose else "disabled")

    def _stop(self):
        self._running = False
        
    def run(self):
        self.dev.unmask_interrupts()
        print "[+] waiting for interrupts..."
        self._running = True
        
        k_handlers = {'q': ("quit", functools.partial(TapDriver._stop, self)),
                      'd': ("link detect", functools.partial(TapDriver._link_detect, self)),
                      'v': ("toggle verbosity", functools.partial(TapDriver.toggle_verbosity, self)),
                      's': ("dump statistics", functools.partial(TapStatistics.display, self.stats)),
                      'r': ("reset statistics", functools.partial(TapStatistics.reset, self.stats))}

        k_handlers['h'] = ("help", functools.partial(TapDriver._help, self, k_handlers))

        e_handlers = {0: functools.partial(TapDriver._handle_keypress, self, k_handlers),
                      1: functools.partial(TapDriver._handle_interrupt, self),
                      2: functools.partial(TapDriver._handle_tap, self)}

        while self._running:
            e_handlers[self._wait_for_something()]()
        return 0