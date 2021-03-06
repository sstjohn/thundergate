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

import traceback
import threading
import functools
from time import sleep

yield_quantum = functools.partial(sleep, 0)

class ExecutionMonitor(object):
    def __init__(self, dev, stopped_callback):
        self._dev = dev
        self._watching = False
        self._stopped_callback = stopped_callback

    def watch(self):
        if self._watching:
            raise Exception("monitor already running")
        if not (self._dev.rxcpu.status.word & 0x7FFFFFFF):
            raise Exception("cpu already running") 
        
        t = threading.Thread(target = self._watch, args = (self._stopped_callback,))
        t.daemon = True
        self._watching = True
        t.start()

    def _watch(self, callback):
        if self._dev.rxcpu.mode.halt:
            self._dev.rxcpu.mode.halt = 0
        if self._dev.rxcpu.status.word & 0x7ff:
            self._dev.rxcpu.status.word = 0xffffffff
        while not (self._dev.rxcpu.status.word & 0x7ff):
            yield_quantum()
        self._watching = False
        print "stopped watching at pc = %x" % self._dev.rxcpu.pc
        try:
            callback()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            raise e
