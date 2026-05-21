#!/usr/bin/env python3
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

# RAM-load fw.img and drive the on-core REPL through the PCIe-side lgate
# (INTERP_EVAL_CMD): the host writes the input line into shmem, raises
# sw_event_0, and reads back a length-prefixed console buffer. Exercises
# zForth and uBASIC including the soft __mulsi3 / __divsi3 paths libgcc
# provides under -mtigon.

import os
import platform
import struct
import sys
from time import sleep, monotonic

PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJ_ROOT, "py"))

from device import Device
import tglib as tg

GATE_SHMEM_BASE = 0xe00
CTRL_ETYPE = 0x88b5
FW_LOAD_ADDR = 0x08000000


def _word_at(dev, off):
    return dev.mem.read_dword(GATE_SHMEM_BASE + off)

def _put_word(dev, off, val):
    dev.mem.write_dword(GATE_SHMEM_BASE + off, val)

def lgate_eval(dev, line, timeout=2.0):
    line = line.encode("utf-8") if isinstance(line, str) else line
    n = len(line)
    if n > 0x150 - 0x10:
        raise ValueError("input too long for GATE_SHMEM")

    # Byte-stream payload: the Tigon3 PCIe path byte-swaps dwords (so u32
    # writes round-trip with the BE rxcpu), which scrambles a string read
    # bytewise on the device. Pack each 4-byte chunk as big-endian so the
    # net byte order at lgate_base[0x10..] matches the source string.
    pad = (-n) & 3
    payload = line + b'\x00' * pad
    for i in range(0, len(payload), 4):
        _put_word(dev, 0x10 + i, struct.unpack(">I", payload[i:i+4])[0])

    _put_word(dev, 0x04, n)                                   # arg1 = byte length
    _put_word(dev, 0x00, (CTRL_ETYPE << 16) | tg.INTERP_EVAL_CMD)

    dev.grc.rxcpu_event.sw_event_0 = 1
    deadline = monotonic() + timeout
    while dev.grc.rxcpu_event.sw_event_0:
        if monotonic() > deadline:
            raise TimeoutError("rxcpu did not clear sw_event_0 within %ss" % timeout)
        sleep(0.001)

    head = _word_at(dev, 0x00)
    cmd  = head & 0xffff
    if cmd != (tg.INTERP_EVAL_REPLY & 0xffff):
        raise RuntimeError("unexpected reply cmd word: %08x" % head)

    rlen = _word_at(dev, 0x04)
    if rlen > 256:
        raise RuntimeError("reply length %d out of range" % rlen)
    out = bytearray()
    for i in range(0, (rlen + 3) & ~3, 4):
        out += struct.pack(">I", _word_at(dev, 0x08 + i))
    return bytes(out[:rlen]).decode("utf-8", errors="replace")


def boot_firmware(dev, image_path):
    with open(image_path, "rb") as f:
        blob = f.read()
    print("[smoketest] loaded %s (%d bytes) for SRAM load at %08x" %
          (image_path, len(blob), FW_LOAD_ADDR))
    dev.rxcpu.image_load(FW_LOAD_ADDR, blob)
    dev.rxcpu.go(FW_LOAD_ADDR)
    sleep(0.25)


def run_cases(dev, cases):
    fails = 0
    for label, line, expected in cases:
        try:
            out = lgate_eval(dev, line)
        except Exception as e:
            print("[FAIL] %-32s  (eval raised: %s)" % (label, e))
            fails += 1
            continue
        ok = all(e in out for e in expected) if isinstance(expected, (list, tuple)) else expected in out
        tag = "[ ok ]" if ok else "[FAIL]"
        printable = out.replace("\n", "\\n").replace("\r", "\\r")
        print("%s %-32s  in=%r  out=%r" % (tag, label, line, printable))
        if not ok:
            fails += 1
    return fails


def main():
    if platform.system() != "Darwin":
        print("smoketest is wired up for macOS only; the dext + MacOSInterface path",
              file=sys.stderr)
        return 2

    from interfaces.macos import MacOSInterface
    intf = MacOSInterface()

    fw_img = os.path.join(PROJ_ROOT, "fw", "fw.img")
    if not os.path.exists(fw_img):
        print("missing %s; run `make -C fw` first" % fw_img, file=sys.stderr)
        return 2

    with Device(intf) as dev:
        dev.init()
        boot_firmware(dev, fw_img)

        cases = [
            # zForth is the default at startup. con_puti emits "<n> " for "." .
            ("zforth: 2+3",              "2 3 + . cr",     "5 "),
            ("zforth: 7*6 (soft mul)",   "7 6 * . cr",     "42 "),
            ("zforth: 100/7 (soft div)", "100 7 / . cr",   "14 "),
            ("switch to basic",          "basic",          "[uBASIC]"),
            ("ubasic: 2+3",              "print 2+3",      "5"),
            ("ubasic: 7*6 (soft mul)",   "print 7*6",      "42"),
            ("ubasic: 100/7 (soft div)", "print 100/7",    "14"),
            ("switch back to forth",     "forth",          "[zForth]"),
            ("zforth: still alive",      "1 1 + . cr",     "2 "),
        ]

        fails = run_cases(dev, cases)
        if fails:
            print("[smoketest] %d/%d cases failed" % (fails, len(cases)))
            return 1
        print("[smoketest] all %d cases passed" % len(cases))
        return 0


if __name__ == "__main__":
    sys.exit(main())
