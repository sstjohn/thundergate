from winlib import *

class TapWinInterface(object):
    def __init__(self, dev):
        self.dev = dev
        self.mm = dev.interface.mm

    def __enter__(self):
        self.tfd = create_tap_if()
        self.tg_evt = IoctlAsync(IOCTL_TGWINK_PEND_INTR, self.dev.interface.cfgfd, 8)
        self.tap_evt = ReadAsync(self.tfd, 1518)
        self.events = (HANDLE * 2)(self.tg_evt.req.hEvent, self.tap_evt.req.hEvent)
        self.tg_is_ready = self.tg_evt.check
        self.tap_is_ready = self.tap_evt.check
        self.tg_evt.submit()
        return self

    def __exit__(self):
        self.tap_evt.reset(False)
        self.tg_evt.reset(False)
        del self.tap_is_ready
        del self.tg_is_ready
        del self.events
        del self.tap_evt
        del self.tg_evt

        del_tap_if(self.tfd)

    def _wait_for_something(self):
        res = WaitForMultipleObjects(2, cast(pointer(self.events), POINTER(c_void_p)), False, INFINITE)
        if WAIT_FAILED == res:
            raise WinError()

    def _get_serial(self):
        serial = cast(self.tg_evt.buffer, POINTER(c_uint64)).contents.value
        self.tg_evt.reset()
        return serial
 
    def _get_packet(self):
        if verbose:
            print "[+] getting a packet from tap device...",
        pkt_len = self.tap_evt.pkt_len
        pkt = self.mm.alloc(pkt_len)
        RtlCopyMemory(pkt, self.tap_evt.buffer, pkt_len)
        self.tap_evt.reset()
        if verbose:
            print "read %d bytes" % pkt_len
        return (pkt, pkt_len)

    def _write_pkt(self, pkt, length):
        o = OVERLAPPED(hEvent = CreateEvent(None, True, False, None))
        try:
            if verbose:
                print "[!] attempting to write to the tap device...",
            if not WriteFile(self.tfd, pkt, length, None, pointer(o)):
                err = WinError()
                if err.winerror != ERROR_IO_PENDING:
                    raise err
                if WAIT_FAILED == WaitForSingleObject(o.hEvent, INFINITE):
                    raise WinError()
            print "wrote %d bytes" % o.InternalHigh
        finally:
            CloseHandle(o.hEvent)

    def _set_tapdev_status(self, connected):
        if verbose:
            print "[+] setting tapdev status to %s" % ("up" if connected else "down")
        o = OVERLAPPED(hEvent = CreateEvent(None, True, False, None))
        try:
            val = c_int32(1 if connected else 0)
            if not DeviceIoControl(self.tfd, TAP_WIN_IOCTL_SET_MEDIA_STATUS, pointer(val), 4, pointer(val), 4, None, pointer(o)):
                err = WinError()
                if err.winerror == ERROR_IO_PENDING:
                    if WAIT_FAILED == WaitForSingleObject(o.hEvent, INFINITE):
                        raise WinError()
                elif err.winerror == 0:
                    pass
                else:
                    raise err
            if connected:
                self.tap_evt.submit()
            else:
                self.tap_evt.reset(False)
        finally:
            CloseHandle(o.hEvent)