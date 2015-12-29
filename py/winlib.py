

from ctypes import *
from ctypes.wintypes import *

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

WriteFile = kernel32.WriteFile
WriteFile.argtypes = [HANDLE, LPCVOID, DWORD, POINTER(DWORD), POINTER(OVERLAPPED)]
ReadFile.restype = BOOL

NtUnmapViewOfSection = windll.ntdll.NtUnmapViewOfSection
NtUnmapViewOfSection.argtypes = [HANDLE, LPVOID]
NtUnmapViewOfSection.restype = ULONG

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = BOOL

HDEVINFO = HANDLE
DI_FUNCTION = UINT

newdev = windll.newdev
fun_prototypes = [(setupapi, "SetupDiCreateDeviceInfoList", [POINTER(GUID), HWND], HDEVINFO),
                  (setupapi, "SetupDiCreateDeviceInfoA", [HDEVINFO, LPCSTR, POINTER(GUID), LPCSTR, HWND, DWORD, POINTER(SP_DEVINFO_DATA)], BOOL),
                  (setupapi, "SetupDiSetDeviceRegistryPropertyA", [HDEVINFO, POINTER(SP_DEVINFO_DATA), DWORD, POINTER(BYTE), DWORD], BOOL),
                  (setupapi, "SetupDiCallClassInstaller", [DI_FUNCTION, HDEVINFO, POINTER(SP_DEVINFO_DATA)], BOOL),
                  (setupapi, "SetupDiDestroyDeviceInfoList", [HDEVINFO], BOOL),
                  (newdev, "DiInstallDevice", [HWND, HDEVINFO, POINTER(SP_DEVINFO_DATA), LPVOID, DWORD, POINTER(BOOL)], BOOL),
                 ]

for proto in fun_prototypes:
    dll, name, args, res = proto
    f = getattr(dll, name)
    f.argtypes = args
    f.restype = res
    if name[-1] == 'A':
        name = name[:-1]
    globals()[name] = f


DICD_GENERATE_ID = 1
SPDRP_DEVICEDESC = 0
SPDRP_HARDWARE_ID = 1
SPDRP_FRIENDLYNAME = 0xc
DIF_SELECTBESTCOMPATDRV = 0x17
DIF_REGISTERDEVICE = 0x19
INSTALLFLAG_FORCE = 1

def create_tap_if(name = None):
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

