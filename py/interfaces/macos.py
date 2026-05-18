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

# MacOSInterface -- the user-space half of the macOS device interface.
#
# It talks to the ThunderGate PCIDriverKit dext (macos/TGDext), which
# matches the Tigon3 PCI device, maps its BAR0, allocates DMA buffers,
# and delivers interrupts. This class opens a connection to that dext
# over IOKit.framework and satisfies the contract device.py expects of
# the vfio/sysfs/win interfaces: an integer `bar0` address, cfg_read /
# cfg_write, and an `mm` DMA memory manager.
#
# The dext<->client ABI -- method selectors and memory types -- is
# defined in macos/TGDext/tg_dext.h; the constants here mirror it.

import ctypes
import ctypes.util

from mm.macos import MacOSMemMgr

# --- dext ABI (mirror of macos/TGDext/tg_dext.h) -------------------------

kTGConfigRead    = 0    # scalar in: (offset);        scalar out: (value)
kTGConfigWrite   = 1    # scalar in: (offset, value); scalar out: ()
kTGGetBar0Info   = 2    # scalar in: ();              scalar out: (size)
kTGAllocDMA      = 3    # scalar in: (size);          scalar out: (handle, iova)
kTGFreeDMA       = 4    # scalar in: (handle);        scalar out: ()
kTGWaitInterrupt = 5    # async: completes on the next device interrupt

kTGMemoryBar0    = 0            # IOConnectMapMemory type: PCI BAR 0
kTGMemoryDMA     = 0x100        # IOConnectMapMemory type: DMA buffer base
kTGMaxDMABuffers = 16

# The IOService class the dext publishes (its Info.plist IOUserClass).
TG_DEXT_CLASS = "TGPCIDevice"

# --- IOKit.framework / Mach bindings ------------------------------------

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

MACH_PORT_RIGHT_RECEIVE = 1
MACH_RCV_MSG            = 0x00000002
MACH_RCV_TIMEOUT        = 0x00000100
MACH_RCV_TIMED_OUT      = 0x10004003

_iokit.IOServiceMatching.restype = ctypes.c_void_p
_iokit.IOServiceMatching.argtypes = [ctypes.c_char_p]

# IOServiceNameMatching matches a registry node by its name. A dext's
# in-kernel node is an IOUserService *named* after the dext class
# (TGPCIDevice); IOServiceMatching matches by provider class and would
# miss it, so the node is found by name instead.
_iokit.IOServiceNameMatching.restype = ctypes.c_void_p
_iokit.IOServiceNameMatching.argtypes = [ctypes.c_char_p]

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

_iokit.IOConnectCallAsyncScalarMethod.restype = kern_return_t
_iokit.IOConnectCallAsyncScalarMethod.argtypes = [
    mach_port_t, ctypes.c_uint32, mach_port_t,
    ctypes.POINTER(ctypes.c_uint64), ctypes.c_uint32,
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

_libc.mach_port_allocate.restype = kern_return_t
_libc.mach_port_allocate.argtypes = [mach_port_t, ctypes.c_int,
                                     ctypes.POINTER(mach_port_t)]

_libc.mach_msg.restype = kern_return_t
_libc.mach_msg.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint32,
                           ctypes.c_uint32, mach_port_t, ctypes.c_uint32,
                           mach_port_t]


def _mach_task_self():
    # mach_task_self() is a macro for the global mach_task_self_ port.
    return mach_port_t.in_dll(_libc, "mach_task_self_").value


def _kr(kr):
    return "0x%08x" % (kr & 0xffffffff)


class MacOSInterface(object):
    def __init__(self):
        self._service = 0
        self._int_port = 0
        self._int_armed = False
        matching = _iokit.IOServiceNameMatching(TG_DEXT_CLASS.encode())
        if not matching:
            raise Exception("IOServiceNameMatching(%s) failed" % TG_DEXT_CLASS)
        self._service = _iokit.IOServiceGetMatchingService(
            kIOMainPortDefault, matching)
        if not self._service:
            raise Exception(
                "ThunderGate dext not found -- is the %s system extension "
                "loaded and a Tigon3 device present? See doc/INSTALL.macos.md"
                % TG_DEXT_CLASS)

    def __enter__(self):
        self._attach()
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
        self._int_armed = False     # a fresh connection: dext not armed

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

        self.mm = MacOSMemMgr(self)

    def _detach(self):
        mm = getattr(self, "mm", None)
        if mm is not None:
            mm.release()
            self.mm = None
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

    # --- external-method plumbing ---------------------------------------

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

    # --- config space ---------------------------------------------------

    def cfg_read(self, offset):
        assert 0 <= offset < 0x1000
        return self._call_scalar(kTGConfigRead, [offset], 1)[0] & 0xffffffff

    def cfg_write(self, offset, val):
        assert 0 <= offset < 0x1000
        self._call_scalar(kTGConfigWrite, [offset, val & 0xffffffff], 0)

    # --- DMA buffers-----------------------------------------------------
    # Called by mm/macos.py:MacOSMemMgr.

    def _dma_alloc(self, size):
        handle, iova = self._call_scalar(kTGAllocDMA, [size], 2)
        return handle, iova

    def _dma_free(self, handle):
        self._call_scalar(kTGFreeDMA, [handle], 0)

    def _dma_map(self, handle):
        addr = ctypes.c_uint64(0)
        size = ctypes.c_uint64(0)
        kr = _iokit.IOConnectMapMemory64(
            self._conn, kTGMemoryDMA + handle, _mach_task_self(),
            ctypes.byref(addr), ctypes.byref(size), kIOMapAnywhere)
        if kr != kIOReturnSuccess:
            raise Exception("mapping DMA buffer %d failed (%s)"
                            % (handle, _kr(kr)))
        return addr.value

    def _dma_unmap(self, handle, vaddr):
        _iokit.IOConnectUnmapMemory64(self._conn, kTGMemoryDMA + handle,
                                      _mach_task_self(), vaddr)

    # --- interrupts------------------------------------------------------

    def wait_interrupt(self, timeout_ms=1000):
        '''Block until the device interrupts, or the timeout elapses.

        Returns True on an interrupt, False on timeout. The dext delivers
        the async completion of kTGWaitInterrupt as a Mach message; this
        receives it directly. The TAP driver (asyncio) runs this in an
        executor thread.'''
        if self._int_port == 0:
            port = mach_port_t(0)
            kr = _libc.mach_port_allocate(_mach_task_self(),
                                          MACH_PORT_RIGHT_RECEIVE,
                                          ctypes.byref(port))
            if kr != kIOReturnSuccess:
                raise Exception("mach_port_allocate failed (%s)" % _kr(kr))
            self._int_port = port.value

        if not self._int_armed:
            ref = (ctypes.c_uint64 * 8)()
            kr = _iokit.IOConnectCallAsyncScalarMethod(
                self._conn, kTGWaitInterrupt, self._int_port,
                ref, 1, None, 0, None, None)
            if kr != kIOReturnSuccess:
                raise Exception("arming interrupt wait failed (%s)" % _kr(kr))
            self._int_armed = True

        buf = (ctypes.c_uint8 * 1024)()
        kr = _libc.mach_msg(buf, MACH_RCV_MSG | MACH_RCV_TIMEOUT, 0,
                            ctypes.sizeof(buf), self._int_port,
                            timeout_ms, 0)
        if (kr & 0xffffffff) == MACH_RCV_TIMED_OUT:
            return False
        if kr != kIOReturnSuccess:
            raise Exception("mach_msg receive failed (%s)" % _kr(kr))
        self._int_armed = False     # the completion was consumed
        return True
