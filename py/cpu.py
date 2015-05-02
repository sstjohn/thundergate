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
from capstone import *
from capstone.mips import *

from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

def to_x(v):
    if not v: return '0'
    r = struct.pack(">q", v)
    while r[0] in (chr(0), 0):
        r = r[1:]

    return " ".join(["%02x" % ord(c) for c in r])
    

class Cpu(rflip.cpu):
    try:
        mode = CS_MODE_MIPS32 + CS_MODE_BIG_ENDIAN
    except:
        mode = CS_MODE_32 + CS_MODE_BIG_ENDIAN
    md = Cs(CS_ARCH_MIPS, mode)
    md.detail = True

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


    def dis_addrs(self, addr, count=1):
        raw = self._dev.mem.read(addr, count * 4)        
        return self.md.disasm(raw, addr)

    def dis_ir(self):
        if not self.status.halted:
            raise Exception("cpu not halted")

        raw = struct.pack(">I", self.instruction)
        return self.md.disasm(raw, self.pc)

    def disp_dis(self, decoded, verbose=0, pc=None):
        for i in decoded:
            tmp = '\t'
            if i.address == pc:
                tmp = '-->\t'
            print "%s0x%08x:\t%s\t%s" % (tmp, i.address, i.mnemonic, i.op_str)
            if verbose and len(i.operands) > 0:
                 print("\t\top_count: %u" % len(i.operands))
                 c = -1
                 for j in i.operands:
                     c += 1
                     if j.type == MIPS_OP_REG:
                         print("\t\t\toperands[%u].type: REG = %s" % (c, i.reg_name(j.reg)))
                     if j.type == MIPS_OP_IMM:
                         print("\t\t\toperands[%u].type: IMM = %s" % (c, to_x(j.imm)))
                     if j.type == MIPS_OP_MEM:
                         print("\t\t\toperands[%u].type: MEM" % c)
                         if j.mem.base != 0:
                             print("\t\t\t\toperands[%u].mem.base: REG = %s" \
                                 % (c, i.reg_name(j.mem.base)))
                         if j.mem.disp != 0:
                             print("\t\t\t\toperands[%u].mem.disp: %s" \
                                 % (c, to_x(j.mem.disp)))

