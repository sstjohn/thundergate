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

from ctypes import *

class FirmwareHeader(BigEndianStructure):
    _fields_ = [("version", c_uint32),
                ("base_addr", c_uint32),
                ("length", c_uint32)]


class FirmwareImage(object):
    @staticmethod
    def load(fname):
        with open(fname, "rb") as f:
            return FirmwareImage(f)

    def __init__(self, fd):
        self._data_in = fd.read()

        self.hdr = FirmwareHeader.from_buffer(create_string_buffer(self._data_in[0:0xc]))
        if self.hdr.length == 0xffffffff:
            self.shdrs = []
            self.imgs = []
            i = 0xc
            while i < len(self._data_in):
                new_hdr = FirmwareHeader.from_buffer(create_string_buffer(self._data_in[i:i+0xc]))
                self.shdrs += [new_hdr]
                l = new_hdr.length
                self.imgs += [self._data_in[i+0xc:i+l]]
                i += l
        else:
            self.img = self._data_in[0xc:self.hdr.length]

    def describe_image(self):
        if hasattr(self, "shdrs"):
            print "segmented image in %d parts" % len(self.shdrs)
            for i in range(len(self.shdrs)):
                h = self.shdrs[i]

                print " segment %d: version %08x, base_addr: %08x, length %08x" % (i, h.version, h.base_addr, h.length)

        else:
            print "unitary image, version %08x, base_addr: %08x, length: %08x" % (self.hdr.version, self.hdr.base_addr, self.hdr.length)


