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
import platform

from device import Device
from testdrv import TestDriver
from shelldrv import ShellDriver
from tginstall import TgInstaller
from tapdrv import TapDriver

sys_name = platform.system()

if sys_name == "Linux":
    from sysfsint import SysfsInterface
    from vfioint import VfioInterface
    from uioint import UioInterface
elif sys_name == "Windows":
    from winint import WinInterface
else:
    raise NotImplementedError("this version of thundergate only runs on linux and windows")

import reutils

import argparse


if __name__ == "__main__":
    print """

 #######                                            #####
    #    #    # #    # #    # #####  ###### #####  #     #   ##   ##### ######
    #    #    # #    # ##   # #    # #      #    # #        #  #    #   #
    #    ###### #    # # #  # #    # #####  #    # #  #### #    #   #   #####
    #    #    # #    # #  # # #    # #      #####  #     # ######   #   #
    #    #    # #    # #   ## #    # #      #   #  #     # #    #   #   #
    #    #    #  ####  #    # #####  ###### #    #  #####  #    #   #   ######
                          
                                 Version 0.9.0
                        Copyright (c) 2015 Saul St John
                             http://thundergate.io
"""

    parser = argparse.ArgumentParser()
    if sys_name == "Linux":
        parser.add_argument("device", help="BDF of tg3 PCI device")
        parser.add_argument("-u", "--uio", help="use uio pci generic interface", action="store_true")
        parser.add_argument("-v", "--vfio", help="use vfio interface", action="store_true")
    parser.add_argument("-t", "--tests", help="run tests", action="store_true")
    parser.add_argument("-s", "--shell", help="ipython cli", action="store_true")
    parser.add_argument("-b", "--backup", help="create eeprom backup", action="store_true", default=False)
    parser.add_argument("-d", "--driver", help="load userspace tap driver", action="store_true")
    parser.add_argument("-i", "--install", help="install thundergate firmware", action="store_true")

    args = parser.parse_args()
    
    ima = "inspector"
    try: 
        if args.driver: ima = "userspace driver"
    except: 
        pass

    print "[+] tg3 %s initializing" % ima

    if sys_name == 'Linux':
        dbdf = args.device
        if len(dbdf.split(':')) == 2:
            dbdf = "0000:%s" % dbdf

        if not os.path.exists("/sys/bus/pci/devices/%s/" % dbdf):
            print "[-] device resources at /sys/bus/pci/devices/%s/ not found; is sysfs mounted?" % dbdf
            sys.exit(1)

        dev_interface = SysfsInterface(dbdf)
        if args.vfio:
            odrv = os.readlink("/sys/bus/pci/devices/%s/driver" % dbdf).split('/')[-1]
            if odrv != 'vfio-pci':
                raise Exception("device %s currently bound by %s, bind to vfio-pci instead" % (dbdf, odrv))
            dev_interface = VfioInterface(dbdf)

        if args.uio:
            odrv = os.readlink("/sys/bus/pci/devices/%s/driver" % dbdf).split('/')[-1]
            if odrv != 'uio_pci_generic':
                raise Exception("device %s currently bound by %s, bind to uio_pci_generic instead")
            dev_interface = UioInterface(dbdf)
    elif sys_name == 'Windows':
        dev_interface = WinInterface()

    if not args.backup:
        if not os.path.exists("eeprom.bak"):
            print "[!] you do not currently have a backup eeprom image saved."
            if raw_input("[?] would you like to create a backup image (y/n): ")[0] in "yY":
                args.backup = True

    with Device(dev_interface) as dev:
        if args.backup:
            dev.nvram.init()
            dev.nvram.dump_eeprom("eeprom.bak")
            print "[+] eeprom backup saved as 'eeprom.bak'"

        if args.install:
            with TgInstaller(dev) as i:
                i.run()
        elif args.shell:
            with ShellDriver(dev) as shell:
                if args.driver:
                    with TapDriver(dev) as tap:
                        shell.run(loc=locals())
                elif args.tests:
                    with TestDriver(dev) as test:
                        test.run()
                        shell.run(loc=locals())
                else:
                    shell.run(loc=locals())
        else:
            if args.driver:
                with TapDriver(dev) as tap:
                    tap.run()
            elif args.tests:
                with TestDriver(dev) as test:
                    test.run()
    
    print "[+] tg3 %s terminated" % ima

def initialize(argv):
    pass