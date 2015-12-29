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

class GUID(Structure):
    _fields_ = [("Data1", c_ulong),
                ("Data2", c_ushort),
                ("Data3", c_ushort),
                ("Data4", ARRAY(c_ubyte, 8))]

    def __str__(self):
       ret = ("%08x-" % self.Data1)
       ret += ("%04x-" % self.Data2)
       ret += ("%04x-" % self.Data3)
       ret += ("%02x%02x-" % (self.Data4[0], self.Data4[1]))
       ret += ''.join([("%02x" % b) for b in self.Data4[2:]])

       return ret

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


def SP_DEVICE_INTERFACE_DETAILS_ofsize(sz):
    class SP_DEVICE_INTERFACE_DETAILS(Structure):
        _fields_ = [('cbSize', DWORD),
                    ('DevicePath', ARRAY(c_char, sz))]

    return SP_DEVICE_INTERFACE_DETAILS(8)
        

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

HDEVINFO = HANDLE
DI_FUNCTION = UINT

REGSAM = DWORD

INVALID_HANDLE_VALUE = HANDLE(-1)
METHOD_OUT_DIRECT = 2
METHOD_BUFFERED = 0
FILE_ANY_ACCESS = 0
FILE_DEVICE_UNKNOWN = 0x22
DIGCF_DEVICEINTERFACE = 0x10
DIGCF_PRESENT = 0x02
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 1
FILE_SHARE_WRITE = 2
OPEN_EXISTING = 3
DICD_GENERATE_ID = 1
SPDRP_DEVICEDESC = 0
SPDRP_HARDWARE_ID = 1
SPDRP_FRIENDLYNAME = 0xc
DIF_SELECTBESTCOMPATDRV = 0x17
DIF_REGISTERDEVICE = 0x19
INSTALLFLAG_FORCE = 1
DIREG_DRV = 2
DICS_FLAG_GLOBAL = 1
KEY_QUERY_VALUE = 1
MAXIMUM_ALLOWED = 0x02000000
FILE_ATTRIBUTE_SYSTEM = 4
FILE_FLAG_OVERLAPPED = 0x40000000

CTL_CODE = lambda d,f,m,a: ((d << 16) | (a << 14) | (f << 2) | m)

IOCTL_TGWINK_SAY_HELLO = CTL_CODE(0x8000, 0x8000, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)
IOCTL_TGWINK_MAP_BAR_0 = CTL_CODE(0x8000, 0x8001, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)

TAP_WIN_IOCTL_GET_VERSION = CTL_CODE(FILE_DEVICE_UNKNOWN, 2, METHOD_BUFFERED, FILE_ANY_ACCESS)

GUID_DEVINTERFACE_TGWINK = GUID(0x77dce17a,0x78bd,0x4b27,(0x84,0x09,0x8f,0x5d,0x20,0x96,0x3c,0x39))

newdev = windll.newdev
advapi32 = windll.advapi32
setupapi = windll.setupapi
kernel32 = windll.kernel32
ntdll = windll.ntdll

fun_prototypes = [
    (kernel32, "CreateFileA", [LPCSTR, DWORD, DWORD, c_void_p, DWORD, DWORD, HANDLE], HANDLE),
    (kernel32, "ReadFile", [HANDLE, LPVOID, DWORD, POINTER(DWORD), POINTER(OVERLAPPED)], BOOL),
    (kernel32, "WriteFile", [HANDLE, LPCVOID, DWORD, POINTER(DWORD), POINTER(OVERLAPPED)], BOOL),
    (kernel32, "DeviceIoControl", [HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, POINTER(DWORD), c_void_p], BOOL),
    (kernel32, "CloseHandle", [HANDLE], BOOL),
    (ntdll, "NtUnmapViewOfSection", [HANDLE, LPVOID], ULONG),
    (setupapi, "SetupDiGetDeviceInterfaceDetailA", [HANDLE, POINTER(SP_DEVICE_INTERFACE_DATA), c_void_p, DWORD, POINTER(DWORD), POINTER(SP_DEVINFO_DATA)], BOOL),
    (setupapi, "SetupDiEnumDeviceInterfaces", [HANDLE, POINTER(SP_DEVINFO_DATA), POINTER(GUID), DWORD, POINTER(SP_DEVICE_INTERFACE_DATA)], BOOL),
    (setupapi, "SetupDiGetClassDevsA", [POINTER(GUID), LPCSTR, HWND, DWORD], HANDLE),
    (setupapi, "SetupDiCreateDeviceInfoList", [POINTER(GUID), HWND], HDEVINFO),
    (setupapi, "SetupDiCreateDeviceInfoA", [HDEVINFO, LPCSTR, POINTER(GUID), LPCSTR, HWND, DWORD, POINTER(SP_DEVINFO_DATA)], BOOL),
    (setupapi, "SetupDiSetDeviceRegistryPropertyA", [HDEVINFO, POINTER(SP_DEVINFO_DATA), DWORD, POINTER(BYTE), DWORD], BOOL),
    (setupapi, "SetupDiCallClassInstaller", [DI_FUNCTION, HDEVINFO, POINTER(SP_DEVINFO_DATA)], BOOL),
    (setupapi, "SetupDiDestroyDeviceInfoList", [HDEVINFO], BOOL),
    (setupapi, "SetupDiOpenDevRegKey", [HDEVINFO, POINTER(SP_DEVINFO_DATA), DWORD, DWORD, DWORD, REGSAM], HKEY),
    (newdev, "DiInstallDevice", [HWND, HDEVINFO, POINTER(SP_DEVINFO_DATA), LPVOID, DWORD, POINTER(BOOL)], BOOL),
    (advapi32, "RegQueryValueExA", [HKEY, LPCSTR, POINTER(DWORD), POINTER(DWORD), POINTER(BYTE), POINTER(DWORD)], LONG),
]

