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
import tglib as tg
import clib as c
from device import tg3_blocks
from rflip import rflip
import struct
import socket
from time import sleep
import hashlib

usleep = lambda x: sleep(x / 1000000.0)

def rread(dev, ofs, count=16):
    dev.mem.write_dword(0xb54, ofs)
    dev.mem.write_dword(0xb58, count)
    dev.mem.write_dword(0xb50, 0x88b50003)

    cnt = 0
    while dev.mem.read_dword(0xb50) == 0x88b50003:
        if dev.rxcpu.status.invalid_data_access:
            raise Exception("invalid data access")
        cnt += 1
        if cnt > 10:
            raise Exception("rxcpu read timed out")
        usleep(10)

    if dev.mem.read_dword(0xb50) != 0x88b50400:
        print "unknown rxcpu response %08x" % dev.mem.read_dword(0xb50)
        raise Exception("unknown rxcpu response found at 0xb50: %08x" % dev.mem.read_dword(0xb50))

    return dev.mem.read(0xb54, 64)

def try_read(dev, ofs, count = 16):
    r = None
    try:
        r = rread(dev, ofs, count)
    except:
        dev.rxcpu.mode.halt = 1
        dev.mem.write_dword(0xb50, 0x4b657654)
        dev.rxcpu.mode.reset = 1
        while dev.mem.read_dword(0xb50) != 0xb49a89ab:
            usleep(10)

    return r

def map_mem(dev):
    m = {}
    with open("mem.map", "w") as f:
        with open("data.rd", "w") as d:
            for i in range(0xfffff):
                addr = i << 12
                if 0 == (i % 0x400):
                    print "now at %x" % addr
                v = try_read(dev, addr)
                if v is None:
                    d.write("%08x: \n" % addr)
                    v = 0
                else:
                    d.write("%08x: %s\n" % (addr, ''.join(["%02x" % ord(j) for j in v])))
                    v = hashlib.sha1(v).hexdigest()
                d.flush()
                try: m[v] += [addr]
                except: m[v] = [addr]
                f.write("%08x: %s\n" % (addr, v))
                f.flush()
    return m

def state_save(dev):
    return (dev.mem.save_mem(), dev.reg_save())

def state_diff(dev, state):
    m = dev.mem.save_mem()
    r = dev.reg_save()
    mem_diff(state[0], m)
    analyze_diff(reg_diff(state[1], r))
    return (m, r)        

def collect_unnamed_registers(dev):
    u = {}
    for i in range(8192):
        v = dev.reg[i]
        if v > 0:
            bn, br, s, l = whats_at(i * 4)
            if br[:4] == "ofs_" or br[:3] == "unk" or br[:3] == "unu" or br[:5] == "reser":
                if not bn in u:
                    u[bn] = {}
                u[bn][br] = v

def regsearch(dev, val, mask=0xffffffff):
    for i in range(0, 0x8000, 4):
        tmp = dev.reg[i >> 2]
        if ((val ^ tmp) & mask) == 0:
            print "value %08x found at register offset %04x" % (tmp, i)

def regcheck(dev):
    for i in range(0, 0x8000, 4):
        tmp = dev.reg[i >> 2]
        dev.pci.reg_base_addr = i
        _ = dev.pci.reg_base_addr
        tmp2 = dev.pci.reg_data
        dev.interface.cfg_write(0x78, i)
        tmp3 = dev.interface.cfg_read(0x80)
        dev.mem.write_dword(0xb54, 0xc0000000 + i)
        dev.mem.write_dword(0xb58, 1)
        dev.mem.write_dword(0xb50, 0x88b50003)
        while (dev.mem.read_dword(0xb50) == 0x88b50003):
            usleep(10)
        tmp4 = dev.mem.read_dword(0xb54)
        if tmp != tmp2 or tmp2 != tmp3 or tmp3 != tmp4 or tmp4 != tmp:
            block, name, _, _ = whats_at(i)
            print "views differ at \"%s.%s\", offset %04x: %08x %08x %08x %08x" % (block, name, i, tmp, tmp2, tmp3, tmp4)

