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

from ctypes import *
from ctypes.wintypes import *
import os
import struct
import uuid


INVALID_HANDLE_VALUE = HANDLE(-1)
METHOD_OUT_DIRECT = 2
FILE_ANY_ACCESS = 0
CTL_CODE = lambda d,f,m,a: ((d << 16) | (a << 14) | (f << 2) | m)

DIGCF_DEVICEINTERFACE = 0x10
DIGCF_PRESENT = 0x02

IOCTL_TGWINK_SAY_HELLO = CTL_CODE(0x8000, 0x8000, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)
IOCTL_TGWINK_MAP_BAR_0 = CTL_CODE(0x8000, 0x8001, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)

class GUID(Structure):
    _fields_ = [("Data1", c_ulong),
                ("Data2", c_ushort),
                ("Data3", c_ushort),
                ("Data4", ARRAY(c_byte, 8))]

GUID_DEVINTERFACE_TGWINK = GUID(0x77dce17a,0x78bd,0x4b27,(0x84,0x09,0x8f,0x5d,0x20,0x96,0x3c,0x39))

setupapi = windll.setupapi

SetupDiGetClassDevs = setupapi.SetupDiGetClassDevsA
SetupDiGetClassDevs.argtypes = [POINTER(GUID), LPCSTR, HWND, DWORD]
SetupDiGetClassDevs.restype = HANDLE

class SP_DEVINFO_DATA(Structure):
    _fields_ = [('cbSize', DWORD),
                ('ClassGuid', GUID),
                ('DevInst', DWORD),
                ('Reserved', POINTER(ULONG))]

class SP_DEVICE_INTERFACE_DATA(Structure):
    _fields_ = [('cbSize', DWORD),
                ('InterfaceClassGuid', GUID),
                ('Flags', DWORD),
                ('Reserved', POINTER(ULONG))]

SetupDiEnumDeviceInterfaces = setupapi.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.argtypes = [HANDLE, POINTER(SP_DEVINFO_DATA), POINTER(GUID), DWORD, POINTER(SP_DEVICE_INTERFACE_DATA)]
SetupDiEnumDeviceInterfaces.restype = BOOL

def SP_DEVICE_INTERFACE_DETAILS_ofsize(sz):
    class SP_DEVICE_INTERFACE_DETAILS(Structure):
        _fields_ = [('cbSize', DWORD),
                    ('DevicePath', ARRAY(c_char, sz))]

    return SP_DEVICE_INTERFACE_DETAILS(8)
        
SetupDiGetDeviceInterfaceDetail = setupapi.SetupDiGetDeviceInterfaceDetailA
SetupDiGetDeviceInterfaceDetail.argtypes = [HANDLE, POINTER(SP_DEVICE_INTERFACE_DATA), c_void_p, DWORD, POINTER(DWORD), POINTER(SP_DEVINFO_DATA)]
SetupDiGetDeviceInterfaceDetail.restype = BOOL

kernel32 = windll.kernel32

CreateFile = kernel32.CreateFileA
CreateFile.argtypes = [LPCSTR, DWORD, DWORD, c_void_p, DWORD, DWORD, HANDLE]
CreateFile.restype = HANDLE

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 1
FILE_SHARE_WRITE = 2
OPEN_EXISTING = 3

DeviceIoControl = kernel32.DeviceIoControl
DeviceIoControl.argtypes = [HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, POINTER(DWORD), c_void_p]
DeviceIoControl.restype = BOOL

class __o(Structure):
    pass
class __u(Union):
    pass
class OVERLAPPED(Structure):
    pass

__o._fields_ = [('Offset', DWORD), ('OffsetHigh', DWORD)]
__u._anonymous_ = ("o",)
__u._fields_ = [("o", __o), ("Pointer", LPVOID)]

OVERLAPPED._anonymous_ = ("u",)
OVERLAPPED._fields_ = [("Internal", POINTER(ULONG)),
                       ("InternalHigh", POINTER(ULONG)),
                       ("u", __u),
                       ("hEvent", HANDLE)]

ReadFile = kernel32.ReadFile
ReadFile.argtypes = [HANDLE, LPVOID, DWORD, POINTER(DWORD), POINTER(OVERLAPPED)]
ReadFile.restype = BOOL

class WinInterface(object):
    def __init__(self):
        hInfoSet = SetupDiGetClassDevs(byref(GUID_DEVINTERFACE_TGWINK), None, None, DIGCF_DEVICEINTERFACE | DIGCF_PRESENT)
        if INVALID_HANDLE_VALUE == hInfoSet:
            raise WindowsError()

        devIntData = SP_DEVICE_INTERFACE_DATA(sizeof(SP_DEVICE_INTERFACE_DATA))
        devInfoData = SP_DEVINFO_DATA(sizeof(SP_DEVINFO_DATA))

        idx = 0
        devIntDetail = None

        while SetupDiEnumDeviceInterfaces(hInfoSet, None, byref(GUID_DEVINTERFACE_TGWINK),  idx, pointer(devIntData)):
            print "[.] found device interface #%d" % idx
            detailSize = DWORD(0)

            SetupDiGetDeviceInterfaceDetail(hInfoSet, byref(devIntData), None, 0, pointer(detailSize), None)

            devIntDetail = SP_DEVICE_INTERFACE_DETAILS_ofsize(detailSize.value)

            if not SetupDiGetDeviceInterfaceDetail(hInfoSet, byref(devIntData), pointer(devIntDetail), detailSize, None, pointer(devInfoData)):
                raise WinError()

            idx += 1

        if idx == 0:
            raise Exception("no devices exporting tgwink interface found!")

        if idx > 1:
            print "[!] multiple tgwink interfaces found, using last."

        #self.cfgfd = os.open(devIntDetail.DevicePath, os.O_RDWR | os.O_BINARY)
        self.cfgfd = CreateFile(devIntDetail.DevicePath, GENERIC_READ | GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None)
        if self.cfgfd == INVALID_HANDLE_VALUE:
            raise WinError()

        handshake = c_int32(0)
        if not DeviceIoControl(self.cfgfd, IOCTL_TGWINK_SAY_HELLO, None, 0, pointer(handshake), sizeof(handshake), None, None):
            raise WinError()
        if handshake.value != 0x5a5aa5a5:
            raise BaseException("unknown response from ioctl on tgwink interface")

        bar_ptr = c_int64()
        if not DeviceIoControl(self.cfgfd, IOCTL_TGWINK_MAP_BAR_0, None, 0, pointer(bar_ptr), sizeof(bar_ptr), None, None):
            raise WinError()

        self.bar0 = bar_ptr.value

    def __enter__(self):
        pass

    def __exit__(self, t, v, traceback):
        pass

    def reattach(self):
        pass

    def cfg_read(self, offset):
        assert offset >= 0 and offset < 0x400
        req = OVERLAPPED(Offset=offset)
        val = c_uint32(0)
        bytes_read = DWORD(0)
        if not ReadFile(self.cfgfd, pointer(val), 4, pointer(bytes_read), pointer(req)):
            raise WinError()
        if bytes_read.value != 4:
            raise Exception("wrong number of bytes read")
        return val.value

    def cfg_write(self, offset, val):
        assert offset >= 0 and offset < 0x400
        raise NotImplementedError()
