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

class TgInstaller(object):
    def __init__(self, dev):
        self.dev = dev

    def __enter__(self):
        self.dev.init()
        self.dev.nvram.init(wr=1)
        return self

    def __exit__(self, t, v, traceback):
        pass

    def run(self, loc = None):
        return self.dev.nvram.install_thundergate()
