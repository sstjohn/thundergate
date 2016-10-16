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

p = platform.system()
if "Windows" == p:
	LINE_SEP = "\n"
else:
	LINE_SEP = "\r\n"
del p

from image import Image
from monitor import ExecutionMonitor
from datamodel import model_registers, model_memory, get_data_value

class Var_Tracker(object):
    def __init__(self):
        self._references = []
        self._scopes = []
        self._fixed_reference_end = None
        self._fixed_scope_end = None

    def _assign_variablesReference(self, v):
	    self._references.append(v)
	    v.variablesReference = len(self._references)
    
    def _add_variables_references(self, v):
        if hasattr(v, "children") and isinstance(v.children, list) and len(v.children) > 0:
            self._assign_variablesReference(v)
            for c in v.children:
                c.scope = v.scope
                self._add_variables_references(c)
    
    def add_fixed_scope(self, s):
        if self._fixed_scope_end:
            raise Exception("fixed scopes cannot be added when dynamic scopes are present")
        self._add_scope(s)
        
    def _add_scope(self, s):
        print "adding scope %s" % s.name
        self._assign_variablesReference(s)
        self._scopes += [s]
        for c in s.children:
            c.scope = s
            self._add_variables_references(c)
            
    def add_dynamic_scope(self, s):
        if not self._fixed_scope_end:
            self._fixed_scope_end = len(self._scopes)
            self._fixed_reference_end = len(self._references)
        self._add_scope(s)

    def clear_dynamic_scopes(self):
        self._scopes = self._scopes[:self._fixed_scope_end]
        self._references = self._references[:self._fixed_reference_end]
        self._fixed_scope_end = None
        self._fixed_reference_end = None

    def get_scopes(self):
        return self._scopes
        
    def dereference(self, ref_no):
        return self._references[ref_no - 1]

