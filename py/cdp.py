'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016  Saul St. John

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

def find_tgmain():
    pname = os.path.abspath(sys.argv[0])
    pdir = os.path.dirname(pname)
    mname = ""
    if os.path.exists(pdir + os.sep + "main.py"):
        mname = pdir + os.sep + "main.py"
    else:
        try:
            sname = os.readlink(pname)
            sdir = os.path.dirname(sname)
            if os.path.exists(sdir + os.sep + "main.py"):
                mname = sdir + os.sep + "main.py"
        except: pass
    if len(sys.argv) > 1:
        adir = sys.argv[1]
        if os.path.exists(adir + os.sep + "py" + os.sep + "main.py"):
            mname = adir + os.sep + "py" + os.sep + "main.py"
    if mname == "":
        try:
            edir = os.environ["TGDIR"]
            if os.path.exists(edir + os.sep + "py" + os.sep + "main.py"):
                mname = edir + os.sep + "py" + os.sep + "main.py"
        except: pass
    if mname == "" and os.path.exists(pdir + os.sep + "tgdir.conf"):
        with open(pdir + os.sep + "tgdir.conf", "r") as f:
            fdir = f.readline().strip()
        if os.path.exists(fdir + os.sep + "py" + os.sep + "main.py"):
            mname = fdir + os.sep + "py" + os.sep + "main.py"
    if mname == "":
        raise Exception("couldn't locate thundergate directory")
    return mname

if __name__ == "__main__":
    main_file = find_tgmain()
    os.chdir(os.path.dirname(os.path.dirname(main_file)))
    sys.path += [os.path.dirname(main_file)]
    import main
    sys.exit(main.main([main_file, "--cdpserver"]))

p = platform.system()
if "Windows" == p:
	LINE_SEP = "\n"
else:
	LINE_SEP = "\r\n"
del p

from image import Image
from monitor import ExecutionMonitor

class CDPServer(object):
    def __init__(self, dev, di, do):
        self.data_in = di
        self.data_out = do
        self.dev = dev
        self._monitor = ExecutionMonitor(dev)
        self.__dispatch_setup()

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
        scopes = []
        func, fname, _, _ = self._top_of_stack
        if len(self._image._compile_units[fname]["variables"]) > 0:
            scopes += [{"name": "Globals", "variablesReference": 1, "expensive": True}]

        if "" != func:
            if len(self._image._compile_units[fname]["functions"][func]["args"]) > 0:
                scopes += [{"name": "Arguments", "variablesReference": 2, "expensive": True}]
            if len(self._image._compile_units[fname]["functions"][func]["vars"]) > 0:
                scopes += [{"name": "Locals", "variablesReference": 3, "expensive": True}]
        b = {"scopes": scopes}
        self._respond(cmd, True, body = b)

    def _cmd_variables(self, cmd):
        func, fname, _, _ = self._top_of_stack
        ref = cmd["arguments"]["variablesReference"]
        b = {}
        if ref == 1:
            variables = self._image._compile_units[fname]["variables"]
        elif ref == 2:
            variables = self._image._compile_units[fname]["functions"][func]["args"]
        elif ref == 3:
            variables = self._image._compile_units[fname]["functions"][func]["vars"]
        else:
            variables = []

        b["variables"] = []
        for v in variables:
            o = {}
            o["name"] = v
            try:
                o["value"] = "%x" % self._image.expr_evaluator.process_expr(self._dev, variables[v]["location"])
            except:
                o["value"] = "(unknown)"
            o["variablesReference"] = 0
            b["variables"] += [o]

        self._respond(cmd, True, body = b)
            
    def _default_cmd(self, cmd):
        self._log_write("unknown command: %s" % cmd["command"])
        self._respond(cmd, False)

    def _log_write(self, data):
        print data.strip()
        sys.stdout.flush()

    def _evt_stopped(self):
        b = {"reason": "pause", "threadId": 1}
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
        

