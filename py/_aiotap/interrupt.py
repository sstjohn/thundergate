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

from ctypes import cast, POINTER, c_char
import logging

import tglib as tg

logger = logging.getLogger(__name__)


async def _handle_interrupt(self):
    dev = self.dev
    if self.verbose:
        sb = self.status_block
        logger.info("handling interrupt -- sb: updated=%d tag=%d att=%d "
                    "link=%d rpci=%x rr0_pi=%x", sb.updated, sb.status_tag,
                    sb.attention, sb.link_status, sb.rpci, sb.rr0_pi)

    # Mask the NIC interrupt for the duration of this handler. This chip's
    # MSI is not one-shot, and the macOS dext never masks it between
    # deliveries -- so unless the host writes a non-zero value to
    # interrupt-mailbox-0, the NIC keeps re-signalling and the handler
    # storms (tg3_msi: "Writing non-zero to intr-mbox-0 ... tells the NIC
    # to stop sending us irqs"). The tag << 24 write at the end re-enables
    # the interrupt and, in tagged-status mode, acks the tag.
    dev.hpmb.box[tg.mb_interrupt].low = 1
    _ = dev.hpmb.box[tg.mb_interrupt].low

    # Capture status_tag now and always write it back below. The old code
    # computed the tag only inside `while self.status_block.updated`, so an
    # interrupt taken with `updated` already 0 -- the steady state in
    # tagged mode -- wrote tag 0 and never acked. Work is driven off the
    # ring indices, not `updated`: _handle_rr, _replenish_rx_bds and
    # _free_sent_bds each no-op when their producer and consumer indices
    # already agree.
    tag = self.status_block.status_tag
    self.status_block.updated = 0

    if dev.emac.status.link_state_changed:
        # ack only -- calling link_detect() here restarts PHY
        # autonegotiation, which itself raises a fresh link event.
        self.dev.emac.status.link_state_changed = 1

    for i in range(len(dev.mem.rxrcb)):
        _handle_rr(self, i)
    _replenish_rx_bds(self)
    _free_sent_bds(self)

    if self.verbose:
        logger.info("interrupt handling concluded")
    self.dev.hpmb.box[tg.mb_interrupt].low = tag << 24
    _ = self.dev.hpmb.box[tg.mb_interrupt].low


def _handle_rr(self, i):
    '''Drain return ring i: deliver each received frame to the host tap
    and swap a fresh buffer into the producer-ring slot it came from.'''
    pi = getattr(self.status_block, "rr%d_pi" % i)
    ci = self.rr_rings_ci[i]
    if pi == ci:
        return

    count = pi - ci if pi >= ci else self.rr_rings_len - ci + pi
    if self.verbose:
        logger.info("rr %d: pi %x, ci %x, %d bds received", i, pi, ci, count)

    rr_bds = cast(self.rr_rings_vaddr[i], POINTER(tg.rbd))
    rx_bds = cast(self.rx_ring_vaddr, POINTER(tg.rbd))
    while count > 0:
        ci += 1
        if ci > self.rr_rings_len:
            ci = 1
        rbd = rr_bds[ci - 1]
        if rbd.index >= len(self.rx_buffers):
            logger.warning("rr %d: bogus return-bd index 0x%x at ci %d; "
                           "stopping ring drain", i, rbd.index, ci)
            break
        if self.verbose:
            _dump_bd(self, ci, rbd)

        old_buf = self.rx_buffers[rbd.index]
        pkt = cast(old_buf, POINTER(c_char * rbd.length))[0]

        new_buf = self.mm.alloc(0x800)
        new_pbuf = self.mm.get_paddr(new_buf)
        rx_bds[rbd.index].addr_hi = new_pbuf >> 32
        rx_bds[rbd.index].addr_low = new_pbuf & 0xffffffff
        self.rx_buffers[rbd.index] = new_buf

        self._put_tap_packet(pkt)
        self.stats.pkt_in(rbd.length)
        self.mm.free(old_buf)

        count -= 1

    mb = getattr(tg, "mb_rbd_rr%d_consumer" % i)
    self.dev.hpmb.box[mb].low = ci
    self.rr_rings_ci[i] = ci


def _replenish_rx_bds(self):
    new_ci = self.status_block.rpci
    old_ci = self._std_rbd_ci
    count = 0
    if new_ci != old_ci:
        if self.verbose:
            logger.debug("rbdp ci now %x, was %x", new_ci, old_ci)
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
            logger.debug("moving std rbd pi to %x", self._std_rbd_pi)
        self.dev.hpmb.box[tg.mb_rbd_standard_producer].low = self._std_rbd_pi


def _free_sent_bds(self):
    tx_ci = self.status_block.sbdci
    if tx_ci != self._tx_ci:
        if self.verbose:
            logger.debug("sbd ci: %x", tx_ci)

        if tx_ci < self._tx_ci:
            if self.verbose:
                if self._tx_ci + 1 == self.tx_ring_len:
                    logger.debug("freeing tx buffer %02x", self._tx_ci)
                else:
                    logger.debug("freeing tx buffers %02x-%02x", self._tx_ci, self.tx_ring_len - 1)
            while self._tx_ci < self.tx_ring_len:
                self.mm.free(self._tx_buffers[self._tx_ci])
                self._tx_ci += 1
        if self._tx_ci == self.tx_ring_len:
            self._tx_ci = 0
        if self.verbose:
            if tx_ci == self._tx_ci + 1:
                logger.debug("freeing tx buffer %02x", self._tx_ci)
            elif tx_ci > self._tx_ci:
                logger.debug("freeing tx buffers %02x-%02x", self._tx_ci, tx_ci - 1)
        while tx_ci > self._tx_ci:
            self.mm.free(self._tx_buffers[self._tx_ci])
            self._tx_ci += 1


def _dump_bd(self, ci, rbd):
    print("consuming bd 0x%x" % ci)
    print(" addr:      %08x:%08x" % (rbd.addr_hi, rbd.addr_low))
    print("  buf[%d] vaddr: %x, paddr: %x" % (rbd.index, self.rx_buffers[rbd.index], self.mm.get_paddr(self.rx_buffers[rbd.index])))
    print(" length:    %04x" % rbd.length)
    print(" index:     %04x" % rbd.index)
    print(" type:      %04x" % rbd.type)
    print(" flags:    ", end=' ')
    for j in ["is_ipv6", "is_tcp", "l4_checksum_correct", "ip_checksum_correct", "reserved", "has_error", "has_vlan_tag", "reserved2", "reserved3", "rss_hash_valid", "packet_end", "reserved4", "reserved5"]:
        if getattr(rbd.flags, j):
            print(j, end=' ')
    print()

    if rbd.flags.rss_hash_type != 0:
        print(" rss hash type: %x" % rbd.flags.rss_hash_type)

    print(" ip cksum:  %04x" % rbd.ip_cksum)
    print(" l4 cksum: %04x" % rbd.l4_cksum)
    print(" err flags:", end=' ')
    for j in ["reserved1", "reserved2", "reserved3", "reserved4", "reserved5", "reserved6", "reserved7", "giant_packet", "trunc_no_res", "len_less_64", "mac_abort", "dribble_nibble", "phy_decode_error", "link_lost", "collision", "bad_crc"]:
        if getattr(rbd.error_flags, j):
            print(j, end=' ')
    print()
    print(" vlan_tag:  %04x" % rbd.vlan_tag)
    print(" rss_hash:  %08x" % rbd.rss_hash)
    print(" opaque:    %08x" % rbd.opaque)
