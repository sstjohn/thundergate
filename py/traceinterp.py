#!/usr/bin/env python

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

import os
import sys
import re
import tglib as fwtypes
import argparse

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../external/build"))

from socket import htonl, ntohl, htons, ntohs
from device import tg3_blocks

regmap = {}

for b in tg3_blocks:
    regmap[b[0]] = b[1]

cr_p = re.compile('\(([0-9a-f]{4}):([0-9a-f]{2}):([0-9a-f]{2})\.([0-9a-f]{1}), \@(0x[0-9a-f]{1,4}), len=(0x[0-9a-f])\)\s([0-9a-f]{1,8})\s*')
cw_p = re.compile('\(([0-9a-f]{4}):([0-9a-f]{2}):([0-9a-f]{2})\.([0-9a-f]{1}), \@(0x[0-9a-f]{1,4}), (0x[0-9a-f]{1,8}), len=(0x[0-9a-f])\)\s*')
rr_p = re.compile('\(([0-9a-f]{4}):([0-9a-f]{2}):([0-9a-f]{2})\.([0-9a-f]{1}):(region[0-9]{1})\+(0x[0-9a-f]{1,4}), (\d*)\) = (0x[0-9a-f]{1,8})\s*')
rw_p = re.compile('\(([0-9a-f]{4}):([0-9a-f]{2}):([0-9a-f]{2})\.([0-9a-f]{1}):(region[0-9]{1})\+(0x[0-9a-f]{1,4}), (0x[0-9a-f]{1,8}), (\d*)\)\s*')

def flip(value, length):
    nv = 0
    while length:
        nv = (nv << 1) | (value & 1)
        value >>= 1
        length -= 1

    return nv

def fdump(typ, value):
    ct = None
    if fwtypes.sizeof(typ) == 2:
        #nval = 0
        #for i in range(16):
        #    nval = (nval << 1) | (value & 1)
        #    value >>= 1
        #ct = fwtypes.c_short(nval)
        ct = fwtypes.c_short(flip(value, 16))
    else:
        #nval = 0
        #for i in range(32):
        #    nval = (nval << 1) | (value & 1)
        #    value >>= 1
        #ct = fwtypes.c_long(nval)
        ct = fwtypes.c_long(flip(value, 32))
    cp = fwtypes.pointer(ct)
    c = fwtypes.cast(cp, fwtypes.POINTER(typ))
    o = c.contents

    desc = ""
    for i in o._fields_:
        fname = i[0]
        if fname.startswith("reserved") and getattr(o, fname) == 0:
            continue
        blen = 0
        try:
            blen = i[2]
        except:
            blen = fwtypes.sizeof(i[1]) * 8
        desc += "%s: %x, " % (i[0], flip(getattr(o, i[0]), blen))

    desc = desc[:-2]
    return "{" + desc + "}"

def explain_r(reg, value, length):
    for i in regmap:
        if (reg & 0xff00) == regmap[i]:
            s = None
            try:
                s = getattr(fwtypes, "%s%s" % (i, "_regs"))
            except:
                return i

            for m in range(len(s._fields_)):
                name = s._fields_[m][0]
                typ = s._fields_[m][1]
                offset = getattr(s, name).offset
                size = fwtypes.sizeof(s._fields_[m][1])
                if (offset <= (reg & 0xff)) and ((offset + size) > (reg & 0xff)):
                    if length != size:
                        try:
                            for n in range(len(typ._fields_)):
                                tname = typ._fields_[n][0]
                                ttyp = typ._fields_[n][1]
                                toffset = getattr(typ, tname).offset
                                tsize = fwtypes.sizeof(ttyp)
                                if (offset + toffset) == (reg & 0xff) and tsize == length:
                                    name = "%s.%s" % (name, tname)
                                    typ = ttyp
                                    break
                        except:
                            print "WARNING (read %x, %s is %x in length)" % (length, s._fields_[m], size)
                    try:
                        return "%s.%s: %s" % (i, name, fdump(typ, value))
                    except:
                        return "%s.%s (%d)" % (i, name, length)
            return "(beyond %s)" % i
    return "(unknown)"



