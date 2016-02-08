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

from ctypes import *
from ctypes.wintypes import *
import os
import struct
import uuid

from winlib import *
from mm.win import WinMemMgr

class WinInterface(object):
    def __init__(self):
        hInfoSet = SetupDiGetClassDevs(byref(GUID_DEVINTERFACE_TGWINK), None, None, DIGCF_DEVICEINTERFACE | DIGCF_PRESENT)
        if INVALID_HANDLE_VALUE == hInfoSet:
            raise WinError()

        devIntData = SP_DEVICE_INTERFACE_DATA(sizeof(SP_DEVICE_INTERFACE_DATA))
        devInfoData = SP_DEVINFO_DATA(sizeof(SP_DEVINFO_DATA))
        devIntDetail = SP_DEVICE_INTERFACE_DETAILS()
        devIntDetail._should_be_eight = 8L

        idx = 0

        while SetupDiEnumDeviceInterfaces(hInfoSet, None, byref(GUID_DEVINTERFACE_TGWINK),  idx, pointer(devIntData)):
            print "[.] found tgwink device interface #%d" % idx

            if not SetupDiGetDeviceInterfaceDetail(hInfoSet, pointer(devIntData), pointer(devIntDetail), sizeof(devIntDetail), None, None):
                raise WinError()

            idx += 1

        if idx == 0:
            raise Exception("no devices exporting tgwink interface found!")

        if idx > 1:
            print "[!] multiple tgwink interfaces found, using last."

        self.device_path = devIntDetail.DevicePath

    def __enter__(self):
        self._attach()
        self.mm = WinMemMgr(self.cfgfd)

    def _attach(self):
        self.cfgfd = CreateFile(self.device_path, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None)
        if self.cfgfd == INVALID_HANDLE_VALUE:
            raise WinError()

        handshake = c_uint32(0)
        #if not DeviceIoControl(self.cfgfd, IOCTL_TGWINK_SAY_HELLO, None, 0, pointer(handshake), sizeof(handshake), None, None):
        #    raise WinError()
        ioctl(self.cfgfd, IOCTL_TGWINK_SAY_HELLO, None, handshake)
        if handshake.value != 0x5a5aa5a5:
            raise Exception("unknown response from ioctl on tgwink interface")

        bar_ptr = c_int64()
        ioctl(self.cfgfd, IOCTL_TGWINK_MAP_BAR_0, None, bar_ptr)

        self.bar0 = bar_ptr.value

    def __exit__(self, t, v, traceback):
        self._detach()

    def _detach(self):
        NtUnmapViewOfSection(cast(-1, HANDLE), cast(self.bar0, c_void_p))
        del self.bar0
        CloseHandle(self.cfgfd)
        del self.cfgfd
        
    def reattach(self):
        self._detach()
        self._reattach()

    def cfg_read(self, offset):
        assert offset >= 0 and offset < 0x400
        try:
            req = OVERLAPPED(Offset=offset, hEvent = CreateEvent(None, True, False, None))
            val = c_uint32(0)
            if not ReadFile(self.cfgfd, pointer(val), 4, None, pointer(req)):
                err = WinError()
                if err.winerror == ERROR_IO_PENDING:
                    if WAIT_FAILED == WaitForSingleObject(req.hEvent, INFINITE):
                        raise WinError()
                elif err.winerror == 0:
                    pass
                else:
                    raise err
            return val.value
        finally:
            CloseHandle(req.hEvent)

    def cfg_write(self, offset, inval):
        assert offset >= 0 and offset < 0x400
        try:
            req = OVERLAPPED(Offset=offset, hEvent = CreateEvent(None, True, False, None))
            bytes_written = DWORD(0)
            val = c_uint32(inval)
            if not WriteFile(self.cfgfd, pointer(val), 4, None, pointer(req)):
                err = WinError()
                if err.winerror == ERROR_IO_PENDING:
                    if WAIT_FAILED == WaitForSingleObject(req.hEvent, INFINITE):
                        raise WinError()
                elif err.winerror == 0:
                    pass
                else:
                    raise err
        finally:
            CloseHandle(req.hEvent)
