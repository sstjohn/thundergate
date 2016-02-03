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

import tglib as tg
import ctypes

def _init_xx_ring(self, bdtype):
    mm = self.mm
    ring_len = mm.page_sz / ctypes.sizeof(bdtype)
    if ring_len > 512:
        ring_len = 512

    for i in range(4):
        ring_len |= (ring_len >> (2 ** i))

    ring_len = ring_len - (ring_len >> 1)

    vaddr = mm.alloc(ring_len * ctypes.sizeof(bdtype))
    return (vaddr, ring_len)

def init_tx_rings(self):
    mm = self.mm
    self.tx_ring_vaddr, self.tx_ring_len = _init_xx_ring(self, tg.sbd)
    self.tx_ring_paddr = mm.get_paddr(self.tx_ring_vaddr)
    self._tx_pi = 0
    self._tx_ci = 0
    self._tx_buffers = [0] * self.tx_ring_len

    dev = self.dev

    dev.mem.txrcb[0].addr_hi = self.tx_ring_paddr >> 32
    dev.mem.txrcb[0].addr_low = self.tx_ring_paddr & 0xffffffff
    dev.mem.txrcb[0].max_len = self.tx_ring_len
    #dev.mem.txrcb[0].nic_addr = 0x4000
    dev.mem.txrcb[0].flags.disabled = 0

    print "[+] send ring 0 of size %d allocated at %x" % (self.tx_ring_len, self.tx_ring_vaddr)

    for i in range(len(dev.mem.txrcb) - 1):
        dev.mem.txrcb[i + 1].flags.disabled = 1
        print "[+] send ring %d disabled" % (i + 1)

def init_rx_rings(self):
    dev = self.dev
    mm = self.mm

    dev.rdi.mini_rcb.disable_ring = 1
    print "[+] mini receive producer ring disabled"

    self.rx_ring_vaddr, self.rx_ring_len = _init_xx_ring(self, tg.rbd)
    self.rx_ring_paddr = mm.get_paddr(self.rx_ring_vaddr)
    
    dev.rdi.std_rcb.host_addr_hi = self.rx_ring_paddr >> 32
    dev.rdi.std_rcb.host_addr_low = self.rx_ring_paddr & 0xffffffff
    dev.rdi.std_rcb.ring_size = self.rx_ring_len
    dev.rdi.std_rcb.max_frame_len = 0x600
    dev.rdi.std_rcb.nic_addr = 0x6000
    dev.rdi.std_rcb.disable_ring = 0

    print "[+] standard receive producer ring of size %d allocated at %x" % (self.rx_ring_len, self.rx_ring_vaddr)

    dev.rdi.jumbo_rcb.disable_ring = 1
    print "[+] jumbo receive producer ring disabled"

def init_rr_rings(self):
    dev = self.dev
    mm = self.mm

    ring_vaddr, self.rr_rings_len = _init_xx_ring(self, tg.rbd)
    self.rr_rings_vaddr = [ring_vaddr]
    
    print "[+] receive return ring 0 of size %d allocated at %x" % (self.rr_rings_len, ring_vaddr)

    for i in range(1, len(dev.mem.rxrcb)):
        ring_vaddr, tmp = _init_xx_ring(self, tg.rbd)
        assert tmp == self.rr_rings_len
        self.rr_rings_vaddr += [ring_vaddr]
        print "[+] receive return ring %d of size %d allocated at %x" % (i, tmp, ring_vaddr)

    self.rr_rings_ci = [0] * len(dev.mem.rxrcb)

    self.rr_rings_paddr = []
    for i in range(0, len(dev.mem.rxrcb)):
        ring_vaddr = self.rr_rings_vaddr[i]

        p = mm.get_paddr(ring_vaddr)
        self.rr_rings_paddr += [p]

        dev.mem.rxrcb[i].addr_hi = (p >> 32)
        dev.mem.rxrcb[i].addr_low = (p & 0xffffffff)
        dev.mem.rxrcb[i].nic_addr = 0x6000
        dev.mem.rxrcb[i].max_len = self.rr_rings_len
        dev.mem.rxrcb[i].flags.disabled = 0

def populate_rx_ring(self, count = None):
    if count == None:
        count = self.rx_ring_len - 1
    assert count < self.rx_ring_len
    mm = self.mm
    r = ctypes.cast(self.rx_ring_vaddr, ctypes.POINTER(tg.rbd))
    self.rx_ring_bds = r
    self.rx_ring_buffers = []
    for i in range(self.rx_ring_len):
        buf = mm.alloc(0x800)
        self.rx_ring_buffers += [buf]

        pbuf = mm.get_paddr(buf)
        r[i].addr_hi = pbuf >> 32
        r[i].addr_low = pbuf & 0xffffffff
        r[i].index = i
        r[i].length = 0x800
        r[i].flags.disabled = 0

    print "[+] produced %d rx buffers" % self.rx_ring_len
    self.dev.hpmb.box[tg.mb_rbd_standard_producer].low = count
    self._std_rbd_pi = count
    self._std_rbd_ci = 0
