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

    def read_reg(self, reg):
        self.emac.mii_communication.phy_addr = self.addr
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
       
    def write_reg(self, reg, val):
        assert val & ~0xffff == 0
        self.emac.mii_communication.phy_addr = self.addr
        self.emac.mii_communication.reg_addr = reg
        self.emac.mii_communication.data = val
        self.emac.mii_communication.write_command = 0
        self.emac.mii_communication.read_command = 1
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
        self.write_reg(0, (1 << 14))
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
        self.write_reg(0, 0)
        anar = (1 << 11) | (1 << 10) | 1
        anar |= (1 << 8) | (1 << 7) | (1 << 6) | (1 << 5)
        self.write_reg(0x4, anar)
        self.write_reg(0x9, (1 << 9))
        self.write_reg(0, (1 << 12) | (1 << 9))
        cnt = 0
        res = self.read_reg(0x19)
        while res & 0x8000 == 0:
            if cnt > 2000:
                break
            usleep(1000)
            res = self.read_reg(0x19)
            cnt += 1
        
        return res
