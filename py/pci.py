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

import os
import ctypes

class PCI_PCIe_cap(object):
    def __init__(self, cfg, offset):
        self.cfg = cfg
        self.offset = offset
        self._read_pcie_capabilities_register()
        if self.device_type:
            raise Exception("not a PCI Express Endpoint device")
        self._read_device_capabilities_register()

    def _read_pcie_capabilities_register(self):
        tmp = self.cfg.read(self.offset)
        self.version = (tmp >> 16) & 0xffff
        self.device_type = (tmp >> 20) & 0xf
        self.slot_implemented = (tmp >> 24) & 0x1
        self.int_msg_num = (tmp >> 25) & 0x1f
        self.rsvdp = tmp >> 30

    def _read_device_capabilities_register(self):
        tmp = self.cfg.read(self.offset + 4)
        self.max_payload_size = tmp & 0x7
        self.phantom_functions = (tmp >> 3) & 0x3
        self.extended_tag_field_supported = (tmp >> 5) & 0x1
        # etc...

    def set_relaxed_ordering(self, val = 0, verbose = 1):
        tmp = self.cfg.read(self.offset + 8)
        ns = (tmp >> 4) & 1
        val = 1 if val > 0 else 0
        if ns != val:
            if verbose:
                print "[+] %s no snoop bit" % ("setting" if val == 1 else "clearing")
            tmp &= (~0x10 | val << 4)
            self.cfg.write(self.offset + 8, tmp)
        elif verbose > 1:
            print "[-] not touching no snoop bit"

    def set_no_snoop(self, val = 0, verbose = 1):
        r = self.cfg.read(self.offset + 8)
        tgt = (r & ~0x800) | (0x800 if val > 0 else 0)
        if r != tgt:
            if verbose:
                print "[+] %s relaxed ordering" % ("enabling" if val > 0 else "disabling")
            self.cfg.write(self.offset + 8, tgt)
        elif verbose > 1:
            print "[-] not touching relaxed ordering bit"


class PCI_MSIX_cap(object):
    def __init__(self, cfg, offset):
        self.cfg = cfg
        self.offset = offset

    def _get_cap_enabled(self):
        tmp = self.cfg.read(self.offset)
        return 0 != (tmp & 0x80000000)

    def _set_cap_enabled(self, val):
        tmp = self.cfg.read(self.offset)
        if val == 0:
            self.cfg.write(self.offset, tmp & ~0x80000000)
        else:
            self.cfg.write(self.offset, tmp | 0x80000000)

    enabled = property(_get_cap_enabled, _set_cap_enabled)

    def _get_tbl_sz(self):
        tmp = self.cfg.read(self.offset)
        return tmp & 0x3ff

    table_size = property(_get_tbl_sz, None)

    def _get_tbl_ofs(self):
        tmp = self.cfg.read(self.offset + 4)
        return tmp & 0xfffffffc

    table_offset = property(_get_tbl_ofs, None)

    def _get_tbl_bir(self):
        tmp = self.cfg.read(self.offset + 4)
        return tmp & 0x3

    table_bir = property(_get_tbl_bir, None)

    def _get_pba_ofs(self):
        tmp = self.cfg.read(self.offset + 8)
        return tmp & 0xfffffffc

    pba_offset = property(_get_pba_ofs, None)

    def _get_pba_bir(self):
        tmp = self.cfg.read(self.offset + 8)
        return tmp & 3

    pba_bir = property(_get_pba_bir, None)

cap_types = {
    0x01: ("Power Management version 3", None),
    0x03: ("VPD", None),
    0x05: ("MSI", None),
    0x11: ("MSI-X", PCI_MSIX_cap, "msix"),
    0x10: ("PCI Express Capabilities List Register", PCI_PCIe_cap, "pcie"),
}

ext_cap_types = {
    0x001: ("Advanced Error Reporting", None),
    0x002: ("Virtual Channel", None),
    0x003: ("Device Serial Number", None),
    0x004: ("Power Budgeting <?>", None),
    0x018: ("Latency Tolerance Reporting", None),
}

class Config(object):
    def __init__(self, interface):
        self.read = interface.cfg_read
        self.write = interface.cfg_write
        self.caps = {}
        try:
            self.enumerate_capabilities()
        except:
            print "[!] failed to enumerate device capabilities"

    def enumerate_capabilities(self, verbose=1):
        print "[+] enumerating device capabilities"
        cap_ptr = self.read(0x34)
        while cap_ptr != 0:
            cap_hdr = self.read(cap_ptr)
            t = cap_hdr & 0xff
            if t in cap_types:
                if verbose:
                    print " * capability at %02x: %s (%02x)" % (cap_ptr, cap_types[t][0], t)
                if cap_types[t][1] != None:
                    self.caps[cap_types[t][2]] = cap_types[t][1](self, cap_ptr)
            else:
                if verbose:
                    print " * capability at %02x: Unknown (%02x)" % (cap_ptr, t)
            cap_ptr = (cap_hdr >> 8) & 0xff

        ext_cap_ptr = 0x100
        while ext_cap_ptr:
            ext_cap = self.read(ext_cap_ptr)
            cap_id = ext_cap & 0xffff
            cap_ver = (ext_cap >> 16) & 0xf
            if cap_id in ext_cap_types:
                if verbose:
                    print " * extended capability at %03x: %s (%04x), version %01x" % (ext_cap_ptr, ext_cap_types[cap_id][0], cap_id, cap_ver)
            else:
                if verbose:
                    print " * extended capability at %03x: Unknown (%04x), version %01x" % (ext_cap_ptr, cap_id, cap_ver)
            ext_cap_ptr = ext_cap >> 20

def check_config(dev):
    line = ""
    bar = ctypes.cast(dev.bar0, ctypes.POINTER(ctypes.c_uint32 * 0x400)).contents

    for i in range(0, 0x400):
        cval = dev.config.read(i * 4) 
        bval = bar[i]

        if cval == bval:
            if cval == 0:
                line += " "
            else:
                line += "."
        else:
            line += "!"

        if len(line) == 80:
            print line
            line = ""

