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

class Phy(object):
    def __init__(self, dev, phyaddr):
        self.emac = dev.emac
        self.addr = phyaddr

    def read_reg(self, reg, addr = None):
        if None == addr:
            addr = self.addr
        self.emac.mii_communication.phy_addr = addr
        self.emac.mii_communication.reg_addr = reg
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
       
    def write_reg(self, reg, val, addr = None):
        assert val & ~0xffff == 0
        if None == addr:
            addr = self.addr
        self.emac.mii_communication.phy_addr = addr
        self.emac.mii_communication.reg_addr = reg
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

    def reset(self):
        self.write_reg(0, 0x8000)
        cnt = 0
        while self.read_reg(0) & 0x8000:
            if cnt > 100:
                raise Exception("phy reset timed out")
            usleep(100)
            cnt += 1

    def loopback(self):
        self.write_reg(0, 1 << 14)
        cnt = 0
        while self.read_reg(1) & (1 << 4):
            if cnt > 15000:
                raise Exception("link failed to drop")
            usleep(10)
            cnt += 1

    def auto_mdix(self):
        self.write_reg(0x18, 0x7007)
        v = self.read_reg(0x18)
        v |= (1 << 9)
        self.write_reg(0x18, v | (1 << 15))
        v = self.read_reg(0x10)
        v &= ~(1 << 14)
        self.write_reg(0x10, v)

    def autonegotiate(self):
        self.reset()
        self.auto_mdix()
        self.loopback()

        anar = (1 << 11) | (1 << 10) | (1 << 8) | (1 << 7);
        anar |= (1 << 6) | (1 << 5) | 1;
        self.write_reg(0x4, anar)

        self.write_reg(0x9, (1 << 9))
        
        self.write_reg(0, (1 << 12) | (1 << 9))
        
        cnt = 0
        res = self.read_reg(1)
        while res & (1 << 5) == 0:
            if cnt > 5000:
                break
            usleep(100)
            res = self.read_reg(1)
            cnt += 1
        
        return self.read_reg(0x19)

    def may_send_pause(self):
        val = self.read_reg(5) & (1 << 10) != 0
        assert val == ((self.read_reg(0x19) & 1) != 0)
        return val

    def may_recv_pause(self):
        val = self.read_reg(5) & (3 << 10) != 0
        assert val == ((self.read_reg(19) & 2) != 0)
        return val

    def dump_regs(self, addr=None):
        if None == addr:
            addr = self.addr

        for i in range(0, 32):
            if addr == 1 and i == 0x18:
                for j in range(0, 8):
                    self.write_reg(0x18, j << 12 | 7, addr=addr)
                    val = self.read_reg(0x18, addr=addr)
                    print "%02x.%x : %04x" % (0x18, j, val)
            elif addr == 1 and i == 0x1c:
                for j in range(0, 32):
                    self.write_reg(0x1c, j << 10, addr=addr)
                    val = self.read_reg(0x1c, addr=addr)
                    print "%02x.%02x : %04x" % (0x1c, j, val)
            elif addr == 1 and i == 0x1d:
                self.write_reg(0x1d, 0, addr=addr)
                val = self.read_reg(0x1d, addr=addr)
                print "1d.00 : %04x" % val
                self.write_reg(0x1d, 0x8000, addr=addr)
                val = self.read_reg(0x1d, addr=addr)
                print "1d.01 : %04x" % val
            else:
                val = self.read_reg(i, addr=addr)
                print "%02x   : %04x" % (i, val)
