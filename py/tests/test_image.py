'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2026  Saul St. John

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

# Tests for the in-memory image formatting on the flash path - efirom's PCI
# option-ROM builder and fw's firmware-image parser. These exercise the
# bytes/str handling that the Python 2 -> 3 port had to get right.

import io
import struct
import unittest

import efirom
import fw


class TestBuildEfiRom(unittest.TestCase):
    def test_rom_structure_and_checksum(self):
        pe = b'MZ' + b'\x00' * 510  # a 512-byte stand-in PE image
        rom = efirom.build_efi_rom(pe, vid=0x14e4, did=0x1682)

        self.assertIsInstance(rom, bytes)
        # PCI expansion-ROM signature 0xAA55, little-endian
        self.assertEqual(rom[0], 0x55)
        self.assertEqual(rom[1], 0xAA)
        # ROM size is padded to a 512-byte multiple
        self.assertEqual(len(rom) % 512, 0)
        # the option-ROM checksum makes every byte sum to 0 mod 256
        self.assertEqual(sum(rom) % 256, 0)


class TestFirmwareImage(unittest.TestCase):
    def test_unitary_image(self):
        body = b'\xde\xad\xbe\xef' * 8
        length = 0xc + len(body)
        # FirmwareHeader is big-endian: version, base_addr, length
        header = struct.pack('>III', 1, 0x08000000, length)
        image = fw.FirmwareImage(io.BytesIO(header + body))

        self.assertEqual(image.hdr.version, 1)
        self.assertEqual(image.hdr.base_addr, 0x08000000)
        self.assertEqual(image.hdr.length, length)
        self.assertEqual(image.img, body)


if __name__ == '__main__':
    unittest.main()
