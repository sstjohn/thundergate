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

from IPython.core.magic import (Magics, magics_class, line_magic,
                        cell_magic, line_cell_magic)
from elftools.elf.elffile import ELFFile
from StringIO import StringIO

from cpu import mips_regs
import reutils
from struct import pack, unpack

@magics_class
class DeviceMagic(Magics):
    def __init__(self, shell, dev):
        super(DeviceMagic, self).__init__(shell)
        self.dev = dev

    @line_magic
    def d(self, arg):
        b = getattr(self.dev, arg)
        b.block_disp()

    @line_magic
    def rd(self, line):
        parts = line.split()
        if len(parts) == 0:
            pass 
        elif len(parts) == 1:
            ofs = int(parts[0], 0)
            print "%04x: %08x" % (ofs, self.dev.reg[ofs >> 2])
        else:
            start = int(parts[0], 0)
            end = int(parts[1], 0)
            i = 0
            for ofs in range(start, end, 4):
                if i % 0x20 == 0:
                    print "\n%04x: " % ofs,
                elif i % 0x10 == 0:
                    print "   ",
                elif i % 8 == 0:
                    print " ",
                print "%08x" % self.dev.reg[ofs >> 2],
                i += 4

    @line_magic
    def rxdbg(self, arg):
        self.dev.rxcpu.tg3db()

    @line_magic
    def ti(self, arg):
	self.dev.nvram.init(wr=1)
	self.dev.nvram.install_thundergate()
	self.dev.reset()

def _register_device_magic(dev):
    ip = get_ipython()
    ip.register_magics(DeviceMagic(ip, dev))

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
                    cnt = 1
                    try:
                        args = addr.split()
                        addr = int(args[0], 0)
                        if (len(args) > 1):
                            cnt = int(args[1], 0)
                    except:
                        pass
                    self.cpu.dis_at(addr, cnt)

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
            else:
                try: addr = int(addr, 0)
                except: pass
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
        def ir(self, arg): return self.cpu.ir

        @line_magic
        def rh(self, arg):
            self.cpu._dev.grc.fastboot_pc.enable = 0
            self.cpu._dev.grc.fastboot_pc.addr = 0
            self.cpu._dev.mem.write_dword(0xb50, 0)
            self.cpu._dev.grc.misc_config.grc_reset = 1
	    self.cpu._dev.init()
            self.cpu.mode.halt = 1
            self.u(None)

        @line_magic
        def su(self, arg, verbose=1):
            if self.cpu.status.halted != 1:
                raise Exception("halt cpu first")
            lpc = self.cpu.pc
            t = eval('lambda cpu: cpu.%s' % arg)
            
            while not t(self.cpu):
                lpc = self.cpu.pc
                self.cpu.mode.single_step = 1

            if verbose:
                print "\"%s\" became true after %08x:" % (str(arg), lpc)
                self.u(lpc)

                print "\npc now %08x: " % self.cpu.pc
                self.u(None)

        @cell_magic
        def tr(self, line, cell):
            if self.cpu.status.halted != 1:
                raise Exception("cpu not halted")

            while True:
                self.su(line, verbose=0)
                exec cell
                self.cpu.mode.single_step = 1
   
        @line_magic
        def elfload(self, line):
            with open(line, "r") as f:
                elf_data = StringIO(f.read())

            self._elf = ELFFile(elf_data)
            try:
                self._dwarf = self._elf.get_dwarf_info()
            except:
                print "%s does not contain DWARF info" % line

        @line_magic
        def elf(self, line):
            try: return self._elf
            except: print "no elf file loaded"

        @line_magic
        def dwarf(self, line):
            try: return self._dwarf
            except: print "no dwarf loaded"

        def _build_funcache(self):
            try: dw = self._dwarf
            except: 
                print "no dwarf loaded"
                return None
            fc = []
            for c in dw.iter_CUs():
                for d in c.iter_DIEs():
                    if d.tag == 'DW_TAG_subprogram':
                        lpc = d.attributes['DW_AT_low_pc'].value
                        hpc = d.attributes['DW_AT_high_pc'].value
                        if hpc < lpc:
                            hpc += lpc
                        n = d.attributes['DW_AT_name'].value
                        fc += [(lpc, hpc, n)]
            self._funcache = fc
            return fc

        @line_magic
        def funcs(self, line):
            try:
                fc = self._funcache
            except:
                fc = self._build_funcache()
                if fc == None:
                    return

            for f in fc:
                lpc, hpc, n = f
                print "%s: %x - %x" % (n, lpc, hpc)

        @line_magic
        def func_at(self, line):
            try:
                fc = self._funcache
            except:
                fc = self._build_funcache()
                if fc == None:
                    return

            pc = int(line, 0)

            for f in fc:
                lpc, hpc, n = f
                if lpc <= pc and pc < hpc:
                    return n

            return "(unknown)"

        @line_magic
        def sloc_at(self, line):
            try: dw = self._dwarf
            except:
                print "no dwarf loaded"
                return

            pc = int(line, 0)
            for c in dw.iter_CUs():
                    lp = dw.line_program_for_CU(c)
                    ps = None
                    for e in lp.get_entries():
                        if e.state is None or e.state.end_sequence:
                            continue
                        if ps and ps.address <= pc < e.state.address:
                            fn = lp['file_entry'][ps.file - 1].name
                            l = ps.line
                            return fn, l
                        ps = e.state
            return None, None

        @line_magic
        def tr2(self, line):
            if self.cpu.status.halted != 1:
                raise Exception("cpu not halted")

            while True:
                self.cpu.mode.single_step = 1
                i = self.cpu.ird
                pc = self.cpu.pc
                if i.mnemonic == 'lw':
                    eff = i.operands[1].eff
                    val = unpack(">I", self.cpu.tr_read(eff, 1))[0]
                    if eff & 0xffff8000 == 0xc0000000:
                        eff &= 0xffff
                        b, n, _, _ = reutils.whats_at(eff)
                        print "%08x: lw %08x from reg %04x (%s.%s)" % (pc, val, eff, b, n)
                    else:
                        print "%08x: lw %08x from %08x" % (pc, val, eff)
                elif i.mnemonic == 'sw':
                    eff = i.operands[1].eff
                    val = i.operands[0].eff
                    if eff & 0xffff8000 == 0xc0000000:
                        eff &= 0xffff
                        b, n, _, _ = reutils.whats_at(eff)
                        print "%08x: sw %08x to reg %04x (%s.%s)" % (pc, val, eff, b, n)
                    else:
                        print "%08x: sw %08x to %08x" % (pc, val, eff)
