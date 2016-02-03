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

from time import sleep

usleep = lambda x: sleep(x / 1000000.0)

class TopLevel(object):
    def __init__(self, bus):
        self._smi_bus = bus

    def _set_access(self, val):
        self._smi_bus.write_shd1c(5, 0xb, val)

    def _get_access(self):
        return self._smi_bus.read_shd1c(5, 0xb)

    access = property(_get_access, _set_access)

    def _set_data(self, val):
        self._smi_bus.write_shd1c(6, 0xc, val)

    def _get_data(self):
        return self._smi_bus.read_exp(3, 0xb)

    data = property(_get_data, _set_data)
