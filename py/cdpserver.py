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

import os
import json
import sys
import platform
import traceback
import functools
import struct

from collections import namedtuple

p = platform.system()
if "Windows" == p:
    LINE_SEP = "\n"
else:
    LINE_SEP = "\r\n"
del p

from image import Image
from monitor import ExecutionMonitor
from datamodel import model_registers, model_memory, get_data_value, GenericModel
from blocks.cpu import mips_regs

try:
    from capstone import *
    from capstone.mips import *
    if cs_version()[0] < 3:
        print "[-] capstone outdated - disassembly unavailable"
        _no_capstone = True
    else:
        _no_capstone = False

        md_mode = CS_MODE_MIPS32 + CS_MODE_BIG_ENDIAN
        md = Cs(CS_ARCH_MIPS, md_mode)
        md.detail = True
        md.skipdata = True

        def _disassemble_word(word):
            i = struct.pack(">I", word)
            r = md.disasm(i, 4).next()
            return "%s %s" % (r.mnemonic, r.op_str)
except:
    print "[-] capstone not present - disassembly unavailable"
    _no_capstone = True

class ScopeModel(GenericModel):
    pass

class Var_Tracker(object):
    def __init__(self):
        self._references = []
        self._scopes = []
        self._fixed_reference_end = None
        self._fixed_scope_end = None
        self._known_frame_levels = []

    def _assign_variablesReference(self, v):
        self._references.append(v)
        v.variablesReference = len(self._references)

    def _add_variables_references(self, v):
        if hasattr(v, "children") and isinstance(v.children, list) and len(v.children) > 0:
            self._assign_variablesReference(v)
            for c in v.children:
                c.scope = v.scope
                self._add_variables_references(c)

    def add_fixed_scope(self, s, fl=-1):
        if self._fixed_scope_end:
            raise Exception("fixed scopes cannot be added while dynamic scopes are present")
        self._add_scope(s, fl)

    def _add_scope(self, s, fl=0):
        print "adding scope %s" % s.name
        s.fl = fl
        self._assign_variablesReference(s)
        self._scopes += [s]
        for c in s.children:
            c.scope = s
            self._add_variables_references(c)
        if not fl in self._known_frame_levels:
            self._known_frame_levels += [fl]

    def add_dynamic_scope(self, s, fl = 0):
        if not self._fixed_scope_end:
            self._fixed_scope_end = len(self._scopes)
            self._fixed_reference_end = len(self._references)
        self._add_scope(s, fl)

    def clear_dynamic_scopes(self):
        self._scopes = self._scopes[:self._fixed_scope_end]
        self._references = self._references[:self._fixed_reference_end]
        self._fixed_scope_end = None
        self._fixed_reference_end = None
        self._known_frame_levels = []

    def get_scopes(self, fl=0):
        return [s for s in self._scopes if s.fl == fl or s.fl == -1]

    def dereference(self, ref_no):
        return self._references[ref_no - 1]

