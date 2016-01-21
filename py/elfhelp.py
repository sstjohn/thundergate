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

def elf_to_image(fname):
    with open(fname, "r") as f:
        elf_data = StringIO(f.read())
    
    e = ELFFile(elf_data)

    s = e.get_section(1)
    base_addr = s.header["sh_addr"]
    img = s.data()

    s = e.get_section(2)
    if s.header["sh_addr"] != base_addr + len(img):
        raise Exception("bad section vaddr - #2 should follow #1")
    img += s.data()

    s = e.get_section(3)
    if s.header["sh_addr"] != base_addr + len(img):
        raise Exception("bad section vaddr - #3 should follow #2")
    img += s.data()

    return (base_addr, img)
