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
from interrupt import handle_interrupt, handle_rr, replenish_rx_bds, free_sent_bds, dump_bd

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
    _handle_interrupt = handle_interrupt
    _handle_rr = handle_rr
    _free_sent_bds = free_sent_bds
    _dump_bd = dump_bd
    _replenish_rx_bds = replenish_rx_bds


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