def mem_diff(start, end):
    print "memory diff: "

    offset = 0
    quiesced = True
    while offset < len(start):
        scur = start[offset:offset+8]
        ecur = end[offset:offset+8]

        if scur == ecur:
            if not quiesced:
                print " ..."
                quiesced = True
        else:
            quiesced = False
            print " 0x%04x:" % offset,
            for i in range(0, 8):
                print "%02x" % ord(scur[i]),

            print " -> ",
            for i in range(0, 8):
                print "%02x" % ord(ecur[i]),

            print

        offset += 8
    print "memory diff ends"
    print

def reg_diff(old, cur):
    m = create_string_buffer(len(cur) * 4)
    for i in range(0, len(cur) * 4):
        c = ((cur[i>>2]) >> ((i % 4) * 8)) & 0xff
        o = ((old[i>>2]) >> ((i % 4) * 8)) & 0xff
        if c == 0:
            if o == 0:
                m[i] = ' '
            else:
                m[i] = '!'
        else:
            if o == c:
                m[i] = '.'
            else:
                m[i] = "!"
    return (m, old, cur)

def dump_diff(diff):
    m = diff[0]
    print
    for i in range(0, len(m), 64):
        print "%04x: %s" % (i, m[i:i+64])
    print

def disp_diff(a, b, ilvl=0, title=""):
    for f in a._fields_:
        assert f in b._fields_
        if hasattr(a, "_anonymous_") and f[0] in a._anonymous_:
            continue
        av = getattr(a, f[0])
        bv = getattr(b, f[0])
        if hasattr(av, "_fields_"):
            if len(title) > 0:
                title += "\n"
            title += "%s%s:" % (" " * ilvl, f[0])
            disp_diff(av, bv, ilvl+1, title)
        else:
            if av != bv:
                if len(title) > 0:
                    print title
                    title = ""
                print "%s%s:" % (" " * ilvl, f[0]),
                print "\t" * (6 - (len(f[0]) + ilvl + 2) / 8),
                print "%x" % av,
                print "\t" * (3 - (len("%x" % av) + 1) / 8),
                print "%x" % bv


def analyze_diff(diff):
    m = diff[0]
    i = 0
    deltas = []
    dstart = None
    dlen = 0
    while i < len(m):
        if dstart:
            if m[i] == "!":
                dlen += 1
            else:
                deltas += [(dstart, dlen)]
                dstart = None
                dlen = 0
        else:
            if m[i] == "!":
                dstart = i
                dlen = 1
        i += 1
    if dstart:
        deltas += [(dstart, dlen)]

    diffs_at = {}
    for d in deltas:
        for i in range(0, d[1]):
            block, reg, offset, size = whats_at(d[0] + i)
            desc = "%s.%s" % (block, reg)
            if not desc in diffs_at:
                diffs_at[desc] = (offset, size)

    print "register diff:"
    for d in sorted(diffs_at.keys(), key=lambda x: diffs_at[x][0]):
        offset, size = diffs_at[d]
        title = "%s (%04x-%04x)" % (d, offset, (offset + size) - 1)
        i = size
        oldval = 0
        newval = 0
        while i >= 4:
            oldval <<= 32
            newval <<= 32
            oldval |= diff[1][(offset + (size - i)) >> 2]
            newval |= diff[2][(offset + (size - i)) >> 2]
            i -= 4
        assert i == 0
        st = d.split(".")
        count = len(st)
        try:
            bt = getattr(tg, "%s_regs" % st[len(st) - count])
            t = rflip(bt)
            count -= 1
            while count > 0:
                piece = st[len(st) - count]
                found = False

                for f in t._fields_:
                    if f[0] == piece:
                        t = f[1]
                        found = True
                        break
                if not found:
                    break
                count -= 1
        except:
            t = c_uint
        if hasattr(t, '_fields_') and sizeof(t) == 4:
            ob = create_string_buffer(struct.pack("I", oldval))
            o = cast(ob, POINTER(t))[0]
            nb = create_string_buffer(struct.pack("I", newval))
            n = cast(nb, POINTER(t))[0]
            print " %s" % title
            print ("  was %0" + str(size * 2) + "x, now %0" + str(size * 2) + "x") % (oldval, newval)
            disp_diff(o, n, 3)
        else:
            print (" %s:\t\t%0" + str(size * 2) + "x\t\t%0" + str(size * 2) + "x") % (title, oldval, newval)
    print "register diff ends"
    print

