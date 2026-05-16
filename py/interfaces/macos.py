'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2026  Saul St. John

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

# MacOSInterface - the user-space half of the macOS device interface.
#
# It talks to the ThunderGate PCIDriverKit dext (macos/TGDext), which
# matches the Tigon3 PCI device, maps its BAR0, and exposes config-space
# access through an IOUserClient. This class opens a connection to that
# dext over IOKit.framework and satisfies the same contract device.py
# expects of the vfio/sysfs/win interfaces: an integer `bar0` address
# plus cfg_read / cfg_write.
#
# The dext<->client ABI -- method selectors and memory types -- is
# defined in macos/TGDext/tg_dext.h; the constants here mirror it.
#
# DMA buffers and interrupt delivery (the `mm` attribute, needed by the
# TAP driver) are Phase 4b; for the flash path `mm` is None, as it is for
# tests/mock.py.

import ctypes
import ctypes.util

# --- dext ABI (mirror of macos/TGDext/tg_dext.h) -------------------------

kTGConfigRead  = 0      # scalar in: (offset);        scalar out: (value)
kTGConfigWrite = 1      # scalar in: (offset, value); scalar out: ()
kTGGetBar0Info = 2      # scalar in: ();              scalar out: (size)

kTGMemoryBar0  = 0      # IOConnectMapMemory memory type for BAR 0

# The IOService class the dext publishes (its Info.plist IOUserClass).
TG_DEXT_CLASS = "TGPCIDevice"

# --- IOKit.framework bindings -------------------------------------------

_iokit_path = ctypes.util.find_library("IOKit") \
    or "/System/Library/Frameworks/IOKit.framework/IOKit"
_iokit = ctypes.CDLL(_iokit_path)
_libc = ctypes.CDLL(None)

kern_return_t = ctypes.c_int
mach_port_t   = ctypes.c_uint
IOOptionBits  = ctypes.c_uint32

kIOReturnSuccess   = 0
kIOMainPortDefault = 0           # MACH_PORT_NULL -- the default IOKit port
kIOMapAnywhere     = 0x00000001

_iokit.IOServiceMatching.restype = ctypes.c_void_p
_iokit.IOServiceMatching.argtypes = [ctypes.c_char_p]

# IOServiceGetMatchingService consumes one reference on the matching dict.
_iokit.IOServiceGetMatchingService.restype = mach_port_t
_iokit.IOServiceGetMatchingService.argtypes = [mach_port_t, ctypes.c_void_p]

_iokit.IOServiceOpen.restype = kern_return_t
_iokit.IOServiceOpen.argtypes = [mach_port_t, mach_port_t, ctypes.c_uint32,
                                 ctypes.POINTER(mach_port_t)]

_iokit.IOServiceClose.restype = kern_return_t
_iokit.IOServiceClose.argtypes = [mach_port_t]

_iokit.IOObjectRelease.restype = kern_return_t
_iokit.IOObjectRelease.argtypes = [mach_port_t]

_iokit.IOConnectCallScalarMethod.restype = kern_return_t
_iokit.IOConnectCallScalarMethod.argtypes = [
    mach_port_t, ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint64), ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint32)]

_iokit.IOConnectMapMemory64.restype = kern_return_t
_iokit.IOConnectMapMemory64.argtypes = [
    mach_port_t, ctypes.c_uint32, mach_port_t,
    ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint64),
    IOOptionBits]

_iokit.IOConnectUnmapMemory64.restype = kern_return_t
_iokit.IOConnectUnmapMemory64.argtypes = [
    mach_port_t, ctypes.c_uint32, mach_port_t, ctypes.c_uint64]


def _mach_task_self():
    # mach_task_self() is a macro for the global mach_task_self_ port.
    return mach_port_t.in_dll(_libc, "mach_task_self_").value


def _kr(kr):
    return "0x%08x" % (kr & 0xffffffff)


class MacOSInterface(object):
    def __init__(self):
        matching = _iokit.IOServiceMatching(TG_DEXT_CLASS.encode())
        if not matching:
            raise Exception("IOServiceMatching(%s) failed" % TG_DEXT_CLASS)
        self._service = _iokit.IOServiceGetMatchingService(
            kIOMainPortDefault, matching)
        if not self._service:
            raise Exception(
                "ThunderGate dext not found -- is the %s system extension "
                "loaded and a Tigon3 device present? See doc/INSTALL.macos.md"
                % TG_DEXT_CLASS)

    def __enter__(self):
        self._attach()
        self.mm = None          # DMA memory manager -- Phase 4b
        return self

    def __exit__(self, t, v, traceback):
        self._detach()
        if self._service:
            _iokit.IOObjectRelease(self._service)
            self._service = 0
        return False

    def _attach(self):
        conn = mach_port_t(0)
        kr = _iokit.IOServiceOpen(self._service, _mach_task_self(), 0,
                                  ctypes.byref(conn))
        if kr != kIOReturnSuccess:
            raise Exception("IOServiceOpen failed (%s)" % _kr(kr))
        self._conn = conn.value

        # BAR0 size from the dext's query method...
        self.bar0_sz = self._call_scalar(kTGGetBar0Info, [], 1)[0]

        # ...and its address by mapping it into this task.
        addr = ctypes.c_uint64(0)
        size = ctypes.c_uint64(0)
        kr = _iokit.IOConnectMapMemory64(
            self._conn, kTGMemoryBar0, _mach_task_self(),
            ctypes.byref(addr), ctypes.byref(size), kIOMapAnywhere)
        if kr != kIOReturnSuccess:
            _iokit.IOServiceClose(self._conn)
            del self._conn
            raise Exception("mapping BAR0 failed (%s)" % _kr(kr))
        self.bar0 = addr.value
        if not self.bar0_sz:
            self.bar0_sz = size.value

    def _detach(self):
        if hasattr(self, "bar0"):
            _iokit.IOConnectUnmapMemory64(self._conn, kTGMemoryBar0,
                                          _mach_task_self(), self.bar0)
            del self.bar0
        if hasattr(self, "_conn"):
            _iokit.IOServiceClose(self._conn)
            del self._conn

    def reattach(self):
        self._detach()
        self._attach()

    def _call_scalar(self, selector, inputs, n_out):
        n_in = len(inputs)
        in_arr = (ctypes.c_uint64 * n_in)(*inputs) if n_in else None
        out_arr = (ctypes.c_uint64 * n_out)() if n_out else None
        out_cnt = ctypes.c_uint32(n_out)
        kr = _iokit.IOConnectCallScalarMethod(
            self._conn, selector,
            in_arr, n_in,
            out_arr, ctypes.byref(out_cnt) if n_out else None)
        if kr != kIOReturnSuccess:
            raise Exception("dext method %d failed (%s)" % (selector, _kr(kr)))
        return [out_arr[i] for i in range(out_cnt.value)] if n_out else []

    def cfg_read(self, offset):
        assert 0 <= offset < 0x1000
        return self._call_scalar(kTGConfigRead, [offset], 1)[0] & 0xffffffff

    def cfg_write(self, offset, val):
        assert 0 <= offset < 0x1000
        self._call_scalar(kTGConfigWrite, [offset, val & 0xffffffff], 0)
