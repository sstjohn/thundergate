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
import time
import os
import select
import reutils
import platform
import functools
import sys

import trollius as asyncio
from trollius import From, Return, coroutine

import logging
logger = logging.getLogger(__name__)

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

from dev_fns import _device_setup, _enable_rx, _enable_tx
from link import _link_detect
from interrupt import _handle_interrupt

def async_msleep(self, t):
    yield From(asyncio.sleep(t / 1000.0))

class TapDriver(TDInt):
    def __init__(self, dev):
        self.verbose = default_verbosity
        super(TapDriver, self).__init__(dev)
        self.dev = dev
        self.mm = dev.interface.mm
        self.stats = TapStatistics()
        self._connected = False

    def __enter__(self):
        print "[+] tap driver initializing"
        super(TapDriver, self).__enter__()
        self.old_msleep = self.dev.msleep
        self.dev.msleep = async_msleep.__get__(self.dev)
        return self

    def __exit__(self, t, v, traceback):
        self.dev.msleep = self.old_msleep
        super(TapDriver, self).__exit__()
        self.dev.close()
        print "[+] tap driver terminated"

    device_setup = _device_setup
    enable_rx = _enable_rx
    enable_tx = _enable_tx
    
    link_detect = _link_detect
    handle_interrupt = _handle_interrupt

    @coroutine
    def gui_handler(self):
        '''launch wxwidgets gui'''
        import gui
        gui.run(self.dev)

    @coroutine
    def help_handler(self):
        '''display keypress bindings'''
        print 
        for k in self.keypress_handlers:
            print "%s - %s" % (k, self.keypress_handlers[k].__doc__)
        print

    @coroutine
    def verbosity_handler(self):
        '''toggle tap driver verbosity'''
        self.verbose = not self.verbose
        print "[+] verbosity %s" % ("enabled" if self.verbose else "disabled")

    @coroutine
    def quit_handler(self):
        '''terminate tap driver execution and close device'''
        self.running = False
        self.loop.stop()

    @coroutine
    def unknown_keypress_handler(self, k):
        print "read unknown keypress '%s'" % k

    @coroutine
    def keypress_dispatch(self):
        r = yield From(self.loop.run_in_executor(None, self._wait_for_keypress))
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

    @coroutine
    def interrupt_watcher(self):
        if hasattr(self, "_wait_for_interrupt"):
            waiter = self._wait_for_interrupt
        else:
            waiter = self._watch_for_sb_update

        yield From(self.loop.run_in_executor(None, waiter))
        yield From(self.handle_interrupt())
        if self.running:
            asyncio.ensure_future(self.interrupt_watcher())

    @coroutine
    def tap_watcher(self):
        pass


    @coroutine
    def arrive_device(self):
        yield From(self.device_setup())
        yield From(self.enable_rx())
        asyncio.ensure_future(self.interrupt_watcher())

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
        asyncio.executor.get_default_executor().shutdown(False) 
