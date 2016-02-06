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

from ctypes import cast, POINTER, c_char
import tglib as tg

def handle_rr(self, i):
    pi = getattr(self.status_block, "rr%d_pi" % i)
    ci = self.rr_rings_ci[i]

    if pi != ci:
        if self.verbose:
            print "[+] rr %d: pi is %x, ci was %x," % (i, pi, ci),

        if pi < ci:
            count = self.rr_rings_len - ci 
            count += pi
        else:
            count = pi - ci
        
        if self.verbose:
            print "%d bds received" % count

        rbds = cast(self.rr_rings_vaddr[i], POINTER(tg.rbd))
        while count > 0:
            ci += 1
            if ci > self.rr_rings_len:
                ci = 1
            rbd = rbds[ci - 1]

            if self.verbose:
                self._dump_bd(ci, rbd)

            pkt = cast(self.rx_ring_buffers[rbd.index], POINTER(c_char * rbd.length))[0]
            
            new_buf = self.mm.alloc(0x800)
            new_pbuf = self.mm.get_paddr(new_buf)
            self.rx_ring_bds[rbd.index].addr_hi = new_pbuf >> 32
            self.rx_ring_bds[rbd.index].addr_low = new_pbuf & 0xffffffff
            self.rx_ring_buffers[rbd.index] = new_buf

            self.put_tap_pkt(pkt)
             
            count -= 1

        mb = getattr(tg, "mb_rbd_rr%d_consumer" % i)
        self.dev.hpmb.box[mb].low = ci
        self.rr_rings_ci[i] = ci

def handle_interrupt(self):
    dev = self.dev
    if self.verbose:
        print "[+] handling interrupt"
    
    _ = dev.hpmb.box[tg.mb_interrupt].low
    tag = 0

    while self.status_block.updated:
        tag = self.status_block.status_tag
        if self.verbose:
            print "[+] status tag %x" % tag
        tag = tag << 24

        self.status_block.updated = 0
        if self.verbose:
            print "[+] status block updated! link: %d, attention: %d" % (self.status_block.link_status, self.status_block.attention)

        if dev.emac.status.link_state_changed:
            self._link_detect()
            dev.emac.status.link_state_changed = 1
            
        for i in range(len(dev.mem.rxrcb)):
            self._handle_rr(i)
        
        self._replenish_rx_bds()

        self._free_sent_bds()

    if self.verbose:
        print "[+] interrupt handling concluded"
    self.dev.hpmb.box[tg.mb_interrupt].low = tag
    _ = self.dev.hpmb.box[tg.mb_interrupt].low

def replenish_rx_bds(self):
    new_ci = self.status_block.rpci
    old_ci = self._std_rbd_ci
    count = 0
    if new_ci != old_ci:
        if self.verbose:
            print "[+] rbdp ci now %x, was %x" % (new_ci, old_ci)
        rbds = cast(self.rx_ring_vaddr, POINTER(tg.rbd))
        while new_ci != old_ci:
            count += 1
            rbds[old_ci].flags.word = 0
            rbds[old_ci].error_flags.word = 0
            rbds[old_ci].length = 0x600
            old_ci += 1
            if old_ci == self.rx_ring_len:
                old_ci = 0

        self._std_rbd_ci = new_ci

        self._std_rbd_pi += count
        if self._std_rbd_pi >= self.rx_ring_len:
            self._std_rbd_pi -= self.rx_ring_len

        if self.verbose:
            print "[+] moving std rbd pi to %x" % self._std_rbd_pi
        self.dev.hpmb.box[tg.mb_rbd_standard_producer].low = self._std_rbd_pi

def free_sent_bds(self):
    tx_ci = self.status_block.sbdci
    if tx_ci != self._tx_ci:
        if self.verbose:
            print "[+] sbd ci: %x" % tx_ci

        if tx_ci < self._tx_ci:
            if self.verbose:
                if self._tx_ci + 1 == self.tx_ring_len:
                    print "[.] freeing tx buffer %02x" % self._tx_ci
                else:
                    print "[.] freeing tx buffers %02x-%02x" % (self._tx_ci, self.tx_ring_len - 1)
            while self._tx_ci < self.tx_ring_len:
                self.mm.free(self._tx_buffers[self._tx_ci])
                self._tx_ci += 1
        if self._tx_ci == self.tx_ring_len:
            self._tx_ci = 0
        if self.verbose:
            if tx_ci == self._tx_ci + 1:
                print "[.] freeing tx buffer %02x" % self._tx_ci
            elif tx_ci > self._tx_ci:
                print "[.] freeing tx buffers %02x-%02x" % (self._tx_ci, tx_ci - 1)
        while tx_ci > self._tx_ci:
            self.mm.free(self._tx_buffers[self._tx_ci])
            self._tx_ci += 1

def dump_bd(self, ci, rbd):
    print "consuming bd 0x%x" % ci
    print " addr:      %08x:%08x" % (rbd.addr_hi, rbd.addr_low)
    print "  buf[%d] vaddr: %x, paddr: %x" % (rbd.index, self.rx_ring_buffers[rbd.index], self.mm.get_paddr(self.rx_ring_buffers[rbd.index]))
    print " length:    %04x" % rbd.length
    print " index:     %04x" % rbd.index
    print " type:      %04x" % rbd.type
    print " flags:    ",
    for j in ["is_ipv6", "is_tcp", "l4_checksum_correct", "ip_checksum_correct", "reserved", "has_error", "has_vlan_tag", "reserved2", "reserved3", "rss_hash_valid", "packet_end", "reserved4", "reserved5"]:
        if getattr(rbd.flags, j):
            print j,
    print

    if rbd.flags.rss_hash_type != 0:
        print " rss hash type: %x" % rbd.flags.rss_hash_type

    print " ip cksum:  %04x" % rbd.ip_cksum
    print " l4 cksum: %04x" % rbd.l4_cksum
    print " err flags:",
    for j in ["reserved1", "reserved2", "reserved3", "reserved4", "reserved5", "reserved6", "reserved7", "giant_packet", "trunc_no_res", "len_less_64", "mac_abort", "dribble_nibble", "phy_decode_error", "link_lost", "collision", "bad_crc"]:
        if getattr(rbd.error_flags, j):
            print j,
    print
    print " vlan_tag:  %04x" % rbd.vlan_tag
    print " rss_hash:  %08x" % rbd.rss_hash
    print " opaque:    %08x" % rbd.opaque

