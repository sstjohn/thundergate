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

import tglib as tg
import struct
from ctypes import *
import os
import hashlib
import msix
from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

import rflip
from memory import Memory
from phy import Phy
from cpu import Cpu
from nvram import Nvram
from ftq import Ftq

import block_utils
import pci

tg3_blocks = [
	("pci", 0, rflip.pci),
	("hpmb", 0x200, rflip.hpmb),
	("emac", 0x400, rflip.emac),
    ("rss", 0x600, rflip.rss),
    ("stats", 0x800, rflip.mac_stats),
	("sdi", 0xc00, rflip.sdi),
    ("tcp_seg_ctrl", 0xce0, rflip.tcp_seg_ctrl),
    ("rtsdi", 0xd00, rflip.rtsdi),
	("sdc", 0x1000, rflip.sdc),
	("sbds", 0x1400, rflip.sbds),
	("sbdi", 0x1800, rflip.sbdi),
	("sbdc", 0x1c00, rflip.sbdc),
	("rlp", 0x2000, rflip.rlp),
	("rdi", 0x2400, rflip.rdi),
	("rdc", 0x2800, rflip.rdc),
	("rbdi", 0x2c00, rflip.rbdi),
	("rbdc", 0x3000, rflip.rbdc),
	("cpmu", 0x3600, rflip.cpmu),
	("hc", 0x3c00, rflip.hc),
	("ma", 0x4000, rflip.ma),
	("bufman", 0x4400, rflip.bufman),
    ("rtbufman", 0x4600, rflip.bufman),
    ("bdrdma", 0x4700, rflip.bdrdma),
	("rdma", 0x4800, rflip.rdma),
    ("nrdma", 0x4900, rflip.nrdma),
    ("rtrdma", 0x4a00, rflip.rdma),
	("wdma", 0x4c00, rflip.wdma),
	("rxcpu", 0x5000, Cpu),
	("lpmb", 0x5800, rflip.lpmb),
	("ftq", 0x5c00, Ftq),
	("msi", 0x6000, rflip.msi),
	("dmac", 0x6400, rflip.dmac),
	("grc", 0x6800, rflip.grc),
	("asf", 0x6c00, rflip.asf),
	("nvram", 0x7000, Nvram),
	("otp", 0x7500, rflip.otp),
	("pcie_alt", 0x7c00, rflip.pcie_alt),
	("pcie_tl", 0x7c00, rflip.pcie_tl),
	("pcie_dl", 0x7d00, rflip.pcie_dl),
	("pcie_pl", 0x7e00, rflip.pcie_pl),
]

tg3_mem = [
    ("txrcb", tg.rcb, 0x100, 2),
    ("rxrcb", tg.rcb, 0x200, 4),
    ("gencomm", tg.gencomm, 0xb50, 1),
    ("txbd", tg.sbd, 0x4000, 0x200),
    ("rxbd", tg.rbd, 0x6000, 0x100),
    ("txmbuf0", tg.mbuf, 0x8000, (22 * 1024) / sizeof(tg.mbuf)),
    ("txmbuf1", tg.mbuf, 0xd800, (8 * 1024) / sizeof(tg.mbuf)),
    ("rxmbuf", tg.mbuf, 0x10000, (40 * 1024) / sizeof(tg.mbuf))
]

