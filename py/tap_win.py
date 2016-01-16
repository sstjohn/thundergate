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
        self._wait_q = {}

    def __enter__(self):
        self.tfd = create_tap_if()
        self._tg_evt = IoctlAsync(IOCTL_TGWINK_PEND_INTR, self.dev.interface.cfgfd, 8)
        self._tap_evts = [ReadAsync(self.tfd, 0x800, self.mm),
                          ReadAsync(self.tfd, 0x800, self.mm)]
        self._hCon = GetStdHandle(STD_INPUT_HANDLE)
        self._events = (HANDLE * 4)(self._hCon, self._tg_evt.req.hEvent, self._tap_evts[0].req.hEvent, self._tap_evts[1].req.hEvent)
        self._tg_evt.submit()
        return self
    
    def __exit__(self):
        for t in self._tap_evts:
            t.reset(False)
        self._tg_evt.reset(False)
        del self._events
        del self._tap_evts
        del self._tg_evt

        del_tap_if(self.tfd)

    def _get_key(self):
        res = None
        cnt = DWORD(0)
        if not GetNumberOfConsoleInputEvents(self._hCon, pointer(cnt)):
            raise WinError()
        if 0 == cnt.value:
            return ''

        ir = (INPUT_RECORD * cnt.value)()
        rr = DWORD(0)
        
        if not ReadConsoleInput(self._hCon, cast(pointer(ir), POINTER(INPUT_RECORD)), cnt.value, pointer(rr)):
            raise WinError()

        if 0 == rr.value:
            print "[!] no input records available (??)"
            return ''

        for i in range(rr.value):
            if ir[i].EventType != KEY_EVENT:
                continue
            if not ir[i].Event.KeyEvent.bKeyDown:
                continue
            res = ir[i].Event.KeyEvent.uChar.AsciiChar
            return res
        return ''

    def _work_wait_q(self):
        if self.verbose:
            print "[+] processing wait queue..."
        completed = 0
        res = 0
        cnt = len(self._wait_q)
        while WAIT_TIMEOUT != res and cnt > 0:
            wait_handles = (HANDLE * cnt)(*self._wait_q.keys())
            res = WaitForMultipleObjects(cnt, cast(pointer(wait_handles), POINTER(c_void_p)), False, 0)
            if WAIT_FAILED == res:
                raise WinError()
            if res < cnt:
                k = wait_handles[res]
                self._wait_q[k]()
                del self._wait_q[k]
                completed += 1
                cnt -= 1
        if self.verbose:
            print "[+] cleaned %d items off the wait queue." % completed
        self.mm.free_coal()

    def _wait_for_something(self):
        res = WAIT_TIMEOUT
        if len(self._wait_q) > 50:
            self._work_wait_q()
        elif len(self._wait_q) > 0:
            res = WaitForMultipleObjects(4, cast(pointer(self._events), POINTER(c_void_p)), False, 0)
            if WAIT_TIMEOUT == res:
                self._work_wait_q()
        if WAIT_TIMEOUT == res:
            res = WaitForMultipleObjects(4, cast(pointer(self._events), POINTER(c_void_p)), False, INFINITE)
        if res < 2:
            return res
        if res < 4:
            self._tap_idx = res - 2
            return 2
        raise WinError()
        
    def _get_serial(self):
        serial = cast(self._tg_evt.buffer, POINTER(c_uint64)).contents.value
        self._tg_evt.reset()
        return serial
 
    def _get_packet(self):
        if self.verbose:
            print "[+] getting a packet from tap device...",
        pkt_len = self._tap_evts[self._tap_idx].pkt_len
        pkt = self._tap_evts[self._tap_idx].buffer
        self._tap_evts[self._tap_idx].reset()
        if self.verbose:
            print "read %d bytes" % pkt_len
        return (pkt, pkt_len)

    def __pkt_buf_free(self, overlapped, pkt):
        if self.verbose:
            print "[.] freeing sent packet at %x" % addressof(pkt)
        self.mm.free(addressof(pkt))
        CloseHandle(overlapped.hEvent)
        del overlapped

    def _write_pkt(self, pkt, length):
        if not self._connected:
            return
        o = OVERLAPPED(hEvent = CreateEvent(None, True, False, None))
        if self.verbose:
            print "[!] attempting to write to the tap device...",
        if not WriteFile(self.tfd, pkt, length, None, pointer(o)):
            err = get_last_error()
            if err > 0 and err != ERROR_IO_PENDING:
                raise WinError(err)
            self._wait_q[o.hEvent] = functools.partial(TapWinInterface.__pkt_buf_free, self, o, pkt)
        else:
            self.mm.free(addressof(pkt))
            CloseHandle(o.hEvent)
        if self.verbose:
            print "wrote %d bytes" % o.InternalHigh

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
                for t in self._tap_evts:
                    t.submit()
            else:
                for t in self._tap_evts:
                    t.reset(False)
            self._connected = connected
        finally:
            CloseHandle(o.hEvent)
