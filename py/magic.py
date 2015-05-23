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
from cpu import mips_regs
import reutils

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
    def rxdbg(self, arg):
        self.dev.rxcpu.tg3db()

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
            self.cpu.status.word = 0xffffffff
            self.cpu.mode.reset = 1
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