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

import trollius as asyncio
from trollius import From, Return

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

    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    raise NotImplementedError("tap driver only available on linux and windows")
   
from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

from ctypes import cast, pointer, POINTER, sizeof

from dev_fns import device_setup, enable_rx, enable_tx
from ring import init_tx_rings, init_rx_rings, init_rr_rings, populate_rx_ring
from link import link_detect
from interrupt import handle_interrupt, handle_rr, replenish_rx_bds, free_sent_bds, dump_bd

def async_msleep(self, t):
    yield From(asyncio.sleep(t / 1000.0))

class TapDriver(TDInt):
    def __init__(self, dev):
        self.verbose = default_verbosity
        super(TapDriver, self).__init__(dev)
        self.dev = dev
        self.mm = dev.interface.mm
        self.stats = TapStatistics()

    def __enter__(self):
        print "[+] tap driver initializing"
        super(TapDriver, self).__enter__()
        self.old_msleep = self.dev.msleep
        self.dev.msleep = async_msleep.__get__(self.dev)
        asyncio.ensure_future(self._device_setup())
        return self

    def __exit__(self, t, v, traceback):
        self.dev.msleep = self.old_msleep
        super(TapDriver, self).__exit__()
        self.dev.close()
        print "[+] tap driver terminated"

    _device_setup = device_setup
    _enable_rx = enable_rx
    _enable_tx = enable_tx
    
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


    def put_tap_pkt(self, pkt):
        sent = self._put_tap_pkt(pkt)
        self.mm.free(pkt)
        self.stats.pkt_in(sent)

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


    @asyncio.coroutine
    def help_handler(self):
        '''display keypress bindings'''
        print 
        for k in self.keypress_handlers:
            print "%s - %s" % (k, self.keypress_handlers[k].__doc__)
        print

    @asyncio.coroutine
    def verbosity_handler(self):
        '''toggle tap driver verbosity'''
        self.verbose = not self.verbose
        print "[+] verbosity %s" % ("enabled" if self.verbose else "disabled")

    @asyncio.coroutine
    def quit_handler(self):
        '''terminate tap driver execution and close device'''
        self.running = False
        self.loop.stop()

    @asyncio.coroutine
    def unknown_keypress_handler(self, k):
        print "read unknown keypress '%s'" % k

    @asyncio.coroutine
    def keypress_dispatch(self):
        r = yield From(self.loop.run_in_executor(None, self._wait_for_keypress))
        if r in self.keypress_handlers:
            asyncio.ensure_future(self.keypress_handlers[r]())
        else:
            asyncio.ensure_future(self.unknown_keypress_handler(r))
        asyncio.ensure_future(self.keypress_dispatch())

    def run(self):
        self.running = True
        self.keypress_handlers = {'h': self.help_handler,
                                  'q': self.quit_handler,
                                  'v': self.verbosity_handler,}

        self.loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.keypress_dispatch())
        self.loop.run_forever()
        asyncio.executor.get_default_executor().shutdown(True) 
