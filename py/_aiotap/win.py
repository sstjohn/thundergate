'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016  Saul St. John

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

import functools
import logging

logger = logging.getLogger(__name__)

from winlib import (
    ReadConsoleInput, WinError, pointer, INPUT_RECORD, GetStdHandle, STD_INPUT_HANDLE,
    DWORD, create_tap_if, del_tap_if, IOCTL_TGWINK_PEND_INTR, ioctl, create_string_buffer,
    c_int32, TAP_WIN_IOCTL_SET_MEDIA_STATUS, DeviceIoControl,
)

class TapWinInterface(object):
    def __init__(self, dev):
        self.dev = dev

    def __enter__(self):
        self.tfd = create_tap_if()
        self._hCon = GetStdHandle(STD_INPUT_HANDLE)
        return self
    
    def __exit__(self):
        del_tap_if(self.tfd)

    def _wait_for_keypress(self):
        ir = INPUT_RECORD()
        rr = DWORD(0)
        while self.running and (ir.EventType != 1 or not ir.Event.KeyEvent.bKeyDown):
            if not ReadConsoleInput(self._hCon, pointer(ir), 1, pointer(rr)):
                raise WinError()
        return ir.Event.KeyEvent.uChar.AsciiChar

    def _wait_for_interrupt(self):
        if not self.running:
            return
        logger.debug("waiting for interrupt")
        buf = create_string_buffer(8)
        ioctl(self.dev.interface.cfgfd, IOCTL_TGWINK_PEND_INTR, None, buf) 
        logger.debug("finished waiting for interrupt")

    def _set_tapdev_status(self, connected):
        if self.verbose:
            print "[+] setting tapdev status to %s" % ("up" if connected else "down")
        val = c_int32(1 if connected else 0)
        if not DeviceIoControl(self.tfd, TAP_WIN_IOCTL_SET_MEDIA_STATUS, pointer(val), 4, pointer(val), 4, None, None):
            raise WinError()
