'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015  Saul St. John

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

import threading
import functools
from time import sleep

yield_quantum = functools.partial(sleep, 0)

class ExecutionMonitor(object):
    def __init__(self, dev):
        self._dev = dev
        self._watching = False

    def watch(self, callback):
        if self._watching:
            raise Exception("monitor already running")

        wrapped_callback = functools.partial(ExecutionMonitor._stopped, self, callback)
        t = threading.Thread(target = self._watch, args = (wrapped_callback,))
        t.daemon = True
        self._watching = True
        t.start()

    def _stopped(self, callback):
        self._watching = False
        callback()

    def _watch(self, callback):
        while not self._dev.rxcpu.status.halted:
            yield_quantum()
        callback()

