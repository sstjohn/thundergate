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

from winlib import *
from async_win import ReadAsync, IoctlAsync
import functools

class TapWinInterface(object):
    def __init__(self, dev):
        self.dev = dev
        self.mm = dev.interface.mm
        self._connected = False
        self._pending_completions = {}

    def __enter__(self):
        self.tfd = create_tap_if()
        self._tg_evt = IoctlAsync(IOCTL_TGWINK_PEND_INTR, self.dev.interface.cfgfd, 8)
        self._tap_evt = ReadAsync(self.tfd, 0x800, self.mm)
        self._hCon = GetStdHandle(STD_INPUT_HANDLE)
        self._events = (HANDLE * 3)(self._hCon, self._tg_evt.req.hEvent, self._tap_evt.req.hEvent)
        self._tg_evt.submit()
        return self
    
    def __exit__(self):
        self._tap_evt.reset(False)
        self._tg_evt.reset(False)
        del self._events
        del self._tap_evt
        del self._tg_evt

        del_tap_if(self.tfd)

    def _wait_for_keypress(self):
        ir = INPUT_RECORD()
        rr = DWORD(0)
        while self.running and (ir.EventType != 1 or not ir.Event.KeyEvent.bKeyDown):
            if not ReadConsoleInput(self._hCon, pointer(ir), 1, pointer(rr)):
                raise WinError()
        return ir.Event.KeyEvent.uChar.AsciiChar

    def _wait_for_something(self):
        while self._running:        
            res = WaitForMultipleObjectsEx(len(self._events), cast(pointer(self._events), POINTER(c_void_p)), False, INFINITE, True)
            if res < 3:
                return res
            if res == WAIT_FAILED:
                raise WinError()
        
    def _get_serial(self):
        serial = cast(self._tg_evt.buffer, POINTER(c_uint64)).contents.value
        self._tg_evt.reset()
        return serial
 
    def _get_packet(self):
        if self.verbose:
            print "[+] getting a packet from tap device...",
        pkt_len = self._tap_evt.pkt_len
        pkt = self._tap_evt.buffer
        self._tap_evt.reset()
        if self.verbose:
            print "read %d bytes" % pkt_len
        return (pkt, pkt_len)

    def _tap_write_completion(self, overlapped, pkt, errcode, written, overlapped_ptr):
        if self.verbose:
            print "[.] freeing sent packet at %x" % addressof(pkt)
        self.mm.free(addressof(pkt))
        del self._pending_completions[addressof(pkt)]

    def _write_pkt(self, pkt, length):
        if not self._connected:
            return
        o = OVERLAPPED(hEvent = CreateEvent(None, True, False, None))
        if self.verbose:
            print "[!] attempting to write to the tap device...",
        completion = FileIOCompletion(functools.partial(TapWinInterface._tap_write_completion, self, o, pkt))
        if not WriteFileEx(self.tfd, pkt, length, pointer(o), completion):
            raise WinError()
        else:
            self._pending_completions[addressof(pkt)] = completion
        if self.verbose:
            print "queued %d bytes" % len(pkt)

    def _set_tapdev_status(self, connected):
        if self.verbose:
            print "[+] setting tapdev status to %s" % ("up" if connected else "down")
        o = OVERLAPPED(hEvent = CreateEvent(None, True, False, None))
        try:
            val = c_int32(1 if connected else 0)
            if not DeviceIoControl(self.tfd, TAP_WIN_IOCTL_SET_MEDIA_STATUS, pointer(val), 4, pointer(val), 4, None, pointer(o)):
                err = get_last_error()
                if err == ERROR_IO_PENDING:
                    if WAIT_FAILED == WaitForSingleObject(o.hEvent, INFINITE):
                        raise WinError()
                elif err == 0:
                    pass
                else:
                    raise WinError(err)
            if connected:
                self._tap_evt.submit()
            else:
                self._tap_evt.reset(False)
            self._connected = connected
        finally:
            CloseHandle(o.hEvent)
