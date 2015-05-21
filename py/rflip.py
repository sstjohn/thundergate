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

import ctypes

import sys
import tglib as tg

def rflip(c):
        fields = []

        d = type(c.__name__ + "_x", c.__bases__, {})

        is_struct = ctypes.Structure in c.__bases__
        is_bf = is_struct
        mem_sz = 0 if is_struct else -1

        for f in c._fields_:
                fname = f[0]

                try:
                        fields += [(fname, rflip(f[1]))]
                except:
                        fields += [(fname, f[1])]

                if not is_struct:
                        continue

                if len(f) < 3:
                        is_bf = False

                if mem_sz == 0:
                        mem_sz = ctypes.sizeof(f[1])
                elif mem_sz != ctypes.sizeof(f[1]):
                        mem_sz = -1

        if is_bf:
                fields = []
                for f in c._fields_[::-1]:
                        fields += [(f[0], f[1], f[2])]
        elif (ctypes.sizeof(c) == 2 or ctypes.sizeof(c) == 4) and mem_sz > 0:
                fields = fields[::-1]

        try:
                d._anonymous_ = c._anonymous_
        except:
                pass

        d._fields_ = fields

	if ctypes.sizeof(c) != ctypes.sizeof(d):
		raise Exception("sizeof flipped struct %s (%d) != sizeof struct %s (%d)" % (d, ctypes.sizeof(d), c, ctypes.sizeof(c)))

        return d

for tname in tg.__dict__:
    if tname[-5:] == "_regs":
        globals()[tname[:-5]] = rflip(getattr(tg, tname))
