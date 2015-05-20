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

import struct
import rflip
from socket import htonl
from ctypes import c_char, c_uint, cast, pointer, POINTER
from IPython.core.magic import (Magics, magics_class, line_magic,
                        cell_magic, line_cell_magic)
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
    

class Cpu(rflip.cpu):
    if not _no_capstone:
        md_mode = CS_MODE_MIPS32 + CS_MODE_BIG_ENDIAN
        md = Cs(CS_ARCH_MIPS, md_mode)
        md.detail = True
        md.skipdata = True

        def dis_at(self, addr, count=1, verbose=0, pc=None):
            if pc is None:
                pc = self.pc

            if addr >= 0x08000000 and addr < 0x08010000:
                raddr = (addr & 0xffff) | 0x30000
            elif addr >= 0x40000000 and addr < 0x40005000:
                raddr = (addr & 0xffff) | 0x20000
            
            try:
                tmp = []
                for i in range(0, count * 4, 4):
                    self._dev.pci.reg_base_addr = raddr + i
                    _ = self._dev.pci.reg_base_addr
                    tmp += [htonl(self._dev.pci.reg_data)]

                tmp = (c_uint * count)(*tmp)
                raw = cast(pointer(tmp), POINTER(c_char * (count * 4))).contents.raw
            except:
                raw = self._dev.mem.read(addr, count * 4)

            dis = self.md.disasm(raw, addr)
            dis = self._disp_dis(dis, verbose=verbose, pc=pc)


        def dis_pc(self, context=0, verbose=1):
            if not self.status.halted:
                raise Exception("cpu not halted")
            if context != 0:
                pc = self.pc
                self.dis_at(pc - context, count = context * 2, pc = pc)
            else:
                self.dis_at(self.pc, verbose=verbose, pc=self.pc)

        def _disp_dis(self, decoded, verbose=0, pc=None):
            for i in decoded:
                tmp = '\t'
                if i.address == pc:
                    tmp = '-->\t'
                print "%s0x%08x:\t%s\t%s" % (tmp, i.address, i.mnemonic, i.op_str)
                if verbose and len(i.operands) > 0:
                     c = -1
                     for j in i.operands:
                         c += 1
                         if j.type == MIPS_OP_REG:
                             val = getattr(self, "r%d" % (j.reg - 1))
                             print("\t\toperand %u: REG %s (= %08x)" % (c, i.reg_name(j.reg), val))
                         if j.type == MIPS_OP_IMM:
                             print("\t\toperand %u: IMM = %s" % (c, to_x(j.imm)))
                         if j.type == MIPS_OP_MEM:
                             print("\t\toperand %u: MEM" % c)
                             if j.mem.base != 0:
                                 print("\t\t\toperand %u mem.base: REG %s"
                                     % (c, i.reg_name(j.mem.base)))
                             if j.mem.disp != 0:
                                 print("\t\t\toperands[%u].mem.disp: %s"
                                     % (c, to_x(j.mem.disp)))

    def set_breakpoint(self, addr, enable = True, reset = False):
        if not self.breakpoint.disabled and not reset:
            raise Exception("breakpoint already set")
        self.breakpoint.address = addr & 0xfffffffc
        if not enable: 
            self.breakpoint.disabled = 1

    def clear_breakpoint(self):
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
        @magics_class
        class DebugMagic(Magics):

                def __init__(self, shell, cpu):
                        super(DebugMagic, self).__init__(shell)
                        self.cpu = cpu

                @line_magic
                def u(self, addr = None):
                        if None is addr or addr == '':
                                self.cpu.dis_pc()
                        else:
                                self.cpu.dis_at(addr)

                @line_magic
                def s(self, arg):
                    self.cpu.mode.single_step = 1
                    self.cpu.dis_pc()

                @line_magic
                def h(self, arg):
                    self.cpu.halt()

                @line_magic
                def g(self, addr):
                    if '' == addr: addr = None
                    self.cpu.go(addr)

                @line_magic
                def bp(self, arg):
                    if None is arg or '' == arg:
                        print "hardware breakpoint at %08x" % self.cpu.breakpoint.address,
                        print "%s" % ("disabled" if self.cpu.breakpoint.disabled else "enabled")
                    elif arg == '-':
                        self.cpu.clear_breakpoint()
                    else:
                        self.cpu.set_breakpoint(int(arg, 0))

                @line_magic
                def reset(self, arg): self.cpu.reset()

                @line_magic
                def reg(self, arg):
                    try:
                        return getattr(self.cpu, "r%d" % int(arg))
                    except:
                        return getattr(self.cpu, "r%d" % mips_regs[arg])
                
                @line_magic
                def pc(self, arg): return self.cpu.pc

                @line_magic
                def ir(self, arg): return self.cpu.instruction

        print "[+] loading %s debug magics" % self.block_name
        ip = get_ipython()
        magics = DebugMagic(ip, self)
        ip.register_magics(magics)

