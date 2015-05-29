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

class GPhy(object):
    def __init__(self, bus, port):
        self._smi_bus = bus
        self._smi_port = port

    def read_reg(self, addr):
        return self._smi_bus.read_reg(self._smi_port, addr)

    def write_reg(self, addr, val):
        self._smi_bus.write_reg(self._smi_port, addr, val)

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

    def get_eee_cap(self):
        val = self._smi_bus.read_cl45(self._smi_port, 3, 0x14)
        return {'gig': 4 == (val & 4), 'fast': 2 == (val & 2)}

    def get_eee_adv(self):
        val = self._smi_bus.read_cl45(self._smi_port, 7, 0x3c)
        return {'gig': 4 == (val & 4), 'fast': 2 == (val & 2)}
    
    def set_eee_adv(self, gig, fast):
        val = (4 if gig else 0) | (2 if fast else 0)
        self._smi_bus.write_cl45(self._smi_port, 7, 0x3c, val)

    def get_eee_res(self):
        val = self._smi_bus.read_cl45(self._smi_port, 7, 0x803e)
        return {'gig': 4 == (val & 4), 'fast': 2 == (val & 2)}

    def get_eee_ctrl(self):
        val = self._smi_bus.read_cl45(self._smi_port, 7, 0x803d)
        return {'lpi': 0 != (val & 0x8000), 'sgmii_an': 0 != (val & 0x4000)}

    def dump_regs(self):
        self._smi_bus.dump_regs(self._smi_port, True, True, True)
