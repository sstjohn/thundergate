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

from time import sleep

usleep = lambda x: sleep(x / 1000000.0)

class Smi(object):
    def __init__(self, dev):
        self.emac = dev.emac

    def read_reg(self, port, addr):
        self.emac.mii_communication.phy_addr = port
        self.emac.mii_communication.reg_addr = addr
        self.emac.mii_communication.write_command = 0
        self.emac.mii_communication.read_command = 1
        self.emac.mii_communication.start_busy = 1
        cnt = 0
        while self.emac.mii_communication.start_busy:
            if cnt > 20:
                raise Exception("mii communication timed out")
            usleep(100)
            cnt += 1

        if self.emac.mii_communication.read_failed:
            raise Exception("mii read failed")

        return self.emac.mii_communication.data
       
    def write_reg(self, port, addr, val):
        assert val & ~0xffff == 0
        self.emac.mii_communication.phy_addr = port
        self.emac.mii_communication.reg_addr = addr
        self.emac.mii_communication.data = val
        self.emac.mii_communication.write_command = 1
        self.emac.mii_communication.read_command = 0
        self.emac.mii_communication.start_busy = 1
        cnt = 0
        while self.emac.mii_communication.start_busy:
            if cnt > 100:
                raise Exception("mii communication timed out")
            usleep(100)
            cnt += 1

    def read_exp18(self, port, shadow):
        assert 0 <= shadow and shadow <= 7
        self.write_reg(port, 0x18, shadow << 12 | 7)
        return self.read_reg(port, 0x18)

    def write_exp18(self, port, shadow, val):
        if val & shadow != shadow:
            raise Exception("shadow selector does not match parameter")
        self.write_reg(port, 0x18, val)

    def read_exp1c(self, port, shadow):
        assert 0 <= shadow and shadow <= 31
        self.write_reg(port, 0x1c, shadow << 10)
        return self.read_reg(port, 0x1c)

    def write_exp1c(self, port, shadow, val):
        assert 0 <= shadow and shadow <= 31
        assert 0 <= val
        val &= 0x7fff
        if val <= 0x3ff:
            val |= shadow << 10
        elif (val >> 10) != shadow:
            raise Exception("shadow selector does not match parameter")
        self.write_reg(port, 0x1c, 0x8000 | val)

    def read_exp1d(self, port, shadow):
        assert 0 <= shadow and shadow <= 1
        self.write_reg(port, 0x1d, shadow << 15)
        return self.read_reg(port, 0x1d)

    def write_exp1d(self, port, shadow, val):
        assert 0 <= shadow and shadow <= 1
        val = (val & 0x7fff) | (0x8000 if shadow > 1 else 0)
        self.write_reg(port, 0x1d, val)

    def _setup_cl45(self, port, devad, reg):
        assert 0 <= devad and devad <= 31
        assert 0 <= reg and reg <= 0xffff
        self.write_reg(port, 0x0d, devad)
        self.write_reg(port, 0x0e, reg)
        self.write_reg(port, 0x0d, 0x4000 | devad)

    def read_cl45(self, port, devad, reg):
        self._setup_cl45(port, devad, reg)
        return self.read_reg(port, 0x0e)

    def write_cl45(self, port, devad, reg, val):
        assert 0 <= val and val <= 0xffff
        self._setup_cl45(port, devad, reg)
        self.write_reg(port, 0x0e, val)

    def dump_regs(self, port, exp18=False, exp1c=False, exp1d=False):
        for i in range(0, 32):
            if exp18 and i == 0x18:
                for j in range(0, 8):
                    print "%02x.%x : %04x" % (0x18, j, self.read_exp18(port, j))
            elif exp1c and i == 0x1c:
                for j in range(0, 32):
                    print "%02x.%02x : %04x" % (0x1c, j, self.read_exp1c(port, j))
            elif exp1d and i == 0x1d:
                for j in range(0, 2):
                    print "1d.%x : %04x" % (j, self.read_exp1d(port, j))
            else:
                val = self.read_reg(port, i)
                print "%02x   : %04x" % (i, val)
