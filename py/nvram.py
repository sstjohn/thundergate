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

import struct
import rflip
import block_utils
import sys
import tglib as tg
import zlib
from ctypes import *
from efirom import build_efi_rom
from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

class Nvram(rflip.nvram):
    def __init__(self):
        super(Nvram, self).__init__()
        self._locked = 0

    def init(self, wr=0, lh=1):
        self.acquire_lock()
        self.access_enable()
        self.reset()

        self.acquire_lock()
        self.access_enable()
        self.eeprom_len = self.__get_eeprom_len()

        if wr: self.write_enable()
        if lh: self.load_eeprom_header()

    def reset(self):
        self.acquire_lock()
        self.access_enable()

        print "[+] resetting nvram state machine"
        self.command.reset = 1

        cntr = 0
        while self.command.reset:
            cntr += 1
            if cntr > 1000:
                raise Exception("timed out waiting for nvram block to reset")

            usleep(10)

        self._locked = 0



    def acquire_lock(self):
        if self.sw_arb.req1:
            self._locked = 1
            return

        self._locked = 0
        cntr = 0
        print "[+] requesting nvram lock... ",
        self.sw_arb.req_set1 = 1
        while not self.sw_arb.arb_won1:
            cntr += 1
            if cntr > 20:
                raise Exception("timed out waiting for nvram arbitration")
            usleep(10)
        if cntr == 0:
            print "granted."
        else:
            print "granted after %d us." % (cntr * 10)

        self._locked = 1

    def access_enable(self):
        if not self._dev.grc.misc_local_control.auto_seeprom:
            print "[+] enabling auto seeprom in grc misc local control"
            self._dev.grc.misc_local_control.auto_seeprom = 1

        if not self.access.enable:
            print "[+] enabling nvram access"
            self.access.enable = 1

    def access_disable(self):
        if self.access.enable:
            print "[+] disabling nvram access"
            self.access.enable = 0

    def write_enable(self):
        if not self._dev.grc.mode.nvram_write_enable:
            print "[+] enabling nvram write in grc block"
            self._dev.grc.mode.nvram_write_enable = 1

        if not self.access.write_enable:
            print "[+] enabling nvram write access"
            self.access.write_enable = 1

    def write_disable(self):
        if self.access.write_enable:
            print "[+] disabling nvram write access"
            self.access.write_enable = 0

    def read_dword(self, offset):
        if not self.access.enable:
            raise Exception("enable nvram access first")

        if not self._locked:
            raise Exception("lock nvram before use")

        self.data_address = offset
        
        if self.command.done:
            self.command.done = 1
            cntr = 0
            while self.command.done:
                cntr += 1
                if cntr > 100:
                    raise Exception("timed out waiting for nvram command done bit to clear")
                usleep(10)
        
        self.command.erase = 0
        self.command.wr = 0
        self.command.first = 1
        self.command.last = 1
        self.command.doit = 1

        cntr = 0
        while not self.command.done:
            cntr += 1
            if cntr > 100:
                raise Exception("timed out waiting for nvram command to complete")

            usleep(10)

        return self.read_data

    def __get_eeprom_len(self): 
        if not self.read_dword(0) == tg.TG3_MAGIC:
            raise Exception("unknown eeprom format")
 
        return ((self.read_dword(0xf0) & 0xffff) >> 8) * 1024

    def load_eeprom_header(self):
        hdr_len = sizeof(tg.nvram_header)
        if tg.TG3_MAGIC != self.read_dword(0):
            raise Exception("unknown nvram format")

        self._eeprom_hdr_buf = create_string_buffer(sizeof(tg.nvram_header))
        eeprom_words = cast(self._eeprom_hdr_buf, POINTER(c_uint32))
        for i in range(0, len(self._eeprom_hdr_buf), 4):
            eeprom_words[i >> 2] = self.read_dword(i)
        self.eeprom_hdr = cast(self._eeprom_hdr_buf, POINTER(tg.nvram_header))[0]

    def write_dword(self, offset, data, first=1, last=1):
        if self.write1.enable_command != 0x6:
            raise Exception("enable_command is 0x%02x, should be 0x06\n" % self.write1.enable_command)

        if self.write1.disable_command != 0x4:
            raise Exception("disable_command is 0x%02x, should be 0x06\n" % self.write1.disable_command)

        if not self._dev.grc.mode.nvram_write_enable:
            raise Exception("nvram write not enabled in grc block")

        if not self.access.enable:
            raise Exception("enable nvram access first")

        if not self.access.write_enable:
            raise Exception("nvram write not enabled in nvram block")

        if not self._locked:
            raise Exception("lock nvram before use")

        
        if self.command.done:
            self.command.done = 1
            cntr = 0
            while self.command.done:
                cntr += 1
                if cntr > 100:
                    raise Exception("timed out waiting for nvram command done bit to clear")
                usleep(10)

        self.data_address = offset
        self.write_data = data

        self.command.erase = 0
        self.command.wr = 1
        self.command.first = first
        self.command.last = last
        self.command.doit = 1

        cntr = 0
        while not self.command.done:
            cntr += 1
            if cntr > 1000:
                raise Exception("timed out waiting for nvram command to complete")

            usleep(10)
        self.command.dome = 1

    def write_block(self, offset, data):
        assert len(data) >= 4 and 0 == (len(data) % 4)

        print "[+] writing block length %x at offset %x..." % (len(data), offset),
        sys.stdout.flush()

        for i in range(0, len(data), 4):
            if 0 == (i % 0x400):
                sys.stdout.write(".")
                sys.stdout.flush()
            self.write_dword(offset + i, struct.unpack("!I", data[i:i+4])[0])
        print

    def read_block(self, offset, length):
        assert length >=4 and 0 == (length % 4)

        ret = ""
        for i in range(0, length, 4):
            ret += struct.pack("!I", self.read_dword(offset + i))

        return ret

    def show_directory(self):
        for index in range(len(self.eeprom_hdr.directory)):
            dentry = self.eeprom_hdr.directory[index]
            nv_ofs = dentry.nvram_start
            sram_ofs = dentry.sram_start
            nv_len = (dentry.typelen & 0x3fffff) << 2
            nv_type = dentry.typelen >> 24
            nv_xa = 0 != (dentry.typelen & 0x00800000)
            nv_xb = 0 != (dentry.typelen & 0x00400000)

            if nv_ofs > 0:
                d = (index, nv_type, nv_ofs, sram_ofs, nv_len)
                print "nvram image #%d. attrs: type %02x, nv_ofs %x, sram_ofs: %x, len %x," % d,
                if nv_xa:
                    print "xa",
                if nv_xb:
                    print "xb",
                if not nv_xa and not nv_xb:
                    print "nx",
                print


    def get_dir_image(self, index):
        dentry = self.eeprom_hdr.directory[index]
        nv_ofs = dentry.nvram_start
        nv_len = (dentry.typelen & 0x3fffff) << 2
        nv_type = dentry.typelen >> 24
        nv_xa = 0 != (dentry.typelen & 0x00800000)
        nv_xb = 0 != (dentry.typelen & 0x00400000)

        return self.read_block(nv_ofs, nv_len)

    def dump_dir_image(self, index, fname):
        f = open(fname, "wb")
        f.write(self.get_dir_image(index))
        f.close()

    def _set_dir_entry(self, index, nv_ofs, ilen, itype=0, sram_ofs=0x10000, xa=False, xb=False):

        if nv_ofs + ilen > self.eeprom_len:
            raise Exception("image too big for eeprom")

        dentry = self.eeprom_hdr.directory[index]
        dentry.nvram_start = nv_ofs
        dentry.sram_start = sram_ofs
        
        tl = (ilen >> 2) | (itype << 24)
        if xa:
            tl |= 0x00800000
        if xb:
            tl |= 0x00400000
        dentry.typelen = tl

        offsetof = lambda x: addressof(x) - addressof(self.eeprom_hdr)
        
        update_start = offsetof(dentry)
        update_len = sizeof(dentry)
        self._flush_eeprom_header(update_start, update_len)

        directory_start = offsetof(self.eeprom_hdr.directory)
        directory_size = len(self.eeprom_hdr.directory) * sizeof(tg.nvram_dir_item)
        s = 0
        for i in range(directory_start, directory_start + directory_size):
            s += ord(self._eeprom_hdr_buf[i]) % 0x100

        self.eeprom_hdr.mfg.dir_cksum = 0x100 - s

        update_start = offsetof(self.eeprom_hdr.mfg)
        update_start += self.eeprom_hdr.mfg.__class__.dir_cksum.offset
        update_len = self.eeprom_hdr.mfg.__class__.dir_cksum.size
        self._flush_eeprom_header(update_start, update_len)
        self._update_mfg_crc()

    def _flush_eeprom_header(self, ofs, size):
        if 0 != (ofs % 4):
            d = ofs & 3
            size += d
            ofs &= ~3

        if 0 != (size % 4):
            size = (size + 3) & ~3

        for i in range(0, size, 4):
            data = struct.unpack("I", self._eeprom_hdr_buf[ofs+i:ofs+i+4])[0]
            self.write_dword(ofs + i, data)

    def write_dir_image(self, index, data, itype = 0, sram_ofs = 0x10000, xa = False, xb = False, nv_ofs = None):
        data += struct.pack("i", zlib.crc32(data))

        if nv_ofs == None:
            nv_ofs = self.eeprom_hdr.directory[index].nvram_start
        if nv_ofs < sizeof(self.eeprom_hdr) or nv_ofs > self.eeprom_len:
            raise Exception("bogus nvram start offset for directory entry 0")
        nv_len = len(data)

        self._set_dir_entry(index, nv_ofs, nv_len, itype, sram_ofs, xa, xb)
        self.write_block(nv_ofs, data)
        return nv_len

    def load_image(self, fname, itype = 0, sram_ofs = 0x10000, xa = False, xb = False):
        data = ''
        with open(fname, "rb") as f:
            data = f.read()

        if len(data) == 0:
            raise Exception("no data to write")

        self.write_dir_image(0, data, itype, sram_ofs, xa, xb)

    def load_efi_drv(self, fname, compress=0):
        data = ''
        with open(fname, "rb") as f:
            data = f.read()

        if len(data) == 0:
            raise Exception("failed to load driver image")

        oprom = build_efi_rom(data, self._dev.pci.vid, self._dev.pci.did, compress=compress)
        self.write_dir_image(0, oprom)

        if not self.getpxe():
            self.setpxe()

    def load_rxcpu_fw(self, fname):
        data = ''
        with open(fname, "rb") as f:
            data = f.read()

        if len(data) == 0:
            raise Exception("failed to load firmware image")

        self.write_dir_image(1, data, 1, 0x08008000, True)
        
        if not self.getasf():
            self.setasf()

    def install_thundergate(self, efidrv="efi/dmarf.efi", cpufw="fw/fw.img"):
        start = self.eeprom_hdr.directory[0].nvram_start
        
        data = ''
        with open(efidrv, "rb") as f:
            data = f.read()
        oprom = build_efi_rom(data, self._dev.pci.vid, self._dev.pci.did, compress=1)
        print "[+] installing thundergate oprom"
        start += self.write_dir_image(0, oprom, nv_ofs=start)
        
        with open(cpufw, "rb") as f:
            data = f.read()
        print "[+] installing thundergate rxcpu firmware"
        self.write_dir_image(1, data, 1, 0x08008000, True, nv_ofs=start)

        if not self.getpxe():
            self.setpxe()
        if not self.getasf():
            self.setasf()
    
    def dump_eeprom(self, fname):
        with open(fname, "wb") as f:
            f.write(self.read_block(0, self.eeprom_len))

    def write_eeprom(self, fname):
        data = ''
        with open(fname, "rb") as f:
            data = f.read()

        if len(data) == 0 or len(data) < self.eeprom_len:
            raise Exception("bad image length")

        self.write_block(0, data)

    def getasf(self):
        return tg.TG3_FEAT_ASF == (self.eeprom_hdr.mfg.feat_cfg & tg.TG3_FEAT_ASF)

    def getpxe(self):
        return tg.TG3_FEAT_PXE == (self.eeprom_hdr.mfg.feat_cfg & tg.TG3_FEAT_PXE)

    def _flush_mfg_feat_cfg(self):
        update_ofs = addressof(self.eeprom_hdr.mfg) - addressof(self.eeprom_hdr)
        update_ofs += self.eeprom_hdr.mfg.__class__.feat_cfg.offset
        update_len = self.eeprom_hdr.mfg.__class__.feat_cfg.size

        self._flush_eeprom_header(update_ofs, update_len)
        self._update_mfg_crc()

    def _update_mfg_crc(self):
        mfg_start = addressof(self.eeprom_hdr.mfg) - addressof(self.eeprom_hdr)
        mfg_len = sizeof(self.eeprom_hdr.mfg)

        data = self._eeprom_hdr_buf[mfg_start:mfg_start + mfg_len - 4]
        rdata = ''.join([data[i:i+4][::-1] for i in range(0, len(data), 4)])
        
        crc = struct.unpack("I", struct.pack("!i", zlib.crc32(rdata)))[0]
        self.eeprom_hdr.mfg.crc = crc

        update_ofs = mfg_start + self.eeprom_hdr.mfg.__class__.crc.offset
        update_len = self.eeprom_hdr.mfg.__class__.crc.size
        self._flush_eeprom_header(update_ofs, update_len)

    def setasf(self, disable=0):
        if disable:
            if not self.eeprom_hdr.mfg.feat_cfg & tg.TG3_FEAT_ASF:
                raise Exception("asf not enabled")

            print "[+] disabling asf in mfg feat cfg"

            self.eeprom_hdr.mfg.feat_cfg &= ~tg.TG3_FEAT_ASF
        
        else:
            if self.eeprom_hdr.mfg.feat_cfg & tg.TG3_FEAT_ASF:
                raise Exception("asf already enabled")
            
            print "[+] enabling asf in mfg feat cfg"
            self.eeprom_hdr.mfg.feat_cfg |= tg.TG3_FEAT_ASF

        self._flush_mfg_feat_cfg()

    def setpxe(self, disable=0):
        if disable:
            if not self.eeprom_hdr.mfg.feat_cfg & tg.TG3_FEAT_PXE:
                raise Exception("asf not enabled")
            
            print "[+] disabling pxe in mfg feat cfg"
            self.eeprom_hdr.mfg.feat_cfg &= ~tg.TG3_FEAT_PXE
        
        else:
            if self.eeprom_hdr.mfg.feat_cfg & tg.TG3_FEAT_PXE:
                raise Exception("asf already enabled")
            
            print "[+] enabling pxe in mfg feat cfg"
            self.eeprom_hdr.mfg.feat_cfg |= tg.TG3_FEAT_PXE

        self._flush_mfg_feat_cfg()
