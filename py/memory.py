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
from socket import htonl
import struct

def is_bf(t):
    try:
        m_is_bf = [len(f) == 3 for f in t._fields_]
        return reduce(lambda x, y: x and y, m_is_bf)
    except:
        return False

def bf_build_prop(ofs, first, bits):
    rlen = 1
    if bits > 8:
        rlen = bits >> 3

    ct = None
    
    if rlen == 1:
        ct = c_ubyte
    if rlen == 2:
        ct = c_ushort
    if rlen == 3:
        rlen += 1
    if rlen == 4:
        ct = c_uint
    if ct == None and rlen < 8:
        rlen = 8
    if rlen == 8:
        ct = c_ulong

    assert ct is not None

    def getter(self):
        data = self._dev.mem.read(self._offset + ofs, rlen)
        tmp = cast(data, POINTER(ct)).contents.value
        mask = 1 << (first + bits) - 1
        mask |= mask - 1
        tmp &= mask
        tmp >>= first
        return tmp

    def setter(self, value):
        #print "field starts at %02x:%02x, extends %02x bits" % (self._offset + ofs, first, bits)
        data = self._dev.mem.read(self._offset + ofs, rlen)
        tmp = cast(data, POINTER(ct)).contents.value
        #print ("read %0" + str(rlen * 2) + "x") % tmp
        mask = 1 << (first + bits) - 1
        mask |= mask - 1
        if first > 0:
            xmask = 1 << first - 1
            xmask |= xmask - 1
            mask &= ~xmask

        #print ("mask is %0" + str(rlen * 2) + "x") % mask 
        #print ("existing data: %0" + str(rlen * 2) + "x") % (tmp & ~mask)
        #print ("new data: %0" + str(rlen * 2) + "x") % ((value << first) & mask)
        tmp = (tmp & ~mask) | ((value << first) & mask)
        #print ("want to write %0" + str(rlen * 2) + "x") % tmp
        tmp = ct(tmp)
        data = cast(byref(tmp), POINTER(c_char * rlen)).contents.raw
        self._dev.mem.write(self._offset + ofs, data)

    return property(getter, setter)

def gen_bf_proxy(t):
    w = type("%s_w" % t.__name__, (), {})
    def w_init(self, dev, offset):
        self._dev = dev
        self._offset = offset

    w.__init__ = w_init

    byte = 0
    bit = 0
    for f in t._fields_:
        setattr(w, f[0], bf_build_prop(byte, bit, f[2]))
        bit += f[2]
        if bit > 7:
            byte += (bit >> 3)
            bit %= 8

    return w

def c_build_prop(fofs, fsize, ftype):
    def getter(self):
        data = self._dev.mem.read(self._offset + fofs, fsize)
        tmp = cast(data, POINTER(ftype))
        try:
            return tmp.contents.value
        except:
            tmp = tmp.contents
            tmp._buf = data
            return tmp

    def setter(self, value):
        tmp = ftype(value)
        data = cast(byref(tmp), POINTER(c_char * fsize))
        self._dev.mem.write(self._offset + fofs, data.contents.raw)

    return property(getter, setter)

def gen_mem_proxy(t):
    w = type("%s_w" % t.__name__, (), {})
    needs_init = []

    for f in t._fields_:
        if is_bf(f[1]):
            bft = gen_bf_proxy(f[1])
            setattr(w, f[0], bft)
            needs_init += [(f[0], bft, getattr(t, f[0]).offset)]
        elif hasattr(f[1], "_fields_"):
            mpt = gen_mem_proxy(f[1])
            setattr(w, f[0], mpt)
            needs_init += [(f[0], mpt, getattr(t, f[0]).offset)] 
        else:
            setattr(w, f[0], c_build_prop(getattr(t, f[0]).offset, getattr(t, f[0]).size, f[1]))
    
    def w_init(self, dev, offset):
        self._dev = dev
        self._offset = offset
        for o in needs_init:
            setattr(self, o[0], o[1](dev, offset + o[2]))

    w.__init__ = w_init

    return w

class Memory(object):
    def __init__(self, dev):
        self.dev = dev

    def _set_window(self, addr, verbose = 1):
        window = addr & 0xffff8000
        offset = addr & 0x00007fff

        if self.dev.pci.mem_base_addr != window:
            if verbose:
                print "[+] shifting memory aperature to %06x" % window
            self.dev.pci.mem_base_addr = window

        return window, offset

    def read(self, addr, length, verbose = 0):
        rlength = length

        window, offset = self._set_window(addr, verbose = verbose)
        rstart = offset
        if offset % 4:
            rstart -= offset % 4
            rlength += offset % 4

        if rlength % 4:
            rlength += 4 - (rlength % 4)
        
        if verbose:
            print "[.] reading memory length %x at %08x:%04x" % (rlength, addr ^ offset, rstart)

        tmp = ''
        assert rlength > 0

        if (rlength + rstart) <= 0x8000:
            tmp = cast(self.dev.bar0 + 0x8000 + rstart, POINTER(c_uint * (rlength >> 2))).contents[:]
            tmp = (c_uint * (rlength >> 2))(*tmp)
            tmp = cast(tmp, POINTER(c_char * rlength)).contents.raw
        else:
            d = 0x8000 - rstart
            tmp = self.read(window + rstart, d, verbose)
            tmp += self.read(window + 0x8000, rlength - d, verbose)
        

        tmp = tmp[offset % 4:length + (offset % 4)]

        return tmp

    def read_dword(self, addr):
        return struct.unpack("I", self.read(addr, 4))[0]

    def write(self, addr, value, verbose = 0):
        if addr >= 0x08000000 and addr < 0x08010000:
            addr = (addr & 0xffff) | 0x30000
        window, offset = self._set_window(addr)
        wstart = offset 
        if wstart % 4:
            wstart -= wstart % 4
            value = self.read(window + wstart, offset - wstart, verbose) + value


        if len(value) % 4:
            value = value + self.read(window + wstart + len(value), 4 - (len(value) % 4), verbose)

        if verbose:
            print "[.] writing memory length %x at %08x:%04x" % (len(value), window, wstart)

        length = len(value) >> 2

        if (len(value) + wstart <= 0x8000):
            dest = cast(self.dev.bar0 + 0x8000 + wstart, POINTER(c_uint))
            src = cast(value, POINTER(c_uint * length)).contents
            for i in range(length):
                dest[i] = src[i]
        else:
            d = 0x800 - wstart
            self.write(window + wstart, value[:d], verbose)
            self.write(window + 0x8000, value[d:], verbose)

    def write_dword(self, addr, value):
        s = struct.pack("I", value)
        self.write(addr, s)

    def map_struct(self, name, t, address, count=1):
        wt = gen_mem_proxy(t)
        if count == 1:
            setattr(self, name, wt(self.dev, address))
        else:
            tmp = []
            for i in range(count):
                tmp.append(wt(self.dev, address + i * sizeof(t)))
            setattr(self, name, tmp)

    def save_mem(self):
        return self.read(0, 0x1a000)