class Device(object):
    def __init__(self, interface):
        self.interface = interface
        self.blocks = []
        self.mem = None

    def __enter__(self):
        self.interface.__enter__()
        self.config = pci.Config(self.interface)

        self.bar0 = self.interface.bar0
        try: self.bar2 = self.interface.bar2
        except: pass
        
        if 'msix' in self.config.caps:
            sz = self.config.caps['msix'].table_size

            tbar = self.config.caps['msix'].table_bir
            tofs = self.config.caps['msix'].table_offset
            try:
                bar = getattr(self, "bar%d" % tbar)
                self.msix_tbl = msix.Table(bar, tofs, sz)
            except: pass            
            pbar = self.config.caps['msix'].pba_bir
            pofs = self.config.caps['msix'].pba_offset
            try:
                bar = getattr(self, "bar%d" % pbar)
                self.msix_pba = msix.Pba(bar, pofs, sz)
            except: pass

        self.map_registers()
        self.map_memory()
        self.phy = Phy(self, 1)

        return self

    def __exit__(self, t, v, traceback):
        self.interface.__exit__(t, v, traceback)

    def close(self):            
        for i in ["rbdi", "rlp", "rdi", "rdc", "rbdc", "sbds", "sbdi", "sdi", "rdma", "sdc", "sbdc", "hc", "wdma"]:
            try:
                block = getattr(self, i)
                block.disable()
            except:
                pass
        
        try: self.ftq.reset()
        except: pass

        try: self.reset()
        except: pass

        if hasattr(self, "pci"):
            if self.pci.command.bus_master:
                print "[+] disabling bus mastering"
                self.pci.command.bus_master = 0
            if self.pci.command.memory_space:
                print "[+] disabling memory space decode"
                self.pci.command.memory_space = 0

    def block_at(self, name, offset, t):
        t.block_dump = block_utils.dump
        t.block_disp = block_utils.disp
        t.block_name = name
        
        if t.__name__ == "ftq":
                t.reset = block_utils.ftq_reset

        for f in t._fields_:
            if f[0] == "mode":
                mt = f[1]
                if hasattr(mt, "enable"):
                    if not hasattr(t, "enable"):
                        t.block_enable = block_utils.enable
                    if not hasattr(t, "disable"):
                        t.block_disable = block_utils.disable
                if hasattr(mt, "reset"):
                    if not hasattr(t, "reset"):
                        t.reset = block_utils.reset

        x = cast(self.bar0 + offset, POINTER(t)).contents
        x.offset = offset
        x._block_regs = cast(self.bar0 + offset, POINTER(c_uint32 * (sizeof(t) / 4))).contents 
        x._dev = self
        return x

    def init_memory_space_decode(self):
        tmp = self.config.read(0x4)
        if not tmp & 0x2:
            print "[+] enabling for memory space decode"

            tmp |= 0x2
            self.config.write(0x4, tmp)

        self.pci.state.rom_enable = 1
        self.pci.state.rom_retry_enable = 1

    def init_bus_master(self):
        if self.pci.command.bus_master:
            return

        print "[+] enabling for bus mastering"
        self.pci.command.bus_master = 1

    def mask_interrupts(self):		
        if self.pci.misc_host_ctrl.mask_interrupt:
            return
        print "[+] masking interrupts"
        self.pci.misc_host_ctrl.mask_interrupt = 1

    def unmask_interrupts(self):		
        if self.pci.misc_host_ctrl.mask_interrupt != 0:
            print "[+] unmasking interrupts"
            self.pci.misc_host_ctrl.mask_interrupt = 0

    def map_registers(self):
        self.reg = cast(self.bar0, POINTER(c_uint32 * (0x8000 / 4))).contents

        for (name, offset, t) in tg3_blocks:
            setattr(self, name, self.block_at(name, offset, t))
            self.blocks += [getattr(self, name)]

    def map_memory(self):
        print "[+] mapping device memory window"
        self.mem = Memory(self)
        for i in tg3_mem:
            self.mem.map_struct(*i)

    def reg_dump(self):
        for i in range(len(self.reg)):
            a = i * 4
            if 0 == (a % 0x10):
                print
                print "0x%04x: " % a,
            print "%08x" % self.reg[i],

    def reg_save(self):
        buf = (c_uint32 * len(self.reg))()
        for i in range(len(self.reg)):
            buf[i] = self.reg[i]
        return buf

    
    
    def reset(self):
        magic = self.mem.read_dword(0xb50)	
        if magic == 0x4b657654:
            print "[.] found magic number at offset 0xb50"
        else:
            print "[+] found %08x at offset 0xb50, writing 0x4b657654" % magic
            self.mem.write_dword(0xb50, 0x4b657654)

        self.nvram.acquire_lock()

        print "[+] clearing fast boot program counter register, was", 
        pfbreg = cast(self.bar0 + 0x6894, POINTER(c_uint32))
        print "0x%08x" % pfbreg[0]
        pfbreg[0] = 0

        if self.grc.misc_config.disable_grc_reset_on_pcie_block == 0:
            print "[+] disabling grc reset on pcie block"
            self.grc.misc_config.disable_grc_reset_on_pcie_block = 1

        #if self.grc.misc_config.gphy_keep_power_during_reset == 0:
        #    print "[+] enabling gphy power during reset"
        #    self.grc.misc_config.gphy_keep_power_during_reset = 1

        print "[+] resetting core clocks"
        self.grc.misc_config.grc_reset = 1

        usleep(1000)

        self.init()	
        
        print "[+] polling for bootcode completion...",
        cntr = 0
        while self.mem.read_dword(0xb50) == 0x4b657654:
            cntr += 1
            if cntr > 5000:
                raise Exception("timed out waiting for bootcode completion")
            usleep(1000)
        if cntr == 0:
            print "complete."
        else:
            print "completed after %d.%d ms." % (cntr / 10, cntr % 10)

    def init_pci_host_ctrl(self):
        if self.pci.misc_host_ctrl.enable_pci_state_register_rw_cap == 0:
            print "[+] enabling pci state register rw capability"
            self.pci.misc_host_ctrl.enable_pci_state_register_rw_cap = 1

        if self.pci.misc_host_ctrl.enable_indirect_access == 0:
            print "[+] enabling indirect access"
            self.pci.misc_host_ctrl.enable_indirect_access = 1

        if self.pci.misc_host_ctrl.enable_endian_word_swap == 0:
            print "[+] enabling endian word swap"
            self.pci.misc_host_ctrl.enable_endian_word_swap = 1


    def init_grc(self):
        if self.grc.mode.byte_swap_bd:
            print "[-] disabling nonframe data byte swap"
            self.grc.mode.byte_swap_bd = 0
        if not self.grc.mode.word_swap_bd:
            print "[+] enabling nonframe data word swap"
            self.grc.mode.word_swap_bd = 1
        if not self.grc.mode.byte_swap_data:
            print "[+] enabling frame data byte swap"
            self.grc.mode.byte_swap_data = 1
        if not self.grc.mode.word_swap_data:
            print "[+] enabling frame data word swap"
            self.grc.mode.word_swap_data = 1

    def init_eratta(self):
        self.cpmu.padring_control.pcie_serdes_lfck_rx_select_cnt0 = 1
        self.grc.mode.pcie_pl_sel = 0
        self.grc.mode.hi_1k_en = 0
        self.grc.mode.pcie_dl_sel = 1
        self.pcie_alt.dll.ftsmax.val = 0x2c
        self.grc.mode.pcie_dl_sel = 0
        self.cpmu.no_link_or_10mb_policy.mac_clock_switch = 0x13

    def init(self):
        self.init_memory_space_decode()
        self.init_eratta()
        self.mask_interrupts()
        self.init_bus_master()
        self.ma.block_enable()
        self.init_pci_host_ctrl()
        self.init_grc()

    def fwed(self):
        oldhash = hashfile("fw/app.c")
        res = os.system("vim fw/app.c")
        if 0 == res:
            newhash = hashfile("fw/app.c")
            if oldhash != newhash:
                print "[+] building new firmware"
                res = os.system("make -C fw")
                if 0 == res:
                    print "[+] firmware compilation successful"
                    self.nvram.init(wr=1)
                    self.nvram.load_rxcpu_fw("fw/fw.img")
                    self.reset()
                else:
                    print "[-] firmware compilation failed!"

def hashfile(path):
    with open(path, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()