for proto in fun_prototypes:
    dll, name, args, res = proto
    f = getattr(dll, name)
    f.argtypes = args
    f.restype = res
    if name[-1] == 'A':
        name = name[:-1]
    globals()[name] = f

def create_tap_if(name = None):
#if __name__ == "__main__":
    class_guid = GUID(0x4d36e972,0xe325,0x11ce,(0xbf,0xc1,0x08,0x00,0x2b,0xe1,0x03,0x18))
    hwid = LPCSTR("tap0901")  #lolol
    class_name = LPCSTR("Network")

    h = SetupDiCreateDeviceInfoList(byref(class_guid), 0)
    if INVALID_HANDLE_VALUE == h:
        raise WinError()

    devInfoData = SP_DEVINFO_DATA()
    devInfoData.cbSize = sizeof(SP_DEVINFO_DATA)
    if not SetupDiCreateDeviceInfo(h, class_name, byref(class_guid), None, 0, DICD_GENERATE_ID, pointer(devInfoData)):
        raise WinError()

    if not SetupDiSetDeviceRegistryProperty(h, pointer(devInfoData), SPDRP_HARDWARE_ID, cast(hwid, POINTER(BYTE)), len(hwid.value) + 1):
        raise WinError()

    if not SetupDiCallClassInstaller(DIF_REGISTERDEVICE, h, pointer(devInfoData)):
        raise WinError()

    if not DiInstallDevice(None, h, pointer(devInfoData), None, 0, None):
        raise WinError()

    if None != name:
        p = LPCSTR(name)
        if not SetupDiSetDeviceRegistryProperty(h, pointer(devInfoData), SPDRP_FRIENDLYNAME, cast(p, POINTER(BYTE)), len(p.value) + 1):
            raise WinError()

    reg = SetupDiOpenDevRegKey(h, pointer(devInfoData), DICS_FLAG_GLOBAL, 0, DIREG_DRV, KEY_QUERY_VALUE)
    if INVALID_HANDLE_VALUE == reg:
        raise WinError()

    info_name = LPCSTR("NetCfgInstanceId")
    required_size = DWORD(128)
    cfg_iid = (c_char * 128)()
    result = RegQueryValueEx(reg, info_name, None, None, cast(pointer(cfg_iid), POINTER(BYTE)), pointer(required_size))
    if 0 != result:
        raise WinError(result)
    device_path = LPCSTR("\\\\.\\Global\\%s.tap" % cfg_iid.value)

    hdev = CreateFile(device_path, GENERIC_READ | GENERIC_WRITE, 0, 0, OPEN_EXISTING, FILE_ATTRIBUTE_SYSTEM | FILE_FLAG_OVERLAPPED, 0)
    if INVALID_HANDLE_VALUE.value == hdev:
        raise WinError()
  
    info = (ULONG * 3)()
    len = DWORD(0)
    if not DeviceIoControl(hdev, TAP_WIN_IOCTL_GET_VERSION, pointer(info), sizeof(info), pointer(info), sizeof(info), pointer(len), None):
        raise WinError()
    print "TAP-Windows Driver Version %d.%d.%d" % (info[0], info[1], info[2])

