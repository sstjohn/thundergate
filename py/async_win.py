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
from ctypes import *

class _async(object):
    def __init__(self, handle):
        self.handle = handle
        self.req = OVERLAPPED(hEvent = CreateEvent(None, True, False, None))
        self.submitted = False
        self.reset(False)

    def __del__(self):
        if self.submitted:
            CancelIoEx(self.handle, pointer(self.req))
        CloseHandle(self.req.hEvent)

    def submit(self):
        raise NotImplementedError()

    def reset(self, resubmit = True):
        if self.submitted:
            CancelIoEx(self.handle, pointer(self.req))
        self.submitted = False        
        self.req.Internal = 0
        self.req.InternalHigh = 0
        self.req.Pointer = None
        if resubmit:
            self.submit()
        
class ReadAsync(_async):
    def __init__(self, handle, length, mm):
        self.length = length
        self.mm = mm
        super(ReadAsync, self).__init__(handle)

    def reset(self, resubmit = True):
        self._pkt_len = 0
        self.buffer = self.mm.alloc(self.length)
        super(ReadAsync, self).reset(resubmit)

    @property
    def pkt_len(self):
        if not self._pkt_len:
            #pkt_len = DWORD(0)
            #if not GetOverlappedResult(self.handle, pointer(self.req), pointer(pkt_len), False):
            #    err = WinError()
            #    if err.winerror == ERROR_IO_PENDING or err.winerror == ERROR_IO_INCOMPLETE:
            #        return 0
            #    raise err
            #self._pkt_len = pkt_len.value
            self.submitted = False
            return self.req.InternalHigh    
        return self._pkt_len
    
    def submit(self):
        pkt_len = DWORD(0)
        if not ReadFile(self.handle, cast(self.buffer, c_void_p), self.length, pointer(pkt_len), pointer(self.req)):
            err = get_last_error()
            if err != 0 and err != ERROR_IO_PENDING:
                raise WinError(err)
            self._pkt_len = 0
            self.submitted = True
        else:
            if not SetEvent(self.req.hEvent):
                raise WinError()
            self._pkt_len = pkt_len.value

class IoctlAsync(_async):
    def __init__(self, ioctl, handle, length, indata = None):
        super(IoctlAsync, self).__init__(handle)
        self.ioctl = ioctl
        if indata is not None:
            self.in_sz = len(indata)
            self.in_buf = create_string_buffer(indata)
        else:
            self.in_sz = 0
            self.in_buf = create_string_buffer(0)
        self.length = length
        self.buffer = (c_char * length)()

    def submit(self):
        if 0 == ioctl(self.handle, self.ioctl, self.in_buf, self.buffer, self.req):
            self.submitted = True
        else:
            if not SetEvent(self.req.hEvent):
                raise WindowsError()
        
