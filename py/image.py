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
from elftools.dwarf.descriptions import set_global_machine_arch
from elftools.dwarf.dwarf_expr import GenericExprVisitor
from elftools.dwarf.locationlists import LocationEntry
from StringIO import StringIO
import bisect
import platform
import struct

class ExprLiveEval(GenericExprVisitor):
    def __init__(self, image):
        self._image = image 
        super(ExprLiveEval, self).__init__(image.dwarf.structs)
    
    def process_expr(self, dev, expr):
        self._val = 0
        self._dev = dev
        print "processing expr %s" % str(expr)
        assert isinstance(expr, list) and len(expr) > 0
        if isinstance(expr[0], LocationEntry):
            cur_pc = self._dev.rxcpu.pc
            fname, cu_name, cu_line_no, cu_comp_dir = self._image.top_frame_at(cur_pc)
            cu = self._image._compile_units[cu_name]
            cu_base = cu["lpc"]
            offset = cur_pc - cu_base
            found = False
            for entry in expr:
                if offset >= entry.begin_offset and offset < entry.end_offset:
                    super(ExprLiveEval, self).process_expr(entry.loc_expr)
                    found = True
                    break
            if not found:
                self._val = '(unhandled ll, offset %d, list: %s)' % (offset, str(expr))
        else:
            super(ExprLiveEval, self).process_expr(expr)
        try:
            print "expr %s evaluates to %x" % (expr, self.value)
        except:
            print "expr %s produces error message %s" % (expr, self.value)
        return self.value

    @property
    def value(self):
        return self._val

    def _after_visit(self, opcode, opcode_name, args):
        if isinstance(self._val, str):
            return
        print
        print "processing opcode: %s (0x%x), args: %s" % (opcode_name, opcode, args)
        if 0x3 == opcode:
            v = self._dev.rxcpu.tr_read(args[0], 1)
            self._val = struct.unpack("!I", v)[0]
        elif 0x30 <= opcode and opcode < 0x50:
            self._val = opcode - 0x30
        elif 0x50 <= opcode and opcode < 0x70:
            self._val = getattr(self._dev.rxcpu, "r%d" % (opcode - 0x50))
        elif 0x70 <= opcode and opcode < 0x90:
            b = getattr(self._dev.rxcpu, "r%d" % (opcode - 0x70))
            b = getattr(self._dev.rxcpu, "r%d" % (opcode - 0x70))
            if len(args) > 0:
                assert len(args) == 1
                b += args[0]
            v = self._dev.rxcpu.tr_read(b, 1)
            v = self._dev.rxcpu.tr_read(b, 1)
            self._val = struct.unpack("!I", v)[0]
        elif 0x91 == opcode:
            cur_pc = self._dev.rxcpu.pc
            fname, cu_name, cu_line_no, cu_comp_dir = self._image.top_frame_at(cur_pc)
            frame_base = self._image._compile_units[cu_name]["functions"][fname]["fb"]
            print "frame base is %s" % str(frame_base)
            assert isinstance(frame_base, list) and len(frame_base) > 0
            expr = None
            if isinstance(frame_base[0], LocationEntry):
                cu_base = self._image._compile_units[cu_name]['lpc']
                offset = cur_pc - cu_base 
                for le in frame_base:
                    if offset >= le.begin_offset and offset < le.end_offset:
                        expr = le.loc_expr
                        break
                if expr is None:
                    self._val = "(op %s unhandled, pc: %d, args: %s, fb: %s)" % (opcode_name, cur_pc, args, str(frame_base))
                    return
            else:
                expr = frame_base
            print "frame base expression is %s" % str(expr)
            evaluator = ExprLiveEval(self._image)
            fb_value = evaluator.process_expr(self._dev, expr)
            if isinstance(fb_value, str):
                self._val = fb_value + " (encountered by frame base evaluator)"
            else:
                print "frame base expression evaluates to %x" % fb_value
                addr = fb_value
                if len(args) > 0:
                    assert len(args) == 1
                    addr += args[0]
                print "frame base plus offset is %x" % addr
                v = self._dev.rxcpu.tr_read(addr, 1)
                self._val = struct.unpack("!I", v)[0]
        else:
            self._val = "(unable to handle opcode %x (%s))" % (opcode, opcode_name)
        try: 
            print "val is now %x" % self._val
        except: 
            print "val is now \"%s\"" % self._val

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
            set_global_machine_arch(self.elf.get_machine_arch())
            self.__tame_dwarf()
            self.expr_evaluator = ExprLiveEval(self)

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
        print "%s" % str(s.header)
        img = s.data()

        s = self.elf.get_section(2)
        if s.header["sh_flags"] & 2:
            if s.header["sh_addr"] != base_addr + len(img):
                raise Exception("bad section vaddr - #2 should follow #1")
            img += s.data()

        s = self.elf.get_section(3)
        if s.header["sh_flags"] & 2:
            if s.header["sh_addr"] != base_addr + len(img):
                raise Exception("bad section vaddr - #3 should follow #2")
            img += s.data()

        return (base_addr, img)

    def __tame_dwarf(self):
        dw = self.dwarf
        self._compile_units = {}
        self._addresses = {}
        self._lowest_known_address = None
        
        location_lists = dw.location_lists()

        for c in dw.iter_CUs():
            functions = {}  
            variables = {}

            td = c.get_top_DIE()

            for d in td.iter_children():
                if d.tag == 'DW_TAG_subprogram':
                    lpc = d.attributes['DW_AT_low_pc'].value
                    hpc = d.attributes['DW_AT_high_pc'].value
                    if hpc < lpc:
                        hpc += lpc

                    function_name = d.attributes['DW_AT_name'].value
                    f = {}
                    f["lpc"] = lpc
                    f["hpc"] = hpc
                    f["args"] = {}
                    f["vars"] = {}
                    if 'DW_AT_frame_base' in d.attributes:
                        a = d.attributes['DW_AT_frame_base']
                        print "frame base attribute: %s" % str(a)
                        if a.form == 'DW_FORM_data4':
                            f["fb"] = location_lists.get_location_list_at_offset(a.value)
                        else:
                            f["fb"] = a.value
                    
                    for child in d.iter_children():
                        if child.tag == "DW_TAG_formal_parameter":
                            name = child.attributes['DW_AT_name'].value
                            v = {}
                            try:
                                print "DW_TAG_formal_parameter child.attributes['DW_AT_location'].value = %s\n" % str(child.attributes['DW_AT_location'])
                                if child.attributes['DW_AT_location'].form == 'DW_FORM_data4':
                                    v["location"] = location_lists.get_location_list_at_offset(child.attributes['DW_AT_location'].value)
                                else:
                                    v["location"] = child.attributes['DW_AT_location'].value
                            except:
                                v["location"] = []
                            f["args"][name] = v
                        if child.tag == "DW_TAG_variable":
                            name = child.attributes['DW_AT_name'].value
                            v = {}
                            try:
                                print "DW_TAG_variable child.attributes['DW_AT_location'].value = %s\n" % str(child.attributes['DW_AT_location'])

                                if child.attributes['DW_AT_location'].form == 'DW_FORM_data4':
                                    v["location"] = location_lists.get_location_list_at_offset(child.attributes['DW_AT_location'].value)
                                else:
                                    v["location"] = child.attributes['DW_AT_location'].value
                            except:
                                v["location"] = []
                            f["vars"][name] = v

                    functions[function_name] = f
                elif d.tag == 'DW_TAG_variable':
                    if d.attributes['DW_AT_decl_file'].value == 1:
                        try:
                            name = d.attributes['DW_AT_name'].value
                        except:
                            name = '(%s)' % str(d.attributes['DW_AT_name'])
                            
                        v = {}
                        try:
                            print "DW_TAG_variable d.attributes['DW_AT_location'].value = %s\n" % str(d.attributes['DW_AT_location'])
                            v["location"] = d.attributes['DW_AT_location'].value
                        except:
                            v["location"] = []
                        variables[name] = v

            x = {}

            fname = td.attributes['DW_AT_name'].value
            x["line_program"] = dw.line_program_for_CU(c).get_entries()
            x["lpc"] = td.attributes['DW_AT_low_pc'].value
            x["hpc"] = td.attributes['DW_AT_high_pc'].value
            x["comp_dir"] = td.attributes['DW_AT_comp_dir'].value
            x["functions"] = functions
            x["variables"] = variables

            self._compile_units[fname] = x
            if ((self._lowest_known_address is None) or
                    (self._lowest_known_address > x["lpc"])):
                self._lowest_known_address = x["lpc"]

        for c in self._compile_units:
            self._compile_units[c]["lines"] = {}
            for line in self._compile_units[c]["line_program"]:
                state = line.state
                if state is not None and not state.end_sequence:
                    if state.address in self._addresses:
                        raise Exception("addr %x is both \"%s\" and \"%s+%d\"" % (state.address, self._addresses[state.address], c, state.line))
                    self._addresses[state.address] = "%s+%d" % (c, state.line)
		    self._compile_units[c]["lines"][state.line] = state.address

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

    def line2addr(self, fname, line):
        return self._compile_units[fname]["lines"][line]	
