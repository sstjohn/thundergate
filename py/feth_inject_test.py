#!/usr/bin/env python3
'''
ThunderGate -- isolation test for the _aiotap macOS feth plumbing.

Creates a throwaway feth pair and checks, in both directions, that a frame
written to a PF_NDRV socket on one end is seen by a BPF reader on the
other. This is exactly the hop _put_tap_packet depends on, with the NIC
and the dext taken out of the picture -- so a failure here is purely in
the feth / BPF / NDRV plumbing, not the driver.

Run as root. With no arguments it makes a throwaway pair and tests both
directions. Given two interface names it probes that live pair instead
(host first, nic second) -- so, while the driver is running:

    sudo .venv/bin/python3 py/feth_inject_test.py feth20 feth21
'''
import importlib.util
import os
import select
import struct
import sys
import time

_macos_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "_aiotap", "macos.py")
_spec = importlib.util.spec_from_file_location("tg_macos_probe", _macos_path)
macos = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(macos)


def _drain(fd, blen):
    '''Read one BPF buffer and split it into the frames it carries.'''
    out = []
    data = os.read(fd, blen)
    off = 0
    while off + macos._BPF_HDRLEN + 2 <= len(data):
        caplen = struct.unpack_from("I", data, off + macos._BPF_CAPLEN)[0]
        hdrlen = struct.unpack_from("H", data, off + macos._BPF_HDRLEN)[0]
        out.append(bytes(data[off + hdrlen:off + hdrlen + caplen]))
        off = macos._wordalign(off + hdrlen + caplen)
    return out


def _probe(label, ndrv_fd, bpf_fd, blen, tag):
    '''Write one tagged frame to ndrv_fd; report whether bpf_fd sees it.'''
    frame = (b'\xff\xff\xff\xff\xff\xff' + b'\x02tgate'
             + b'\x88\xb5' + tag).ljust(64, b'\0')
    while select.select([bpf_fd], [], [], 0)[0]:
        os.read(bpf_fd, blen)
    n = os.write(ndrv_fd, frame)
    deadline = time.time() + 2.0
    while True:
        timeout = deadline - time.time()
        if timeout <= 0:
            break
        if not select.select([bpf_fd], [], [], timeout)[0]:
            break
        for f in _drain(bpf_fd, blen):
            if tag in f:
                print("  %-28s PASS  (wrote %d, got %d bytes back)"
                      % (label, n, len(f)))
                return True
    print("  %-28s FAIL  (wrote %d, nothing arrived in 2s)" % (label, n))
    return False


def main():
    if os.geteuid() != 0:
        print("must run as root (feth create / bpf / PF_NDRV)")
        return 2

    args = sys.argv[1:]
    if len(args) == 2:
        host, nic = args
        created = False
        print("probing live pair: host=%s  nic=%s" % (host, nic))
    else:
        host, nic = macos._create_feth_pair()
        created = True
        print("throwaway pair: host=%s  nic=%s" % (host, nic))

    try:
        host_bpf, host_blen = macos._open_bpf(host)
        nic_ndrv = macos._open_ndrv(nic)
        time.sleep(0.3)
        ok = _probe("inject   nic->host (RX path)",
                    nic_ndrv, host_bpf, host_blen, b'TG-INJECT-NIC2HOST')

        if created:
            # A control run only makes sense on a throwaway pair: on a
            # live pair the host->nic frame would be caught by the running
            # driver's BPF and forwarded to the NIC.
            nic_bpf, nic_blen = macos._open_bpf(nic)
            host_ndrv = macos._open_ndrv(host)
            time.sleep(0.2)
            ok &= _probe("control  host->nic",
                         host_ndrv, nic_bpf, nic_blen, b'TG-CONTROL-HOST2NIC')
        return 0 if ok else 1
    finally:
        if created:
            for f in (host, nic):
                try:
                    macos._ifconfig(f, "destroy")
                except Exception:
                    pass


if __name__ == "__main__":
    sys.exit(main())