def whats_at(addr):
    assert addr < 0x8000
    block_name = "unknown"
    reg_name = "unknown"
    b = tg3_blocks[0]
    for nb in tg3_blocks[1:]:
        if nb[1] > addr:
            break
        else:
            b = nb
    block_name, block_offset, block_t = b
    
    reg_offset = (addr - block_offset) & 0xffc
    reg_name = "ofs_%02x" % reg_offset
    reg_size = 4
    reg_t = c_uint32
    for f in block_t._fields_:
        if hasattr(block_t, "_anonymous_") and f[0] in block_t._anonymous_:
            continue
        ofs = getattr(block_t, f[0]).offset
        sz = getattr(block_t, f[0]).size
        if (addr - block_offset) >= ofs and (addr - block_offset) < (ofs + sz):
            reg_name = f[0]
            reg_t = f[1]
            reg_offset = getattr(block_t, reg_name).offset
            reg_size = getattr(block_t, reg_name).size

    try:
        if Array in reg_t.__bases__:
            reg_size = sizeof(reg_t._type_)
            index = (addr - (reg_offset + block_offset)) / reg_size
            reg_name = reg_name + ("[0x%x]" % index)
            reg_offset += index * reg_size
            reg_t = reg_t._type_
    except: 
        pass
    try:
        if reg_size > 4:
            for f in reg_t._fields_:
                if hasattr(reg_t, "_anonymous_") and f[0] in reg_t._anonymous_:
                    continue
                field = getattr(reg_t, f[0])
                ofs = field.offset
                sz = field.size
                if (addr - (reg_offset + block_offset)) >= ofs and (addr - (reg_offset + block_offset)) < (ofs + sz):
                    reg_t = f[1]
                    reg_offset += ofs
                    reg_size = sizeof(reg_t)
                    reg_name += (".%s" % f[0])
                    break
    except:
        pass
    return (block_name, reg_name, block_offset + reg_offset, reg_size)

def __blargh():
            if hasattr(t, "_anonymous_"):
                fields = [f for f in t._fields_ if f[0] not in t._anonymous_]
                anonf = [f[1] for f in t._fields_ if f[0] in t._anonymous_]
                while len(anonf) > 0:
                    a = anonf.pop()
                    if hasattr(a, "_anonymous_"):
                        fields += [f for f in a._fields_ if f[0] not in a._anonymous_]
                        anonf += [f[1] for f in a._fields_ if f[0] in a._anonymous_]
                    else:
                        fields += [f for f in a._fields_]
            else:
                fields = t._fields_
            for f in fields:
                ov = getattr(o, f[0])
                nv = getattr(n, f[0])
                if hasattr(ov, "_fields_"):
                    print "  %s:" % f[0]
                    for g in t._fields_:
                        sov = getattr(o, g[0])
                        snv = getattr(n, g[0])
                        if sov != snv:
                            tabs = (6 - (len(g[0]) + 3) / 8)
                            fmtstr = "   %s" + ('\t' * tabs) + "%x\t\t%x"
                            print fmtstr % (g[0], sov, snv)
                else:
                    if ov != nv:
                        tabs = (6 - (len(f[0]) + 2) / 8)
                        fmtstr = "  %s" + ('\t' * tabs) + "%x\t\t%x"
                        print fmtstr % (f[0], ov, nv)
