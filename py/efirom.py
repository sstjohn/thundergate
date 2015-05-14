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

from ctypes import *
import argparse

class PCI_DATA_STRUCTURE(Structure):
    _pack_ = 1
    _fields_ = [
        ('Signature', c_uint32),
        ('VendorId', c_uint16),
        ('DeviceId', c_uint16),
        ('Reserved0', c_uint16),
        ('Length', c_uint16),
        ('Revision', c_uint8),
        ('ClassCode', c_uint8 * 3),
        ('ImageLength', c_uint16),
        ('CodeRevision', c_uint16),
        ('CodeType', c_uint8),
        ('Indicator', c_uint8),
        ('Reserved1', c_uint16),
    ]

class EFI_PCI_EXPANSION_ROM_HEADER(Structure):
    _pack_ = 1
    _fields_ = [
        ('Signature', c_uint16),
        ('InitializationSize', c_uint16),
        ('EfiSignature', c_uint32),
        ('EfiSubsystem', c_uint16),
        ('EfiMachineType', c_uint16),
        ('CompressionType', c_uint16),
        ('Reserved', c_uint8 * 8),
        ('EfiImageHeaderOffset', c_uint16),
        ('PcirOffset', c_uint16),
    ]


def build_efi_rom(pe_img, vid, did, compress = 0):
    if compress > 0:
        import EfiCompressor
        pe_img = EfiCompressor.UefiCompress(pe_img, len(pe_img))[:]

    hdr_size = sizeof(EFI_PCI_EXPANSION_ROM_HEADER) 

    pad1_size = 4 - (hdr_size % 4)

    hdr_size += pad1_size
    hdr_size += sizeof(PCI_DATA_STRUCTURE)
    hdr_size += sizeof(c_uint8)

    pad2_size = 0x8 - (hdr_size & 0x7)

    hdr_size += pad2_size
    
    rom_size = hdr_size + len(pe_img)
    rom_size = (rom_size + 0x1ff) & ~0x1ff

    class RomImage(Structure):
        _pack_ = 4
        _fields_ = [("rom", EFI_PCI_EXPANSION_ROM_HEADER),
                    ("_pad1", c_uint8 * pad1_size),
                    ("pci", PCI_DATA_STRUCTURE),
                    ("cksum", c_uint8),
                    ("_pad2", c_uint8 * pad2_size),
                    ("pe", c_uint8 * (rom_size - hdr_size))]

    buf = create_string_buffer(sizeof(RomImage))
    image = cast(buf, POINTER(RomImage))[0]
    
    memmove(byref(image.pe), pe_img, len(pe_img))

    image.rom.Signature = 43605
    image.rom.InitializationSize = (rom_size >> 9)
    image.rom.EfiSignature = 3825
    image.rom.EfiSubsystem = 0xb
    image.rom.EfiMachineType = 0x8664
    image.rom.CompressionType = 1 if compress > 0 else 0
    image.rom.EfiImageHeaderOffset = hdr_size
    image.rom.PcirOffset = RomImage.pci.offset

    image.pci.Signature = 1380533072
    image.pci.VendorId = vid
    image.pci.DeviceId = did
    image.pci.Length = sizeof(PCI_DATA_STRUCTURE)
    image.pci.ClassCode[0] = 2
    image.pci.ImageLength = rom_size >> 9
    image.pci.CodeType = 0x3
    image.pci.Indicator = 0x80
    
    cksum = 0

    for i in range(rom_size):
        cksum += ord(buf[i])

    image.cksum = -cksum

    return buf.raw 

if __name__ == "__main__":
   def auto_int(x):
       return int(x, 0)
   parser = argparse.ArgumentParser()
   parser.add_argument('infile', type=argparse.FileType('rb'))
   parser.add_argument('outfile', type=argparse.FileType('wc'))
   parser.add_argument("-v", "--vendor", type=auto_int, default=0)
   parser.add_argument("-d", "--device", type=auto_int, default=0)
   parser.add_argument("-c", "--compress", action="store_true")
   args = parser.parse_args()
   o = args.outfile
   i = args.infile.read()
   o.write(build_efi_rom(i, args.vendor, args.device, compress=1 if args.compress else 0))
   o.close()
   args.infile.close()
