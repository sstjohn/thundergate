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

from elftools.elf.elffile import ELFFile
from StringIO import StringIO

class Image(object):
    def __init__(self, fname):
        with open(fname, "r") as f:
            self.elf_data = StringIO(f.read())
    
        self.elf = ELFFile(self.elf_data)
        if self.elf.has_dwarf_info():
            self.dwarf = self.elf.get_dwarf_info()
            self.__tame_dwarf()

    @property
    def executable(self):
        try:
            return self._exe
        except:
            self._exe = self._build_executable()
        return self._exe

    def _build_executable(self):
        s = self.elf.get_section(1)
        base_addr = s.header["sh_addr"]
        img = s.data()

        s = self.elf.get_section(2)
        if s.header["sh_addr"] != base_addr + len(img):
            raise Exception("bad section vaddr - #2 should follow #1")
        img += s.data()

        s = self.elf.get_section(3)
        if s.header["sh_addr"] != base_addr + len(img):
            raise Exception("bad section vaddr - #3 should follow #2")
        img += s.data()

        return (base_addr, img)

    def __tame_dwarf(self):
        dw = self.dwarf
        self._compilation_units = []
        self._functions = []
        for c in dw.iter_CUs():
            self._compilation_units += [c]
            for d in c.iter_DIEs():
                if d.tag == 'DW_TAG_subprogram':
                    lpc = d.attributes['DW_AT_low_pc'].value
                    hpc = d.attributes['DW_AT_high_pc'].value
                    if hpc < lpc:
                        hpc += lpc

                    f = {}
                    f["name"] = d.attributes['DW_AT_name'].value
                    f["DIE"] = d
                    f["CU"] = c
                    self._functions += [(lpc, hpc, f)]

