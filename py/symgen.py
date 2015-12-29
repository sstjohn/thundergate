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

import ctypes
import device

xtra = [("reg", 0xc0000000),
        ("rom", 0x40000000),
        ("scratchpad", 0x08000000)]

if __name__ == "__main__":
    for m in device.tg3_mem:
        print "%s = 0x%x;" % (m[0], m[2])
    for r in device.tg3_blocks:
        print "%s = 0x%x;" % (r[0], r[1] + 0xc0000000)
    for x in xtra:
        print "%s = 0x%x;" % (x[0], x[1])