class CDPServer(object):
    def __init__(self, dev, di, do):
        self.data_in = di
        self.data_out = do
        self.dev = dev
        self._monitor = ExecutionMonitor(dev)
        self.__dispatch_setup()      
        self._register_model = model_registers(dev)
        self._memory_model = model_memory(dev)
        self._vt = Var_Tracker()
        self._vt.add_fixed_scope(self._register_model)
        self._vt.add_fixed_scope(self._memory_model)
                    
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
        self.dev.rxcpu.image_load(*self._image.executable)
        self._respond(cmd, True)

        if stop_now:
            b = {}
            b["reason"] = "launch"
            b["threadId"] = 1
            self._event("stopped", body = b)
        else:
            self.dev.rxcpu.resume()

        self._event("initialized")

    def _cmd_setExceptionBreakpoints(self, cmd):
        self._respond(cmd, True)

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

    def _cmd_next(self, cmd):
        self._respond(cmd, True)
        initial_pc = self.dev.rxcpu.pc
        current_pc = initial_pc
        cl = self._image.addr2line(initial_pc)
        self._log_write("initial pc: %x, cl: %s" % (initial_pc, cl))
        while True: 
            self.dev.rxcpu.mode.single_step = 1
            count = 0
            while self.dev.rxcpu.mode.single_step:
                count += 1
                if count > 500:
                    raise Exception("single step bit failed to clear")
                self.msleep(10)
            current_pc = self.dev.rxcpu.pc
            if current_pc in self._image._addresses:
                break
        cl = self._image.addr2line(current_pc)
        self._log_write("now, pc: %x, cl: \"%s\"" % (current_pc, cl))
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
        callback = functools.partial(CDPServer._evt_stopped, self)
        if self.dev.rxcpu.status.invalid_instruction:
            self.dev.rxcpu.resume_from_breakpoint()
        else:
            self.dev.rxcpu.resume()
        self._monitor.watch(callback)
        self._respond(cmd, True)

    def _cmd_pause(self, cmd):
        self._respond(cmd, True)
        self.dev.rxcpu.halt()

    def _cmd_stackTrace(self, cmd):
        self._top_of_stack = self._image.top_frame_at(self.dev.rxcpu.pc)
        frame_name, source_name, source_line, source_dir = self._top_of_stack
        source_path = source_dir + os.sep + source_name
        source_name = "fw" + os.sep + source_name
        s = {"name": source_name, "path": source_path}
        f = {"id": 1, "name": frame_name, "line": int(source_line), "column": 1, "source": s}

        b = {"stackFrames": [f]}
        self._respond(cmd, True, body = b)

    def _cmd_scopes(self, cmd):
        self._vt.clear_dynamic_scopes()   
        #func, fname, _, _ = self._top_of_stack
        #if len(self._image._compile_units[fname]["variables"]) > 0:
        #    scopes += [{"name": "Globals", "variablesReference": 1, "expensive": True}]

        #if "" != func:
        #    if len(self._image._compile_units[fname]["functions"][func]["args"]) > 0:
        #        scopes += [{"name": "Arguments", "variablesReference": 2, "expensive": True}]
        #    if len(self._image._compile_units[fname]["functions"][func]["vars"]) > 0:
        #        scopes += [{"name": "Locals", "variablesReference": 3, "expensive": True}]
                
        #scopes += [{"name": "CPU", "variablesReference": 4, "expensive": True}]
        scopes = []
        for s in self._vt.get_scopes():
            scopes += [{"name": s.name, "variablesReference": s.variablesReference, "expensive": True}]
        b = {"scopes": scopes}
        self._respond(cmd, True, body = b)

    def _cmd_variables(self, cmd):
        members = self._vt.dereference(cmd["arguments"]["variablesReference"])
        b = {}
        b["variables"] = []
        for child in members.children:
            o = {"name": child.name}
            #try: 
            #    o["variablesReference"] = child.variablesReference
            #except: 
            if hasattr(child, "variablesReference"):
                o["variablesReference"] = child.variablesReference
                o["value"] = ""
            else:
                o["variablesReference"] = 0
                data_value = get_data_value(child, child.scope)
                try: o["value"] = "%x" % data_value
                except: o["value"] = str(data_value)
            b["variables"] += [o]
            
        self._respond(cmd, True, body = b)
                
        '''
        func, fname, _, _ = self._top_of_stack
        ref = cmd["arguments"]["variablesReference"]
        b = {}
        if 0 < ref < 4:
            if ref == 2:
                variables = self._image._compile_units[fname]["functions"][func]["args"]
            elif ref == 3:
                variables = self._image._compile_units[fname]["functions"][func]["vars"]
            else:
                variables = self._image._compile_units[fname]["variables"]

            b["variables"] = []
            for v in variables:
                o = {}
                o["name"] = v
                v_value = self._image.get_expr_evaluator().process_expr(self.dev, variables[v]["location"]) 
                print "variables[v][\"location\"] = %s\n" % variables[v]["location"]
                if isinstance(v_value, (int, long)):
                    o["value"] = "%x" % v_value
                else:
                    o["value"] = str(v_value)
                o["variablesReference"] = 0
                b["variables"] += [o]

            self._respond(cmd, True, body = b)               
        elif ref == 4:
            variables = []
            for child in self._rxcpu_registers_model.children:
                o = {}
                o["name"] = child.name
                o["value"] = 0
                o["variablesReference"] = 0
                variables += [o]
            self._respond(cmd, True, body = {"variables": variables})
        ''' 
            
    def _default_cmd(self, cmd):
        self._log_write("unknown command: %s" % cmd["command"])
        self._respond(cmd, False)

    def _log_write(self, data):
        print data.strip()
        sys.stdout.flush()

    def _evt_stopped(self):
        print "!!!!! stopped !!!!!!"
	if self.dev.rxcpu.status.halted:
	    reason = "pause"
	elif self.dev.rxcpu.status.invalid_instruction:
	    if self.dev.rxcpu.pc in self.dev.rxcpu._breakpoints:
		reason = "breakpoint"
	    else:
		reason = "invalid instruction"
	else:
		reason = "unknown"
        b = {"reason": reason, "threadId": 1}
        print "!!!! sending event !!!!!"
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

    def _setup_breakpoint(self, filename, line):
	try:
	    addr = self._image.line2addr(filename, line)
        except:
            return False
	try:
	    current_breakpoints = self._breakpoints[filename]
	except:
	    current_breakpoints = {}
        if line in current_breakpoints and current_breakpoints[line] == addr:
	    return True
        self.dev.rxcpu.set_breakpoint(addr)
        current_breakpoints[line] = addr
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
	    try:
		addr = current_breakpoints[line]
	    except:
		continue
	    dev.rxcpu.clear_breakpoint(addr)
	    del self._breakpoints[filename][line]

    def send(self, resp):
        r = json.dumps(resp, separators=(",",":"))
        cl = len(r)
        txt = "Content-Length: %d%s%s" % (cl, LINE_SEP + LINE_SEP, r)
        
        self._log_write("out:\n%s\n" % txt)
        self.data_out.write(txt)
        self.data_out.flush()
            
    def recv(self):
        h = self.data_in.readline()
        self._log_write("in:\n%s" % repr(h))
        content_length = int(h.split(" ")[1])
        d = self.data_in.readline()
        self._log_write("%s" % repr(d))
        d = self.data_in.read(content_length)
        self._log_write("%s\n" % repr(d))
        self._log_write("len(d): %d\n" % len(d))
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
        


