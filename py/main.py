#!/usr/bin/env python

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
import sys
import subprocess
import platform
import logging
class tglog(logging.Formatter):
    cmap= {logging.NOTSET: '?', logging.DEBUG: '.', logging.INFO: '+', 
            logging.WARNING: '-', logging.ERROR: '!', logging.CRITICAL: '*'}
    def format(self, rec):
        return "[%s] %s" % (self.cmap[rec.levelno], rec.msg % rec.args)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = tglog()
ch.setFormatter(formatter)
logger.addHandler(ch)

sys_name = platform.system()

if __name__ == "__main__":
    tgdir = sys.argv[0]
    if tgdir != "":
        tgdir = os.path.abspath(tgdir)
        tgdir = os.sep.join(tgdir.split(os.sep)[:-2])
        cwd = os.getcwd()
        if tgdir != cwd:
            logger.warn("resetting cwd (was %s, now %s)", cwd, tgdir)
            os.chdir(tgdir)

from device import Device

if sys_name == "Linux":
    from interfaces.sysfs import SysfsInterface
    from interfaces.vfio import VfioInterface
    from interfaces.uio import UioInterface
elif sys_name == "Windows" or sys_name == "cli":
    from interfaces.win import WinInterface
else:
    raise NotImplementedError("this version of thundergate only runs on linux and windows")

import reutils

import argparse

def banner():
    print """

 #######                                            #####
    #    #    # #    # #    # #####  ###### #####  #     #   ##   ##### ######
    #    #    # #    # ##   # #    # #      #    # #        #  #    #   #
    #    ###### #    # # #  # #    # #####  #    # #  #### #    #   #   #####
    #    #    # #    # #  # # #    # #      #####  #     # ######   #   #
    #    #    # #    # #   ## #    # #      #   #  #     # #    #   #   #
    #    #    #  ####  #    # #####  ###### #    #  #####  #    #   #   ######
                          
                                 Version 0.9.6a
                    Copyright (c) 2015-2016 Saul St John
                             http://thundergate.io
"""

def main(args):
    parser = argparse.ArgumentParser()
    if sys_name == "Linux":
        parser.add_argument("--device", help="BDF of tg3 PCI device", default=None)
        parser.add_argument("--devid", help="id of tg3 PCI device", default=None)
    parser.add_argument("-p", "--ptvsd", help="enable ptvsd server", action="store_true")
    parser.add_argument("--ptvsdpass", help="ptvsd server password", default=None)
    parser.add_argument("-t", "--tests", help="run tests", action="store_true")
    parser.add_argument("-s", "--shell", help="ipython cli", action="store_true")
    parser.add_argument("-b", "--backup", help="create eeprom backup", action="store_true", default=False)
    parser.add_argument("-d", "--driver", help="load userspace tap driver", action="store_true")
    parser.add_argument("-i", "--install", help="install thundergate firmware", action="store_true")
    parser.add_argument("--wait", help="wait for debugger attachment at startup", action="store_true")
    parser.add_argument("--cdpserver", help="launch VS Code debug protocol server", action="store_true")
    parser.add_argument("-g", "--gui", help="launch wxpython gui", action="store_true")

    args = parser.parse_args(args=args[1:])

    if args.cdpserver:
        conout = sys.stdout
        conin = sys.stdin
        sys.stdin = open(os.devnull, "r")
        sys.stdout = open("cdp.%d.log" % os.getpid(), "w")
        
    banner()

    ima = "inspector"
    try: 
        if args.driver: ima = "userspace driver"
    except: 
        pass

    logger.info("tg3 %s initializing" % ima)
    logger.debug("process id is %d" % os.getpid())

    if args.ptvsd:
        import ptvsd
        ptvsd.enable_attach(secret=args.ptvsdpass)
        if args.wait:
            logger.info("waiting for ptvsd client...")
            ptvsd.wait_for_attach()
            logger.info("ptvsd client attached!")
            ptvsd.break_into_debugger()
        else:
            logger.info("ptvsd server enabled")
    elif args.wait:
        print "[!] press 'enter' to continue..."
        raw_input()

    if sys_name == 'Linux':
        if args.device is None:
            devid = args.devid
            if devid is None:
                devid = "14e4:1682"
            dbdf = subprocess.check_output(["lspci", "-d %s" % devid, "-n"]).split(" ")[0].strip()
            if '' == dbdf:
                logger.error("tigon3 device not found")
                return 1
        else:
            dbdf = args.device
        if len(dbdf.split(':')) == 2:
            dbdf = "0000:%s" % dbdf

        if not os.path.exists("/sys/bus/pci/devices/%s/" % dbdf):
            logger.error(
                "device resources at /sys/bus/pci/devices/%s/ not found; " +
                "is sysfs mounted?", dbdf)
            return 1
        
        try:
            kmod = os.readlink("/sys/bus/pci/devices/%s/driver" % dbdf).split('/')[-1]
        except:
            kmod = '' 
        if kmod == 'vfio-pci':
            dev_interface = VfioInterface(dbdf)
        elif kmod == 'uio_pci_generic':
            dev_interface = UioInterface(dbdf)
        else:
            dev_interface = SysfsInterface(dbdf)

        if kmod == 'tg3' and args.driver:
            logger.error("device is currently bound to tg3; this won't work")
            return 1

    elif sys_name == 'Windows' or sys_name == 'cli':
        try:
            dev_interface = WinInterface()
        except:
            dev_interface = None
    if not args.backup:
        if not os.path.exists("eeprom.bak"):
            logger.warn("no backup image found")
            if not args.cdpserver:
                resp = raw_input("\n\n" + 
                        "would you like to create a backup image (y/n): ")
                if resp[0] in "yY":
                    args.backup = True

    with Device(dev_interface) as dev:
        if args.backup:
            dev.nvram.init()
            dev.nvram.dump_eeprom("eeprom.bak")
            logger.info("eeprom backup saved as 'eeprom.bak'")

        if args.install:
            from tginstall import TgInstaller
            with TgInstaller(dev) as i:
                return i.run()
        elif args.shell:
            from shelldrv import ShellDriver
            with ShellDriver(dev) as shell:
                if args.tests:
                    from testdrv import TestDriver
                    with TestDriver(dev) as test:
                        test.run()
                        return shell.run(loc=locals())
                else:
                    return shell.run(loc=locals())
        elif args.cdpserver:
            from cdpserver import CDPServer
            with CDPServer(dev, conin, conout) as server:
                return server.run()
        elif args.gui:
            import gui
            dev.reset(cold = True)
            gui._run(dev)
        else:
            if args.driver:
                import tap
                return tap.run(dev)
            elif args.tests:
                from testdrv import TestDriver
                with TestDriver(dev) as test:
                    return test.run()
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))