rbase = "0"
mbase = "0"

def describe_r(op, offset, length, value):
    global rbase
    global mbase
    ioff = int(offset, 16)
    ilen = int(length, 16)
    ival = int(value, 16)
    fmt = ""

    if op[0] == 'R':
        if ioff == 0x78:
            if ival == int(rbase, 16):
                return
        if ioff == 0x7c:
            if ival == int(mbase, 16):
                return
        if ioff == 0x80:
            describe_r("RRI", rbase, length, value)
            return
        if ioff == 0x84:
            describe_m("RMI", mbase, length, value)
            return
        fmt = "%s %08x == %08x %s"
    elif op[0] == 'W':
        if ioff == 0x78:
            rbase = "0x%08x" % ival
            return
        if ioff == 0x7c:
            mbase = "0x%08x" % ival
            return
        if ioff == 0x80:
            describe_r("WRI", rbase, length, value)
            return
        if ioff == 0x84:
            describe_m("WMI", mbase, length, value)
            return
        fmt = "%s %08x <- %08x %s"

    print fmt % (op, ioff, ival, explain_r(ioff, ival, ilen))

def describe_m(op, offset, length, value):
    ioff = int(offset, 16)
    ilen = int(length, 16)
    ival = int(value, 16)

    if op[0] == 'R':
        fmt = "%s %08x == %08x"
    elif op[0] == 'W':
        fmt = "%s %08x <- %08x"

    print fmt % (op, ioff, ival)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tracefile", type=file)
    pargs = parser.parse_args()
  
    line = pargs.tracefile.readline()
    while line != '':
        op, args = line.split(None,1)
        op = op.split(':')[1]
        if op == "vfio_region_read":
            _, domain, bus, device, function, region, offset, length, value, _ = rr_p.split(args)
            describe_r("RR ", offset, length, value)
        elif op == "vfio_region_write":
            _, domain, bus, device, function, region, offset, value, length, _ = rw_p.split(args)
            describe_r("WR ", offset, length, value)
        elif op == "vfio_pci_read_config":
            _, domain, bus, device, function, offset, length, value, _ = cr_p.split(args)
            describe_r("RC ", offset, length, value)
        elif op == "vfio_pci_write_config":
            _, domain, bus, device, function, offset, value, length, _ = cw_p.split(args)
            describe_r("WC ", offset, length, value)
        elif op == "vfio_intx_interrupt":
            print "intx_interrupt"
        elif op == "vfio_eoi":
            print "EOI"
        elif op == "vfio_initfn":
            print "init"
        elif op == "vfio_listener_region_add_ram":
            print "listener_region_add_ram"
        elif op == "vfio_listener_region_add_skip":
            print "listener_region_add_skip"
        elif op == "vfio_get_device":
            print "get_device"
        elif op == "vfio_populate_device_region":
            print "populate_device_region"
            pargs.tracefile.readline()
        elif op == "vfio_populate_device_config":
            print "populate_device_config"
            pargs.tracefile.readline()
        elif op == "vfio_early_setup_msix":
            print "early_setup_msix"
        elif op == "vfio_setup_msi":
            print "setup_msi"
        elif op == "vfio_enable_intx":
            print "enable_intx"
        elif op == "vfio_pci_reset":
            print "pci_reset"
        elif op == "vfio_disable_intx":
            print "disable_intx"
        elif op == "vfio_pci_reset_flr":
            print "pci_reset_flr"
        elif op == "vfio_listener_region_del":
            print "listener_region_del"
        elif op == "vfio_listener_region_del_skip":
            print "listener_region_del_skip"
        elif op == "vfio_update_irq":
            print "update_irq"
        else:
            print "UNKNOWN OP: %s" % line
        line = pargs.tracefile.readline()