class CDPServer(object):
    def __init__(self, dev, di, do):
        self.data_in = di
        self.data_out = do
        self.dev = dev
        self._monitor = ExecutionMonitor(dev, functools.partial(CDPServer._evt_stopped, self))
        self.__dispatch_setup()
        self._register_model = model_registers(dev)
        self._register_model.accessor = functools.partial(get_data_value, mroot=self._register_model)
        self._memory_model = model_memory(dev)
        self._memory_model.accessor = functools.partial(get_data_value, mroot=self._register_model)
        self._vt = Var_Tracker()
        self._vt.add_fixed_scope(self._register_model)
        self._vt.add_fixed_scope(self._memory_model)
        for c in self._register_model.children:
            if c.name == "rxcpu":
                s = ScopeModel("rxcpu registers")
                s2 = ScopeModel("rxcpu state")
                for r in c.children:
                    if r.name[0] == 'r' and r.name[1:].isdigit():
                        reg_no = int(r.name[1:])
                        reg_name = mips_regs.inv[reg_no]
                        reg_for_display = GenericModel(r.name, r.parent)
                        reg_for_display.display_name = reg_name
                        s.children += [reg_for_display]
                    if r.name == "pc":
                        ss = GenericModel(r.name, r.parent)
                        ss.display_name = "program counter"
                        ss.accessor = lambda r=r:self._register_model.accessor(r)
                        s2.children += [ss]
                    if r.name == "ir":
                        ss = GenericModel(r.name, r.parent)
                        ss.display_name = "instruction register"
                        ss.accessor = lambda r=r:self._register_model.accessor(r)
                        s2.children += [ss]
                        if not _no_capstone:
                            ss = GenericModel(r.name, r.parent)
                            ss.display_name = "instruction register (decoded)"
                            ss.accessor = lambda r=r:_disassemble_word(self._register_model.accessor(r))
                            s2.children += [ss]

                    if r.name in ["mode", "status"]:
                        ss = GenericModel(r.name, r.parent)
                        ss.accessor = lambda r=r:self._register_model.accessor(r)
                        for b in r.children:
                            cc = GenericModel(b.name, b.parent)
                            cc.accessor = lambda b=b:self._register_model.accessor(b)
                            ss.children += [cc]
                        s2.children += [ss]
                
                s.accessor = self._register_model.accessor
                self._vt.add_fixed_scope(s, fl=1)
                
                s2.accessor = lambda x: x.accessor()
                self._vt.add_fixed_scope(s2, fl=1)

        self._breakpoints = {}
        self._bp_replaced_insn = {}

    def __enter__(self):
        return self

    def __exit__(self, t, v, traceback):
        pass

    def __dispatch_setup(self):
        self.__dispatch_tbl = {}
        for i in self.__class__.__dict__:
            if len(i) > 5 and i[0:5] == "_cmd_":
                self.__dispatch_tbl[unicode(i[5:])] = getattr(self, i)

    def _dispatch_cmd(self, cmd):
        try:
            fncall = self.__dispatch_tbl[cmd["command"]]
        except:
            fncall = self._default_cmd
        fncall(cmd)

    def _cmd_initialize(self, cmd):
        self._seq = 1
        ex = {}
        ex["supportsConfigurationDoneRequest"] = True
        ex["supportEvaluateForHovers"] = False
        self._respond(cmd, True, ex=ex)

    def _cmd_launch(self, cmd):
        try:
            stop_now = cmd["arguments"]["stopOnEntry"]
        except:
            stop_now = False

        program = cmd["arguments"]["program"]
        self._image = Image(program)
        self.dev.rxcpu.reset()
        #self.dev.ma.mode.fast_ath_read_disable = 1
        #self.dev.ma.mode.cpu_pipeline_request_disable = 1
        #self.dev.ma.mode.low_latency_enable = 1
        self.dev.rxcpu.image_load(*self._image.executable)
        self._respond(cmd, True)

        if stop_now:
            b = {}
            b["reason"] = "launch"
            b["threadId"] = 1
            self._event("stopped", body = b)
        else:
            self._monitor.watch()

        self._event("initialized")

    def _cmd_setExceptionBreakpoints(self, cmd):
        self._respond(cmd, False)

    def _cmd_setBreakpoints(self, cmd):
        source = os.path.basename(cmd["arguments"]["source"]["path"])
        self._clear_breakpoint(source)
        breakpoints_set = []
        if "lines" in cmd["arguments"]:
            for line in cmd["arguments"]["lines"]:
                success = self._setup_breakpoint(source, line)
                b = {"verified": success, "line": line}
                breakpoints_set += [b]
        if "breakpoints" in cmd["arguments"]:
            for bp in cmd["arguments"]["breakpoints"]:
                line = bp["line"]
                if "condition" in bp:
                    success = False
                else:
                    success = self._setup_breakpoint(source, line)
                b = {"verified": success, "line": line}
                breakpoints_set += [b]
        self._respond(cmd, True, body = {"breakpoints": breakpoints_set})

    def __advance_to_next_line(self):
        while True:
            self.dev.rxcpu.mode.single_step = 1
            count = 0
            while self.dev.rxcpu.mode.single_step:
                count += 1
                if count > 500:
                    raise Exception("single step bit failed to clear")
            current_pc = self.dev.rxcpu.pc
            if not current_pc in self._bp_replaced_insn:
                ir_reg_val = self.dev.rxcpu.ir
                insn_from_mem = struct.unpack(">I", self.dev.rxcpu.tr_read(current_pc, 1))[0]
                if ir_reg_val != insn_from_mem:
                    print "ir reg is %x, should be %x, fixing." % (ir_reg_val, insn_from_mem)
                    self.dev.rxcpu.ir = insn_from_mem
                    ir_reg_val = self.dev.rxcpu.ir
                assert ir_reg_val == insn_from_mem
            else:
                self.__prepare_resume_from_breakpoint()
            if current_pc in self._image._addresses:
                break
        
    def _cmd_next(self, cmd):
        self._respond(cmd, True)
        pc = self.dev.rxcpu.pc
        cl = self._image.addr2line(pc)
        self._log_write("single step began at pc: %x, cl: %s" % (pc, cl))
        self.__advance_to_next_line()
        pc = self.dev.rxcpu.pc
        cl = self._image.addr2line(pc)
        self._log_write("single step completed at pc: %x, cl: \"%s\"" % (pc, cl))
        self.__prepare_resume_from_breakpoint()
        self._event("stopped", {"reason": "step", "threadId": 1})

    def _cmd_threads(self, cmd):
        t = {}
        t["id"] = 1
        t["name"] = "Main Thread"
        b = {}
        b["threads"] = [t]
        self._respond(cmd, True, body = b)

    def _cmd_disconnect(self, cmd):
        self._running = False
        self._respond(cmd, True)

    def _cmd_continue(self, cmd):
        self._respond(cmd, True)
        self._monitor.watch()


    def _cmd_pause(self, cmd):
        self._respond(cmd, True)
        self.dev.rxcpu.halt()

    def _cmd_stackTrace(self, cmd):
        self._vt.clear_dynamic_scopes()
        self._stack = self.__stack_unwind()
        frame_id = 1
        b = {"stackFrames": []}
        for f in self._stack:
            loc = self._image.loc_at(f["pc"])
            print "0x%x" % f["pc"]
            source_path = loc[3] + os.sep + loc[1]
            source_name = "fw" + os.sep + loc[1]
            s = {"name": source_name, "path": source_path}
            f = {"id": frame_id, "name": loc[0], "line": int(loc[2]), "column": 1, "source": s}
            b["stackFrames"] += [f]
            frame_id += 1
        self._respond(cmd, True, body = b)

    def __stack_unwind(self):
        frame_state_attrs = ["r%d" % x for x in range(32)] + ["pc"]
        frame_state = {}
        for a in frame_state_attrs:
            frame_state[a] = getattr(self.dev.rxcpu, a)
        if 0x8008000 <= frame_state["pc"] and 0x8008010 > frame_state["pc"]:
            return [frame_state]
        else:
            return self.__unwind_stack_from([frame_state])

    def __unwind_stack_from(self, frame_states):
        frame_state = self.__restore_cf(frame_states[-1])
        if frame_state is None:
            return frame_states
        return_address = frame_state["r31"]
        call_site = return_address - 8
        if 0x8000000 <= call_site and 0x8010000 > call_site:
            frame_state["pc"] = call_site
            if not frame_state["r31"] is None:
                return self.__unwind_stack_from(frame_states + [frame_state])
            else:
                return frame_states + [frame_state]
        else: 
            return frame_states + [frame_state]

    def __find_cfa_tbl_line_for(self, pc):
        result = None
        for entry in sorted(self._image._cfa_rule.keys(), reverse=True):
            if pc >= entry and entry != 0:
                result = self._image._cfa_rule[entry]
                break
        return result

    def __restore_cf(self, frame_state):
        new_frame_state = frame_state.copy()
        pc = frame_state["pc"]
        tbl_line = self.__find_cfa_tbl_line_for(pc)
        if tbl_line is None:
            return None
        cfa_rule = tbl_line["cfa"]
        if not cfa_rule.expr is None:
            raise Exception("DWARF expression unhandled in CFA")
        
        cfa = frame_state["r%d" % cfa_rule.reg]
        cfa += cfa_rule.offset
        new_frame_state["r29"] = cfa
        for reg in tbl_line:
            if reg in ["cfa", "pc"]: continue
            reg_rule = tbl_line[reg]
            if reg_rule.type != 'OFFSET':
                raise Exception("DWARF register rule type %s unhandled" % reg_rule.type)
            reg_val_addr = cfa + reg_rule.arg
            reg_val = struct.unpack(">I", self.dev.rxcpu.tr_read(reg_val_addr, 1))[0]
            new_frame_state["r%d" % reg] = reg_val

        return new_frame_state

    def _collect_scopes(self, frame):
        loc = self._image.loc_at(frame["pc"])
        func_name, cu_name, cu_line, source_dir = loc

        scopes = []
        if len(self._image._compile_units[cu_name]["variables"]) > 0:
            global_scope = ScopeModel("global variables")
            global_scope.children = self._collect_vars(self._image._compile_units[cu_name]["variables"], global_scope, frame)
            global_scope.accessor = lambda x: x.evaluator()

            scopes += [global_scope]

        if func_name:
            if len(self._image._compile_units[cu_name]["functions"][func_name]["args"]) > 0:
                argument_scope = ScopeModel("function arguments")
                argument_scope.children = self._collect_vars(self._image._compile_units[cu_name]["functions"][func_name]["args"], argument_scope, frame)
                argument_scope.accessor = lambda x: x.evaluator()

                scopes += [argument_scope]

            if len(self._image._compile_units[cu_name]["functions"][func_name]["vars"]) > 0:
                local_scope = ScopeModel("local variables")
                local_scope.children = self._collect_vars(self._image._compile_units[cu_name]["functions"][func_name]["vars"], local_scope, frame)
                local_scope.accessor = lambda x: x.evaluator()

                scopes += [local_scope]

        return scopes

    def _collect_vars(self, variables, scope, frame):
        def _var_pp(v):
            try: return "%x" % v
            except: return str(v)

        collected = []
        for v in variables:
            o = GenericModel(v, scope, scope)
            o.evaluator = lambda v=v: _var_pp(self._image.get_expr_evaluator().process_expr(self.dev, variables[v]["location"], frame)) 
            collected += [o]
        return collected

    def _cmd_scopes(self, cmd):
        
        frame_id = cmd["arguments"]["frameId"]
        if not frame_id in self._vt._known_frame_levels:
            frame = self._stack[frame_id - 1]   
            dynamic_scopes = self._collect_scopes(frame)
            for scope in dynamic_scopes:
                self._vt.add_dynamic_scope(scope, frame_id)

        scopes = []
        for s in self._vt.get_scopes(frame_id):
            scopes += [{"name": s.name, "variablesReference": s.variablesReference, "expensive": True}]
        b = {"scopes": scopes}
        self._respond(cmd, True, body = b)

    def _cmd_variables(self, cmd):
        members = self._vt.dereference(cmd["arguments"]["variablesReference"])
        b = {}
        b["variables"] = []
        for child in members.children:
            o = {}

            try: o["name"] = child.display_name
            except: o["name"] = child.name

            if hasattr(child, "variablesReference"):
                o["variablesReference"] = child.variablesReference
                o["value"] = ""
            else:
                o["variablesReference"] = 0
                data_value = child.scope.accessor(child)
                try: o["value"] = "%x" % data_value
                except: o["value"] = str(data_value)
            b["variables"] += [o]

        self._respond(cmd, True, body = b)

    def _default_cmd(self, cmd):
        self._log_write("unknown command: %s" % cmd["command"])
        self._respond(cmd, False)

    def _log_write(self, data):
        print data.strip()
        sys.stdout.flush()

    def _evt_stopped(self):
        b = {"threadId": 1}
        pc = self.dev.rxcpu.pc
        if self.dev.rxcpu.status.halted:
            b["reason"] = "pause"
            if not self._image.addr2line(pc):
                print "halted at unknown pc %x, advancing..." % pc
                self.__advance_to_next_line()
                pc = self.dev.rxcpu.pc
                cl = self._image.addr2line(pc)
                print "finished halting at pc %x, \"%s\"" % (pc, cl)
                self.__prepare_resume_from_breakpoint()
        else:
            if pc in self._bp_replaced_insn:
                b["reason"] = "breakpoint"
                print "breakpoint reached at %x (\"%s\")" % (pc, self._image.addr2line(pc))
                self.__prepare_resume_from_breakpoint()
            else:
                b["reason"] = "exception"
                b["text"] = "status: %x" % self.dev.rxcpu.status.word
                print "stopped on unknown rxcpu exception at %x (\"%s\"), status: %x" % (pc, self._image.addr2line(pc), self.dev.rxcpu.status.word)
        self._event("stopped", body = b)

    def _event(self, event, body = None):
        r = {}

        r["type"] = "event"

        r["seq"] = self._seq
        self._seq += 1

        r["event"] = event
        if body is not None:
            r["body"] = body

        self.send(r)

    def _respond(self, req, success, message = None, body = None, ex=None):
        r = {}

        r["type"] = "response"
        
        r["seq"] = self._seq
        self._seq += 1
        
        r["request_seq"] = req["seq"]
        r["success"] = True if success else False
        r["command"] = req["command"]
        if message is not None:
            r["message"] = message
        if body is not None:
            r["body"] = body
        if ex is not None:
            r.update(ex)
        self.send(r)

    def __insn_repl(self, addr, replacement):
        original_insn = struct.unpack("!I", self.dev.rxcpu.tr_read(addr, 1))[0]
        self.dev.rxcpu.tr_write_dword(addr, replacement)
        return original_insn

        try:
            self._breakpoints[addr] = original_insn
        except:
            self._breakpoints = {addr: original_insn}

    def _setup_breakpoint(self, filename, line):
        try:
            line_addrs = self._image.line2addr(filename, line)
        except:
            return False
        if not filename in self._breakpoints:
            self._breakpoints[filename] = {}

        current_breakpoints = self._breakpoints[filename]

        for addr in line_addrs:
            if line in current_breakpoints and addr in current_breakpoints[line]:
                print "breakpoint at %s+%d already set" % (filename, line)
            else:
                self._bp_replaced_insn[addr] = self.__insn_repl(addr, 0xd)
                try: current_breakpoints[line] += [addr]
                except: current_breakpoints[line] = [addr]
                print "breakpoint set at \"%s+%d\" (%x)" % (filename, line, addr)
        return True

    def _clear_breakpoint(self, filename, line_no = None):
        try:
            current_breakpoints = self._breakpoints[filename]
        except:
            return
        if line_no is None:
    	    lines = current_breakpoints.keys()
        else:
            lines = [line_no]
        for line in lines:
            line_addrs = current_breakpoints[line]
            for addr in line_addrs:
                self.__insn_repl(addr, self._bp_replaced_insn[addr])
                del self._bp_replaced_insn[addr]
                print "breakpoint cleared at \"%s+%d\" (%x)" % (filename, line, addr)
            del self._breakpoints[filename][line]

    def __prepare_resume_from_breakpoint(self):
        pc = self.dev.rxcpu.pc
        if pc in self._bp_replaced_insn:
            replacement = self._bp_replaced_insn[pc]
            print "pc %x is a soft breakpoint, restoring ir with %x" % (pc, replacement) 
            self.dev.rxcpu.ir = replacement

    def send(self, resp):
        r = json.dumps(resp, separators=(",",":"))
        cl = len(r)
        txt = "Content-Length: %d%s%s" % (cl, LINE_SEP + LINE_SEP, r)
        
        self._log_write("sent: %s\n" % r)
        self.data_out.write(txt)
        self.data_out.flush()
            
    def recv(self):
        h = self.data_in.readline()
        content_length = int(h.split(" ")[1])
        d = self.data_in.readline()
        d = self.data_in.read(content_length)
        self._log_write("rcvd: %s\n" % repr(d))
        try:
            j = json.loads(d)
        except:
            self._log_write("EXCEPTION!")
        return j

    def run(self):
        self._running = True
        while self._running:
            j = self.recv()
            try:
                self._dispatch_cmd(j)
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                raise e
        return 0
        


