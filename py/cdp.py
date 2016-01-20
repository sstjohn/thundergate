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

class CDPServer(object):
    def __init__(self, data_in, data_out, log=False):
        self.data_in = data_in
        self.data_out = data_out
        self.logging = log
        self.__dispatch_setup()
        if log:
            self.__logging_setup()

    def __logging_setup(self):
        f = "CDPServer.%d.txt" % os.getpid()
        self.logfile = open(f, "w", 0)
    
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
        self._respond(cmd, True)
        try:
            stop_now = cmd["arguments"]["stopOnEntry"]
        except:
            stop_now = False
        if stop_now:
            b = {}
            b["reason"] = "launch"
            self._event("stopped", body = b)
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
        self._respond(cmd, True)
        sys.exit(0)

    def _default_cmd(self, cmd):
        self._log_write("unknown command: %s" % cmd["command"])
        self._respond(cmd, False)

    def _log_write(self, data):
        if self.logging:
            self.logfile.write(data)

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
        txt = "Content-Length: %d\r\n\r\n%s" % (cl, r)
        
        self._log_write("out:\n%s\n" % txt)
        self.data_out.write(txt)
        self.data_out.flush()
            
    def recv(self):
        h = self.data_in.readline()
        self._log_write("in:\n%s" % h)
        content_length = int(h.split(" ")[1])
        d = self.data_in.readline()
        self._log_write("%s" % d)
        d = self.data_in.read(content_length)
        self._log_write("%s\n" % d)
        self._log_write("len(d): %d\n" % len(d))
        try:
            j = json.loads(d)
        except:
            self._log_write("EXCEPTION!")
        return j

if __name__ == "__main__":
    c = CDPServer(sys.stdin, sys.stdout, True)
    try:
        while True:
            j = c.recv()
            c._dispatch_cmd(j)
    finally:
        c.logfile.close()
