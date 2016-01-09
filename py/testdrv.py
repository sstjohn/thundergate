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
from ctypes import *
import random
import tglib as tg
import reutils
from ctypes import cast, POINTER, sizeof, c_char
import csv
import os
from time import sleep
usleep = lambda x: sleep(x / 1000000.0)
import socket
from struct import pack, unpack
from tapdrv import TapDriver

class TestDriver(object):
    def __init__(self, dev):
        self.dev = dev

    def __enter__(self):
        return self

    def __exit__(self, t, v, traceback):
        pass

    def run(self):
        self.dev.init()
        self.clear_txmbufs()
        self.clear_txbds()

        self.tap = TapDriver(self.dev)
        self.tap.__enter__()
        self.tap._link_detect()
        self.test_send(self.tap)
        #self.gate_send()
        #self.test_dmar()
        #self.test_rdmar()
        #self.test_dmaw()
        #self.reg_finder()
        #self.msi_wr()
        #self.asfdiff()
        #self.pxediff()
        #self.pxeidiff()
        #self.read_oprom()

    def gate_send(self):
        dev = self.dev

        print "[+] constructing buffer:",
        buf_vaddr = dev.interface.mm.alloc(1024)
        buf = cast(buf_vaddr, POINTER(c_char))
        for b in range(0, 1024, 4):
            buf[b] = '\xde'
            buf[b+1] = '\xad'
            buf[b+2] = '\xbe'
            buf[b+3] = '\xef'
        buf_paddr = dev.interface.mm.get_paddr(buf_vaddr)
        print "vaddr %x, paddr %x" % (buf_vaddr, buf_paddr)

        print "[+] resetting device"
        dev.mem.write_dword(0xe00, 0)
	self.clear_txmbufs()
	self.clear_txbds()
        dev.reset()

        if dev.mem.gencomm.dword[0xac] >> 16 != 0x88b5:
            raise Exception("thundergate firmware does not appear to be runing.")

        print "[+] posting command to local thundergate command window"
        dev.mem.write_dword(0xe04, buf_paddr >> 32)
        dev.mem.write_dword(0xe08, buf_paddr & 0xffffffff)
        dev.mem.write_dword(0xe0c, 0x400)
        dev.mem.write_dword(0xe00, 0x88b5000e)

        print "[+] saving state"
        initial = reutils.state_save(dev)

        print "[+] setting sw event 0"
        dev.grc.rxcpu_event.sw_event_0 = 1

        cntr = 0
        while (dev.grc.rxcpu_event.sw_event_0):
            cntr += 1
            if cntr > 100:
                print "[!] timed out waiting for command completion"
                break
            usleep(100)

        if cntr <= 100:
            print "[+] command completed after usleeping for %d" % (cntr * 100)

        if dev.mem.gencomm.dword[0xac] != 0x88b5000e:
            print "[!] unexpected response: %08x" % dev.mem.gencomm.dword[0xac]

        intermediate = reutils.state_diff(dev, initial)

        for b in range(0, 1024, 4):
            buf[b] = '\xba'
            buf[b+1] = '\xad'
            buf[b+2] = '\xd0'
            buf[b+3] = '\x0d'

        print "[+] setting sw event 0 again"
        dev.grc.rxcpu_event.sw_event_0 = 1

        cntr = 0
        while (dev.grc.rxcpu_event.sw_event_0):
            cntr += 1
            if cntr > 100:
                print "[!] timed out waiting for command completion"
                break
            usleep(100)

        if cntr <= 100:
            print "[+] command completed after usleeping for %d" % (cntr * 100)

        if dev.mem.gencomm.dword[0xac] != 0x88b5000e:
            print "[!] unexpected response: %08x" % dev.mem.gencomm.dword[0xac]

        inter2 = reutils.state_diff(dev, intermediate)
    
        print "[+] constructing new buffer:",
        buf_vaddr = dev.interface.mm.alloc(1024)
        buf = cast(buf_vaddr, POINTER(c_char))
        for b in range(0, 1024, 4):
            buf[b] = '\xab'
            buf[b+1] = '\xcd'
            buf[b+2] = '\xdc'
            buf[b+3] = '\xba'
        buf_paddr = dev.interface.mm.get_paddr(buf_vaddr)
        print "vaddr %x, paddr %x" % (buf_vaddr, buf_paddr)

        dev.mem.write_dword(0xe04, buf_paddr >> 32)
        dev.mem.write_dword(0xe08, buf_paddr & 0xffffffff)

        print "[+] setting sw event 0 again"
        dev.grc.rxcpu_event.sw_event_0 = 1

        cntr = 0
        while (dev.grc.rxcpu_event.sw_event_0):
            cntr += 1
            if cntr > 100:
                print "[!] timed out waiting for command completion"
                break
            usleep(100)

        if cntr <= 100:
            print "[+] command completed after usleeping for %d" % (cntr * 100)

        if dev.mem.gencomm.dword[0xac] != 0x88b5000e:
            print "[!] unexpected response: %08x" % dev.mem.gencomm.dword[0xac]

        final = reutils.state_diff(dev, inter2)
    def pxeidiff(self):
	dev = self.dev
	cpu = dev.rxcpu

	dev.nvram.init(wr=1)
	if dev.nvram.getpxe():
		was_enabled = True
		dev.nvram.setpxe(1)
	else:
		was_enabled = False

        dev.reset(quick=True)
        cpu.mode.halt = 1
        
        nr_is = {}
        for i in range(1000000):
            try: nr_is[cpu.pc] += 1
            except: nr_is[cpu.pc] = 1
            cpu.mode.single_step = 1

        self.norom_insns = nr_is

        dev.reset()
	usleep(1000)
	dev.reset(cold = False)
	usleep(1000)

	dev.nvram.init(wr=1)
	dev.nvram.setpxe()
        dev.reset(quick=True)
        cpu.mode.halt = 1

        print
        print "[!] read rom now"
        print

        r_is = {}
        for i in range(1000000):
            try: r_is[cpu.pc] += 1
            except: r_is[cpu.pc] = 1
            cpu.mode.single_step = 1

        self.rom_insns = r_is

        uniq = []
        more = []

        for i in r_is.keys():
            try:
                diff = r_is[i] - nr_is[i]
                if diff > 0:
                    more += [(i, diff)]
            except:
                uniq += [(i, r_is[i])]

        print "[+] rom-unique insns:"
        for i in uniq:
            print "\t%08x: %d" % (i[0], i[1])

    def read_oprom(self, count = 4):
        dev = self.dev
        bdf = dev.interface.bdf
        words = []
        print "[+] reading oprom..."
        with file("/sys/bus/pci/devices/%s/rom" % bdf, "rb+") as rom:
            try:
                x = rom.read(4)
            except:
                print "[+] enabling oprom"
                rom.write("1")
                x = rom.read(4)

            words += [unpack(">I", x)[0]]

            for ofs in range(4, count, 4):
                x = rom.read(4)

                words += [unpack(">I", x)[0]]

        print "[+] last word read: %08x" % unpack(">I", x)[0]
        return words

    def pxediff(self):
	dev = self.dev
	cpu = dev.rxcpu

	dev.nvram.init(wr=1)
	if dev.nvram.getpxe():
		was_enabled = True
		dev.nvram.setpxe(1)
	else:
		was_enabled = False

	dev.reset()
	sleep(5)
	
	initial = reutils.state_save(dev)

	dev.reset()
	usleep(1000)

	dev.nvram.init(wr=1)
	dev.nvram.setpxe()
        dev.reset()

        print "[+] press any key to continue..."
        raw_input()
        dev.interface.reattach()
        dev.init()

        self.read_oprom()
	wpxe = reutils.state_diff(dev, initial)

        dev.reset(quick=True)
        cpu.mode.halt = 1
        wpxei = reutils.state_diff(dev, wpxe)

	if not was_enabled:
                dev.reset()
		dev.nvram.init(wr=1)
		dev.nvram.setpxe(1)
		dev.reset()

    def asfdiff(self):
	dev = self.dev
	cpu = dev.rxcpu

	dev.nvram.init(wr=1)
	if dev.nvram.getasf():
		was_enabled = True
		dev.nvram.setasf(1)
	else:
		was_enabled = False

	self.clear_txmbufs()
	self.clear_txbds()
	dev.reset()
	sleep(5)
	
	cpu.halt()
	initial = reutils.state_save(dev)

	dev.reset()
	usleep(1000)
	dev.reset(cold = False)
	usleep(1000)

	dev.nvram.init(wr=1)
	dev.nvram.setasf()
	self.clear_txmbufs()
	self.clear_txbds()
	
	dev.reset()
	sleep(5)
	
	cpu.halt()
	wasf = reutils.state_diff(dev, initial)

	if not was_enabled:
		dev.nvram.init(wr=1)
		dev.nvram.setasf(1)
		dev.reset()

    def clear_txmbufs(self):
        for i in range(0x8000, 0x10000, 4):
            self.dev.mem.write_dword(i, 0)

    def clear_txbds(self):
        for i in range(0x4000, 0x4800, 4):
            self.dev.mem.write_dword(i, 0)

    def block_pump(self, block):
        bn = block.block_name
        if bn.endswith("_x"):
            bn = bn[:-2]
        if bn.endswith("_regs"):
            bn = bn[:-5]
        print "[+] pumping %s" % bn
        block.block_enable(quiet = 1)
        usleep(10)
        block.block_disable(quiet = 1)

    def msi_wr(self):
        dev = self.dev
        dev.rxcpu.halt()
        dev.bufman.block_enable()
        dev.wdma.block_enable()

        test_buf_v = dev.interface.mm.alloc(8)
        cast(test_buf_v, POINTER(c_uint64))[0] = ~0
        test_buf_p = dev.interface.mm.get_paddr(test_buf_v)
        print "test buf is at %x" % test_buf_p
        print "test buf starts %s" % repr(cast(test_buf_v, POINTER(c_char * 8)).contents.raw)

        dev.pci.msi_lower_address = test_buf_p & 0xffffffff
        dev.pci.msi_upper_address = test_buf_p >> 32
        dev.pci.msi_data = 0xaaaa
        dev.msi.mode.msi_message = 0x7 
        dev.pci.msi_cap_hdr.msi_enable = 1
        dev.msi.status.msi_pci_request = 1
        usleep(1000)
        print "test buf is now %s" % repr(cast(test_buf_v, POINTER(c_char * 8)).contents.raw)

        
        for tl in (False, True):
            for pl in (False, True):
                for hi in (False, True):
                    dev.grc.mode.pcie_tl_sel = 1 if tl else 0
                    dev.grc.mode.pcie_pl_sel = 1 if pl else 0
                    dev.grc.mode.pcie_hi1k_en = 1 if hi else 0

                    for i in range(0x7c00, 0x8000, 4):
                        if 0 == i % 32:
                            print
                            print "%04x'%d%d%d: " % (i, 1 if hi else 0, 1 if pl else 0, 1 if tl else 0),
                        elif 0 == i % 16:
                            print "\t",
                        print "%08x" % dev.reg[i >> 2],

    def spy_read(self, tap):
        dev = self.dev
        dev.sbdi.block_disable()
        dev.sbdc.block_disable()
        dev.sbds.block_disable()
        dev.sdi.block_disable()
        dev.sdc.block_disable()
        dev.rxcpu.halt()

        state = reutils.state_save(dev)

        test_buf_v = dev.interface.mm.alloc(128)
        test_buf_p = dev.interface.mm.get_paddr(test_buf_v)
        print "[+] allocated test buffer at vaddr %x, paddr %x" % (test_buf_v, test_buf_p)
        for i in range(128):
            cast(test_buf_v, POINTER(c_char))[i] = '\xb4'

        dev.mem.txbd[0].addr_hi = test_buf_p >> 32
        dev.mem.txbd[0].addr_low = test_buf_p & 0xffffffff
        
        dev.mem.txbd[0].flags.l4_cksum_offload = 0
        dev.mem.txbd[0].flags.ip_cksum_offload = 0
        dev.mem.txbd[0].flags.jumbo_frame = 0
        dev.mem.txbd[0].flags.hdrlen_2 = 0
        dev.mem.txbd[0].flags.snap = 0
        dev.mem.txbd[0].flags.vlan_tag = 0
        dev.mem.txbd[0].flags.coalesce_now = 0
        dev.mem.txbd[0].flags.cpu_pre_dma = 0
        dev.mem.txbd[0].flags.cpu_post_dma = 0
        dev.mem.txbd[0].flags.hdrlen_3 = 0
        dev.mem.txbd[0].flags.hdrlen_4 = 0
        dev.mem.txbd[0].flags.hdrlen_5 = 0
        dev.mem.txbd[0].flags.hdrlen_6 = 0
        dev.mem.txbd[0].flags.hdrlen_7 = 0
        dev.mem.txbd[0].flags.no_crc = 0
        dev.mem.txbd[0].flags.packet_end = 1

        dev.mem.txbd[0].length = 64
        dev.mem.txbd[0].vlan_tag = 0
        dev.mem.txbd[0].reserved = 0

        print "[+] txbd[0] forged"
        state = reutils.state_diff(dev, state)

        dev.sbdi.ofs_48 = 0x210
        print "[+] sbdi mailbox msg delivered"
        state = reutils.state_diff(dev, state)


        self.block_pump(dev.sdi)
        state = reutils.state_diff(dev, state)

    def test_send(self, tap):
        dev = self.dev
        tap._link_detect()
        dev.rxcpu.halt()
        
        #dev.sbds.block_disable()
        #dev.sdi.block_disable()
        #dev.sdc.block_disable()
        #dev.sbds.reset()
        #dev.sdi.reset()
        #dev.sdc.reset()


        print "[+] saving initial state"
        state = reutils.state_save(dev)
        
        print "[+] submitting test packet to tap driver"
        tap.send('\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x88\xb5' + ('\xaa\x55' * 25)) #, flags=("cpu_post_dma"))
        usleep(10)
        state = reutils.state_diff(dev, state)

	    #dev.sdc.block_enable()
        #dev.sdi.block_enable()
        #dev.sbds.block_enable()
        #usleep(10)

        #state = reutils.state_diff(dev, state)

    def test_rdmar(self, init=1, reset=0):
        dev = self.dev
        dev.reset()

        print "[+] testing remote dma read"

        vaddr = dev.interface.mm.alloc(8)
        paddr = dev.interface.mm.get_paddr(vaddr)
        buf = ctypes.cast(vaddr, ctypes.POINTER(ctypes.c_uint32))

        buf[0] = 0xdeadbeee
        buf[1] = 0xdeadbeef

        cnt = 0

        while dev.mem.read_dword(0xb50) >> 16 != 0x88b5:
            cnt += 1
            if cnt > 10000:
                print "[-] fw signature not found in gencomm"
                return
            usleep(10)

        dev.mem.write_dword(0xb54, paddr >> 32)
        dev.mem.write_dword(0xb58, paddr & 0xffffffff)
        dev.mem.write_dword(0xb50, 0x88b50007)

        while dev.mem.read_dword(0xb50) & 0xff:
            pass

        if buf[0] != dev.mem.read_dword(0xb54) or buf[1] != dev.mem.read_dword(0xb58):
            print "[-] remote dma read test failed"
        else:
            print "[+] remote dma read test complete"

        dev.interface.mm.free(vaddr)

    def test_dmar(self, size=0x80, init=1, reset=0):
        dev = self.dev
        dev.rxcpu.halt()
        dev.bufman.block_enable()
        dev.grc.mode.pcie_tl_sel = 0
        dev.grc.mode.pcie_pl_sel = 1
        dev.grc.mode.pcie_hi1k_en = 1
        dev.hpmb.box[tg.mb_rbd_standard_producer].low = 0
        
        end = 0x6000 + (size * 4)
        print "[+] clearing device memory from 0x6000 to 0x%04x" % end
        for i in range(0x6000, end, 4):
                dev.mem.write_dword(i, 0)

        for i in range(0x6000, end, 4):
                if dev.mem.read_dword(i) != 0:
                        raise Exception("buffer not clear")
        
        print "[+] zapping rdi std rcb"
        dev.rdi.std_rcb.host_addr_hi = 0
        dev.rdi.std_rcb.host_addr_low = 0
        dev.rdi.std_rcb.ring_size = 0
        dev.rdi.std_rcb.max_frame_len = 0
        dev.rdi.std_rcb.disable_ring = 0
        dev.rdi.std_rcb.nic_addr = 0

        vaddr = dev.interface.mm.alloc(4 * size)
        paddr = dev.interface.mm.get_paddr(vaddr)
        buf = ctypes.cast(vaddr, ctypes.POINTER(ctypes.c_uint32))

        for i in range(size):
                buf[i] = 0xaabbccdd;
        
        state = reutils.state_save(dev)

        print "[+] setting up standard rcb"

        dev.rdi.std_rcb.host_addr_hi = (paddr >> 32)
        dev.rdi.std_rcb.host_addr_low = (paddr & 0xffffffff)
        dev.rdi.std_rcb.ring_size = 0x200
        dev.rdi.std_rcb.max_frame_len = 0
        dev.rdi.std_rcb.disable_ring = 0
        dev.rdi.std_rcb.nic_addr = 0x6000
        
        state = reutils.state_diff(dev, state)

        print "[+] initiating dma read of sz %x to buffer at vaddr %x, paddr %x" % (size, vaddr, paddr)
        dev.hpmb.box[tg.mb_rbd_standard_producer].low = size >> 3

        blocks = ["rbdi", "rdma"]
        for b in blocks:
                o = getattr(dev, b)
                o.block_enable(reset=reset)
                state = reutils.state_diff(dev, state)
        
        for i in range(0x6000, end, 4):
                if dev.mem.read_dword(i) != buf[(i - 0x6000) >> 2]:
                        raise Exception("dma read test failed")

        print "[+] dma read test complete"

        dev.interface.mm.free(vaddr)

    def test_dmaw(self):
        dev = self.dev
        dev.rxcpu.halt()
        dev.bufman.block_enable()
        dev.grc.mode.pcie_tl_sel = 1
        dev.grc.mode.pcie_pl_sel = 0
        dev.grc.mode.pcie_hi1k_en = 0

        buf_v = dev.interface.mm.alloc(0x80)
        buf_p = dev.interface.mm.get_paddr(buf_v)
        sbuf = cast(buf_v, POINTER(c_char * 0x80))

        dev.wdma.block_disable()
        dev.wdma.reset()

        dev.hc.block_disable()
        dev.hc.reset()

        state = reutils.state_save(dev)

        dev.hc.nic_diag_sbd_ci[0] = 4
        dev.hc.status_block_host_addr_hi = buf_p >> 32
        dev.hc.status_block_host_addr_low = buf_p & 0xffffffff
        dev.hc.mode.no_int_on_force_update = 1

        for i in range(0x3d00, 0x3e00, 4):
            dev.reg[i >> 2] = 0xffffffff
        dev.reg[0x3f04 >> 2] = 0xffffffff

        state = reutils.state_diff(dev, state) 

        print "[*] coalescing"
        dev.hc.mode.coalesce_now = 1
        state = reutils.state_diff(dev, state)

        print "[*] status block is now"
        print "    %s" % repr(sbuf.contents.raw)
        print


        dev.wdma.block_enable()
        state = reutils.state_diff(dev, state)

        print "[*] status block is now"
        print "    %s" % repr(sbuf.contents.raw)
        print
       
        print "[*] coalescing"
        dev.hc.mode.coalesce_now = 1
        state = reutils.state_diff(dev, state)

        print "[*] status block is now"
        print "    %s" % repr(sbuf.contents.raw)
        print

    def reg_finder(self):
        dev = self.dev
        regs = {}
        with open('regs.csv', 'wb') as csvfile:
            fns = ['offset', 'block', 'name', 'rw', 'mod_mask', 'o', 't1', 't2']
            w = csv.DictWriter(csvfile, fieldnames=fns)
            w.writeheader()

            for dl in (True, False):
                for pl in (True, False):
                    for hi1k in (True, False):
                        dev.grc.mode.pcie_dl_sel = 1 if dl else 0
                        dev.grc.mode.pcie_pl_sel = 1 if pl else 0
                        dev.grc.mode.pcie_hi1k_en = 1 if hi1k else 0
                        ss = "%s%s%s" % ("d" if dl else "",
                                         "p" if pl else "",
                                         "h" if hi1k else "")

                        for i in range(0x7c00, 0x8000, 4):
                            ofs = "%04x%s" % (i, ss)
                            bn = reutils.whats_at(i)
                            regs[ofs] = {'block': 'pcie_win',
                                       'name': 'ofs_%03x' % (i - 0x7c00),
                                       'offset': ofs,
                                       'rw': '',
                                       'mod_mask': '',
                                       'o': '', 't1': '', 't2': ''}

                            o = dev.reg[i >> 2]
                            if o == 0xffffffff:
                                if dev.reg[0] == 0xffffffff:
                                    raise Exception("device quit bus")

                            if False:
                                dev.reg[i >> 2] = 0xffffffff
                                t1 = dev.reg[i >> 2]
                                dev.reg[i >> 2] = 0
                                t2 = dev.reg[i >> 2]
                                dev.reg[i >> 2] = o
                                regs[ofs]['t1'] = "%08x" % t1
                                regs[ofs]['t2'] = "%08x" % t2
                                if (o ^ t1) or (o ^ t2):
                                    regs[ofs]['rw'] = True
                                    regs[ofs]['mod_mask'] = "%08x" % (~(t2 | ~t1))
                            
                            regs[ofs]['o'] = "%08x" % o
                            
                            w.writerow(regs[ofs])
                            csvfile.flush()

            for i in range(0x100, 0x7c00, 4):
                if i % 0x400 == 0:
                    print "now at %04x" % i
                if 0 == os.system("dmesg -c | grep -q dmar"):
                    raise Exception("noticed dmar freaking out at %04x" % i)

                bn = reutils.whats_at(i)
                regs[i] = {'block': bn[0],
                           'name': bn[1],
                           'offset': "%04x" % i,
                           'rw': False,
                           'mod_mask': '',
                           'o': '', 't1': '', 't2': ''}

                o = dev.reg[i >> 2]
                if o == 0xffffffff:
                    if dev.reg[0] == 0xffffffff:
                        raise Exception("device quit bus")

                if (i < 0x3600 or i > 0x36e8) and (i < 0x6800 or i > 0x68fc):
                    dev.reg[i >> 2] = 0xffffffff
                    t1 = dev.reg[i >> 2]
                    dev.reg[i >> 2] = 0
                    t2 = dev.reg[i >> 2]
                    dev.reg[i >> 2] = o

                regs[i]['o'] = "%08x" % o
                try:
                    regs[i]['t1'] = "%08x" % t1
                    regs[i]['t2'] = "%08x" % t2
                    if (o ^ t1) or (o ^ t2):
                        regs[i]['rw'] = True
                        regs[i]['mod_mask'] = "%08x" % (~(t2 | ~t1))
                except:
                    pass

                if regs[i]['name'].startswith('ofs') and regs[i]['rw']:
                    print "Unknown rw register at %04x" % i

                w.writerow(regs[i])


        return regs
