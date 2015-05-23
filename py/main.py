#!/usr/bin/env python

'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015  Saul St. John

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

from device import Device
from testdrv import TestDriver
from shelldrv import ShellDriver
from tapdrv import TapDriver
from sysfsint import SysfsInterface
from vfioint import VfioInterface
from uioint import UioInterface
from tginstall import TgInstaller
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
                          
                                 Version 0.5.0
                        Copyright (c) 2015 Saul St John
                             http://thundergate.io
"""

    parser = argparse.ArgumentParser()
    parser.add_argument("device", help="BDF of tg3 PCI device")
    parser.add_argument("-i", "--install", help="install thundergate firmware", action="store_true")
    parser.add_argument("-u", "--uio", help="use uio pci generic interface", action="store_true")
    parser.add_argument("-v", "--vfio", help="use vfio interface", action="store_true")
    parser.add_argument("-d", "--driver", help="load userspace tap driver", action="store_true")
    parser.add_argument("-t", "--tests", help="run tests", action="store_true")
    parser.add_argument("-s", "--shell", help="ipython cli", action="store_true")

    args = parser.parse_args()

    ima = "userspace driver" if args.driver else "inspector"

    print "[+] tg3 %s initializing" % ima

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

    with Device(dev_interface) as dev:
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
