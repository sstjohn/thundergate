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

import ctypes

try:
    from traitlets.config import Config
except:
    from IPython.config.loader import Config

cfg = Config()
pm = cfg.PromptManager
pm.in_template = 'In <\\#>: '
pm.in2_template = '   .\\D.: '
pm.out_template = 'Out<\\#>: '

cfg.PlainTextFormatter.type_printers = {int: lambda n, p, cycle: p.text("0x%x" % n),
                                        long: lambda n, p, cycle: p.text("0x%x" % n)}

cfg.InteractiveShellApp.exec_lines = ['from magic import _register_device_magic',
                                      '_register_device_magic(dev)']

cfg.TerminalInteractiveShell.banner1 = "[+] launching interactive shell"

from IPython import start_ipython

from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

class ShellDriver(object):
    def __init__(self, dev):
        self.dev = dev

    def __enter__(self):
        self.dev.init()
        return self

    def __exit__(self, t, v, traceback):
        pass

    def test(self):
        from testdrv import TestDriver
        with TestDriver(self.dev) as tdrv:
            tdrv.run()

    def run(self, loc):
        start_ipython(argv=[], 
                      user_ns=loc, 
                      config=cfg, 
                      banner1="[+] launching interactive shell", 
                      exit_msg="[+] interactive shell terminating")
        return 0