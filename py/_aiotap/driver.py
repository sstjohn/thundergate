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

import ctypes
import tglib as tg
import struct
import time
import os
import select
import reutils
import platform
import functools
import sys

import asyncio

import logging
logger = logging.getLogger(__name__)

from .stats import TapStatistics

default_verbosity = 0

sys_name = platform.system()

if sys_name == "Linux":
    import fcntl

    import cabi as c
    from cabi import *
    from .linux import TapLinuxInterface
    TDInt = TapLinuxInterface

elif sys_name == "Windows" or sys_name == "cli":
    from winlib import *
    from .win import TapWinInterface
    TDInt = TapWinInterface

    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

elif sys_name == "Darwin":
    from .macos import TapMacInterface
    TDInt = TapMacInterface

else:
    raise NotImplementedError("tap driver only available on linux, macos and windows")
   
from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

from ctypes import cast, pointer, POINTER, sizeof

from .dev_fns import _device_setup, _enable_rx, _enable_tx
from .link import _link_detect
from .interrupt import _handle_interrupt

async def async_msleep(self, t):
    await asyncio.sleep(t / 1000.0)

class TapDriver(TDInt):
    def __init__(self, dev):
        self.verbose = default_verbosity
        super(TapDriver, self).__init__(dev)
        self.dev = dev
        self.mm = dev.interface.mm
        self.stats = TapStatistics()
        self._connected = False

    def __enter__(self):
        print("[+] tap driver initializing")
        super(TapDriver, self).__enter__()
        self.old_msleep = self.dev.msleep
        self.dev.msleep = async_msleep.__get__(self.dev)
        return self

    def __exit__(self, t, v, traceback):
        self.dev.msleep = self.old_msleep
        super(TapDriver, self).__exit__()
        self.dev.close()
        print("[+] tap driver terminated")

    device_setup = _device_setup
    enable_rx = _enable_rx
    enable_tx = _enable_tx
    
    link_detect = _link_detect
    handle_interrupt = _handle_interrupt

    async def gui_handler(self):
        '''launch wxwidgets gui'''
        import gui
        gui.run(self.dev)

    async def help_handler(self):
        '''display keypress bindings'''
        print()
        for k in self.keypress_handlers:
            print("%s - %s" % (k, self.keypress_handlers[k].__doc__))
        print()

    async def verbosity_handler(self):
        '''toggle tap driver verbosity'''
        self.verbose = not self.verbose
        print("[+] verbosity %s" % ("enabled" if self.verbose else "disabled"))

    async def quit_handler(self):
        '''terminate tap driver execution and close device'''
        self.running = False
        self.loop.stop()

    async def unknown_keypress_handler(self, k):
        print("read unknown keypress '%s'" % k)

    async def keypress_dispatch(self):
        r = await self.loop.run_in_executor(None, self._wait_for_keypress)
        if r in self.keypress_handlers:
            asyncio.ensure_future(self.keypress_handlers[r]())
        else:
            asyncio.ensure_future(self.unknown_keypress_handler(r))
        asyncio.ensure_future(self.keypress_dispatch())

    def _watch_for_sb_update(self):
        logger.info("watching for status block update")
        while self.running:
            if self.status_block.updated:
                logger.info("status block updated")
                return
            time.sleep(.01)
        logger.info("status block not updated, terminating watch")

    async def interrupt_watcher(self):
        if hasattr(self, "_wait_for_interrupt"):
            waiter = self._wait_for_interrupt
        else:
            waiter = self._watch_for_sb_update

        await self.loop.run_in_executor(None, waiter)
        await self.handle_interrupt()
        if self.running:
            asyncio.ensure_future(self.interrupt_watcher())

    def _send_b(self, buf, buf_sz):
        '''Hand a DMA buffer holding one frame to the NIC's send ring.'''
        i = self._tx_pi
        self._tx_buffers[i] = buf
        paddr = self.mm.get_paddr(buf)
        txb = cast(self.tx_ring_vaddr, POINTER(tg.sbd))
        txb[i].addr_hi = paddr >> 32
        txb[i].addr_low = paddr & 0xffffffff
        txb[i].length = buf_sz
        txb[i].flags.packet_end = 1
        i = (i + 1) % self.tx_ring_len
        self.dev.hpmb.box[tg.mb_sbd_host_producer].low = i
        _ = self.dev.hpmb.box[tg.mb_sbd_host_producer].low  # flush the posted write
        self._tx_pi = i
        self.stats.pkt_out(buf_sz)

    async def tap_watcher(self):
        buf = self.mm.alloc(0x800)
        buf, n = await self.loop.run_in_executor(
            None, self._get_tap_packet, buf, 0x800)
        if n < 64:
            ctypes.memset(buf + n, 0, 64 - n)
            n = 64
        self._send_b(buf, n)
        if self.running:
            asyncio.ensure_future(self.tap_watcher())

    async def arrive_device(self):
        await self.device_setup()
        await self.enable_rx()
        await self.enable_tx()
        asyncio.ensure_future(self.interrupt_watcher())
        asyncio.ensure_future(self.tap_watcher())

    def run(self):
        self.running = True
        self.keypress_handlers = {
            'g': self.gui_handler,
            'h': self.help_handler,
            'q': self.quit_handler,
            'v': self.verbosity_handler,
        }

        self.loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.keypress_dispatch())
        asyncio.ensure_future(self.arrive_device())
        self.loop.run_forever()
        self.loop.run_until_complete(self.loop.shutdown_default_executor())
        self.loop.close()
