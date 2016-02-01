'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016 Saul St. John

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

import struct
import rflip
from socket import htonl
from ctypes import c_char, c_uint, cast, pointer, POINTER
from bidict import bidict

mips_regs = bidict(zero=0,
                   at=1,
                   v0=2, v1=3,
                   a0=4, a1=5, a2=6, a3=7,
                   t0=8, t1=9, t2=10, t3=11,
                   t4=12, t5=13, t6=14, t7=15,
                   s0=16, s1=17, s2=18, s3=19,
                   s4=20, s5=21, s6=22, s7=23,
                   t8=24, t9=25, 
                   k0=26, k1=27,
                   gp=28,
                   sp=29,
                   fp=30,
                   ra=31)

try:
    from capstone import *
    from capstone.mips import *
    if cs_version()[0] < 3:
        print "[-] capstone outdated - disassembly unavailable"
        _no_capstone = True
    else:
        _no_capstone = False
except:
    print "[-] capstone not present - disassembly unavailable"
    _no_capstone = True

from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

def to_x(v):
    if not v: return '0'
    r = struct.pack(">q", v)
    while r[0] in (chr(0), 0):
        r = r[1:]

    return " ".join(["%02x" % ord(c) for c in r])
    

class cpu(rflip.cpu):
    def _tr_addr(self, addr):
        if addr >= 0x08000000 and addr < 0x08010000:
            raddr = (addr & 0xffff) | 0x30000
        elif addr >= 0x40000000 and addr < 0x40010000:
            raddr = (addr & 0xffff) | 0x20000
        elif addr >= 0xc0000000:
            raddr = addr & 0xffff
        else:
            raise Exception("unable to translate address %x" % addr)
        return raddr

    def tr_read(self, addr, count):
        raddr = self._tr_addr(addr)
        
        try:
            tmp = []
            for i in range(0, count * 4, 4):
                self._dev.pci.reg_base_addr = raddr + i
                _ = self._dev.pci.reg_base_addr
                tmp += [htonl(self._dev.pci.reg_data)]

            tmp = (c_uint * count)(*tmp)
            return cast(pointer(tmp), POINTER(c_char * (count * 4))).contents.raw
        except:
            return self._dev.mem.read(addr, count * 4)

    def tr_write_dword(self, addr, dw):
        raddr = self._tr_addr(addr)
        self._dev.pci.reg_base_addr = raddr
        _ = self._dev.pci.reg_base_addr
        self._dev.pci.reg_data = dw

    def image_load(self, addr, blob):
        if not self.mode.halt:
            self.halt()

        raddr = self._tr_addr(addr)

        if (raddr % 0x10000) + len(blob) > 0x10000:
            raise Exception("image too big")
        
        if (len(blob) % 4) != 0:
            raise Exception("bad image length")

        for i in range(0, len(blob), 4):
            wd = struct.unpack("!I", blob[i:i+4])[0]
            self._dev.pci.reg_base_addr = raddr + i
            _ = self._dev.pci.reg_base_addr
            self._dev.pci.reg_data = wd
            _ = self._dev.pci.reg_data

        self.pc = addr

    def set_breakpoint(self, addr):
        original_insn = struct.unpack("!I", self.tr_read(addr, 1))[0]
        self.tr_write_dword(addr, 0xd)
        try:
            self._breakpoints[addr] = original_insn
        except:
            self._breakpoints = {addr: original_insn}

    def resume_from_breakpoint(self):
        if not self.status.invalid_instruction:
            raise Exception("not halted at breakpoint")
        try:
            original_instruction = self._breakpoints[self.pc]
        except:
            raise Exception("not halted at known breakpoint")
        self.ir = original_instruction
	self.status.invalid_instruction = 1

    def clear_breakpoint(self, addr):
        original_insn = self._breakpoints[addr]
        self.tr_write_dword(addr, original_insn)
        del self._breakpoints[addr]

    if not _no_capstone:
        md_mode = CS_MODE_MIPS32 + CS_MODE_BIG_ENDIAN
        md = Cs(CS_ARCH_MIPS, md_mode)
        md.detail = True
        md.skipdata = True

        def get_ir_dis(self):
            if not self.status.halted:
                raise Exception("cpu not halted")

            i = struct.pack(">I", self.ir)
            r = self.md.disasm(i, 4).next()
            if r.operands > 0:
                 for j in r.operands:
                     eff = 0
                     if j.type == MIPS_OP_REG:
                         eff = getattr(self, "r%d" % (j.reg - 1))
                     if j.type == MIPS_OP_IMM:
                         eff = j.imm
                     if j.type == MIPS_OP_MEM:
                         eff = getattr(self, "r%d" % (j.reg - 1))
                         eff += int(j.mem.disp)
                     j.eff = eff
            return r

        ird = property(get_ir_dis, None)

        def dis_at(self, addr, count=1, verbose=0):
            pc = self.pc
            
            raw = self.tr_read(addr, count)

            dis = self.md.disasm(raw, addr)
            dis = self._disp_dis(dis, verbose=verbose)

        def dis_pc(self, context=0, verbose=1):
            if not self.status.halted:
                raise Exception("cpu not halted")
            pc = self.pc
            bp = self.breakpoint.address
            if context != 0:
                self.dis_at(pc - (context * 4), count = (context * 2) + 1)
            else:
                self.dis_at(self.pc, verbose=verbose)

        def _disp_dis(self, decoded, verbose=0, pc=None, bp=None):
            for i in decoded:
                tmp = '    '
                if i.address == pc:
                    tmp = '--> '
                if i.address == bp:
                    tmp = '*' + tmp[1:]
                print "%s0x%08x:  %08x  %s  %s" % (tmp, i.address, struct.unpack(">I", i.bytes)[0], i.mnemonic, i.op_str)
                if verbose and len(i.operands) > 0:
                     c = -1
                     for j in i.operands:
                         c += 1
                         if j.type == MIPS_OP_REG:
                             val = getattr(self, "r%d" % (j.reg - 1))
                             print(" " * 19 + "operand %u: REG %s = %08x" % (c, i.reg_name(j.reg), val))
                         if j.type == MIPS_OP_IMM:
                             print(" " * 19 + "operand %u: IMM = %s" % (c, to_x(j.imm)))
                         if j.type == MIPS_OP_MEM:
                             addr = 0
                             val = 0
                             disp = 0
                             eff = 0
                             if j.mem.base != 0:
                                 val = getattr(self, "r%d" % (j.reg - 1))
                                 addr = val
                             if j.mem.disp != 0:
                                 disp = int(j.mem.disp)
                                 addr += disp
                             if addr != 0:
                                 eff = struct.unpack(">I", self.tr_read(addr, 1))[0]
                             print(" " * 19 + "operand %u: MEM @%08x = %08x" % (c, addr, eff))
                             if j.mem.base != 0:
                                 val = getattr(self, "r%d" % (j.reg - 1))
                                 print(" " * 21 + "operand %u base: REG %s = %08x"
                                     % (c, i.reg_name(j.mem.base), val))
                                 addr = val
                             if j.mem.disp != 0:
                                 print(" " * 21 + "operand %u disp: IMM %x"
                                     % (c, int(j.mem.disp)))
                                 addr += j.mem.disp

    def set_hw_breakpoint(self, addr, enable = True, reset = False):
        if not self.breakpoint.disabled and not reset:
            raise Exception("breakpoint already set")
        self.breakpoint.address = addr & 0xfffffffc
        if not enable: 
            self.breakpoint.disabled = 1

    def clear_hw_breakpoint(self):
        self.breakpoint.disabled = 1

    def reset(self):
        self.status.word = 0xffffffff
        self.mode.reset = 1

        print "[+] resetting rxcpu...",
        cnt = 0
        while self.mode.reset:
            cnt += 1
            if cnt > 1000:
                raise Exception("timed out waiting for rxcpu to reset")

            usleep(10)

        print "completed after %d us" % (cnt * 10)

    def halt(self):
        if not self.mode.halt:
            print "[+] halting rx cpu",
            self.mode.halt = 1
            cnt = 0
            while not self.status.halted:
                cnt += 1
                if cnt > 1000:
                    raise Exception("timed out halting rx cpu")
                usleep(10)

            print "halted after %d us" % (cnt * 10)

    def resume(self):
        if self.mode.halt:
            print "[+] resuming rx cpu from %08x" % self.pc,
            self.mode.halt = 0

            cnt = 0
            while self.status.halted:
                cnt += 1
                if cnt > 1000:
                    raise Exception("timed out resuming rx cpu")
                usleep(10)

            print "resumed after %d us" % (cnt * 10)

    def clear_events(self):
        if self.status.word & ~0x400:
            print "[+] clearing rx cpu events (was %08x, now" % self.status.word,
            self.status.word = 0xffffffff
            self.status.word = 0
            print "%08x)" % self.status.word

            
    def go(self, addr = None):
        self.halt()
        if addr == None:
            addr = self.pc

        self.pc = addr
        self.clear_events()
        self.resume()

    def tg3db(self, en=1):
        from magic import DebugMagic
        print "[+] loading %s debug magics" % self.block_name
        ip = get_ipython()
        magics = DebugMagic(ip, self)
        ip.register_magics(magics)

