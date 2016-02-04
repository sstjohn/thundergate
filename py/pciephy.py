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

blocks = [('IEEE0', 0),
          ('IEEE1', 1),
          ('BLK0', 0x800),
          ('BLK1', 0x801),
          ('BLK2', 0x802),
          ('BLK3', 0x803),
          ('BLK4', 0x804),
          ('TXPLL', 0x808),
          ('TXCTRL0', 0x820),
          ('SERDESID', 0x831),
          ('RXCTRL0', 0x40)]

class PCIePhy(object):
    def __init__(self, bus):
        self._smi_bus = bus
        self._smi_port = 0

    def _set_block(self, block):
        assert 0 <= block and block <= 0xffff
        self._smi_bus.write_reg(self._smi_port, 0x1f, block << 4)

    def read_reg(self, block, ofs):
        assert 0 <= ofs and ofs < 0x1f
        self._set_block(block)
        return self._smi_bus.read_reg(self._smi_port, ofs)

    def write_reg(self, block, ofs, val):
        assert 0 <= ofs and ofs < 0x1f
        self._set_block(block)
        self._smi_bus.write_reg(self._smi_port, ofs, val)

    def dump_regs(self, block = 0):
        self._set_block(block)
        self._smi_bus.dump_regs(self._smi_port)

    def dump_blocks(self):
        for b in blocks:
            print b[0] + ":"
            self.dump_regs(b[1])
            print
