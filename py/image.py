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
import bisect
import platform

class Image(object):
    def __init__(self, fname):
        if platform.system() == "Windows":
            elf_data = open(fname, "r")
        else:     
            with open(fname, "r") as f:
                elf_data = StringIO(f.read())
        
        self.elf = ELFFile(elf_data)
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
        self._compile_units = {}
        self._addresses = {}
        self._lowest_known_address = None
        for c in dw.iter_CUs():
            functions = {}    

            for d in c.iter_DIEs():
                if d.tag == 'DW_TAG_subprogram':
                    lpc = d.attributes['DW_AT_low_pc'].value
                    hpc = d.attributes['DW_AT_high_pc'].value
                    if hpc < lpc:
                        hpc += lpc

                    function_name = d.attributes['DW_AT_name'].value
                    f = {}
                    f["lpc"] = lpc
                    f["hpc"] = hpc

                    functions[function_name] = f

            td = c.get_top_DIE()
            x = {}

            fname = td.attributes['DW_AT_name'].value
            x["line_program"] = dw.line_program_for_CU(c).get_entries()
            x["lpc"] = td.attributes['DW_AT_low_pc'].value
            x["hpc"] = td.attributes['DW_AT_high_pc'].value
            x["comp_dir"] = td.attributes['DW_AT_comp_dir'].value
            x["functions"] = functions

            self._compile_units[fname] = x
            if ((self._lowest_known_address is None) or
                    (self._lowest_known_address > x["lpc"])):
                self._lowest_known_address = x["lpc"]

        for c in self._compile_units:
            for line in self._compile_units[c]["line_program"]:
                state = line.state
                if state is not None:
                    self._addresses[state.address] = "%s+%d" % (c, state.line)

    def addr2line(self, addr):
        if addr in self._addresses:
            return self._addresses[addr]
        return ''

    def top_frame_at(self, addr):
        line = self.addr2line(addr)
        while '' == line and addr >= self._lowest_known_address:
            addr -= 4
            line = self.addr2line(addr)
        if '' == line:
            return ("unknown", "", 0, "")

        cuname, culine = line.split("+")
        fname = ""
        c = self._compile_units[cuname]
        for f in c["functions"]:
            if ((c["functions"][f]["lpc"] <= addr) and
                    (c["functions"][f]["hpc"] >= addr)):
                fname = f
                break
        return (fname, cuname, culine, c["comp_dir"])

