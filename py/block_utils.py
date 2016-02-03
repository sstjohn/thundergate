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

import ctypes
import tglib as tg

from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

def disp(b, ilvl=0):
    for f in b._fields_:
        name = f[0]
        if name[0] == "_":
            name = "<%s>" % f[1].__name__
        if ctypes.Structure in f[1].__bases__:
            print "%sstruct %s:" % (" " * ilvl, name)
            disp(getattr(b, f[0]), ilvl+1)
        elif ctypes.Union in f[1].__bases__:
            print "%sunion %s:" % (" " * ilvl, name)
            disp(getattr(b, f[0]), ilvl+1)
        elif ctypes.Array in f[1].__bases__:
            a = getattr(b, f[0])
            print "%s%s[%d]:" % (" " * ilvl, name, len(a)),
            tmp = None
            if type(a) == str:
                tmp = '"%s"' % a
            else:
                for v in a:
                    try:
                        if None == tmp:
                            tmp = "[%x" % v
                        else:
                            tmp = "%s, %x" % (tmp, v)
                    except:
                        tmp = "<error>"
                    print "%s]" % tmp
        else:
            print "%s%s: %x" % (" " * ilvl, name, getattr(b, f[0]))
        
def dump(self):
    for i in range(0, ctypes.sizeof(self.mem), 4):
            if 0 == i % 0x10:
                    print
                    print "0x%04x: " % (self.offset + i),
            print "%08x" % self.mem[i / 4],
    print

def _enable(self,reset=0,quiet=0):
    bn = self.block_name
    if bn.endswith("_x"):
        bn = bn[:-2]
    if bn.endswith("_regs"):
        bn = bn[:-5]
    if reset:
        if not quiet:
            print "[+] resetting and enabling %s" % bn
            quiet = 1
        _disable(self, quiet=1)
        _reset(self, quiet=1)

    if self.mode.enable == 0:
        if not quiet:
            print "[+] enabling %s" % bn
        self.mode.enable = 1
        return 0
    return 1

def _disable(self, quiet=0):
    bn = self.block_name
    if bn.endswith("_x"):
        bn = bn[:-2]
    if bn.endswith("_regs"):
        bn = bn[:-5]
    if self.mode.enable:
        if not quiet:
            print "[+] disabling %s" % bn,
        self.mode.enable = 0
        slept = 0
        while self.mode.enable:
            if slept >= 50000:
                raise Exception("%s failed to stop" % bn)
            usleep(100)
            slept += 1
            self.mode.enable = 0
        if slept and not quiet:
            print "took %d ms" % slept
        else:
            print
        return 1
    return 0

def _reset(self, quiet=0):
    bn = self.block_name
    if bn.endswith("_x"):
        bn = bn[:-2]
    if bn.endswith("_regs"):
        bn = bn[:-5]
    if not quiet:
        print "[+] resetting %s" % bn
    tmp = _disable(self, quiet=1)
    self.mode.reset = 1
    cntr = 0
    while self.mode.reset and cntr < 1000:
        cntr += 1
        usleep(10)
        if self.mode.reset:
            raise Exception("timed out waiting for %s reset to complete" % bn)
    if tmp:
        _enable(self, quiet=1)

reset = _reset
enable = _enable
disable = _disable