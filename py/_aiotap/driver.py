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

import ctypes
import tglib as tg
import struct
import time
import os
import select
import reutils
import platform
import functools
import sys

import asyncio

import logging
logger = logging.getLogger(__name__)

from .stats import TapStatistics

default_verbosity = 0

sys_name = platform.system()

if sys_name == "Linux":
    import fcntl

    import cabi as c
    from cabi import *
    from .linux import TapLinuxInterface
    TDInt = TapLinuxInterface

elif sys_name == "Windows" or sys_name == "cli":
    from winlib import *
    from .win import TapWinInterface
    TDInt = TapWinInterface

    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

elif sys_name == "Darwin":
    from .macos import TapMacInterface
    TDInt = TapMacInterface

else:
    raise NotImplementedError("tap driver only available on linux, macos and windows")
   
from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

from ctypes import cast, pointer, POINTER, sizeof

from .dev_fns import _device_setup, _enable_rx, _enable_tx
from .link import _link_detect
from .interrupt import _handle_interrupt


class TapDriver(TDInt):
    def __init__(self, dev):
        self.verbose = default_verbosity
        super(TapDriver, self).__init__(dev)
        self.dev = dev
        self.mm = dev.interface.mm
        self.stats = TapStatistics()
        self._connected = False

    def __enter__(self):
        print("[+] tap driver initializing")
        super(TapDriver, self).__enter__()
        return self

    def __exit__(self, t, v, traceback):
        super(TapDriver, self).__exit__()
        self.dev.close()
        print("[+] tap driver terminated")

    device_setup = _device_setup
    enable_rx = _enable_rx
    enable_tx = _enable_tx
    
    link_detect = _link_detect
    handle_interrupt = _handle_interrupt

    async def gui_handler(self):
        '''launch wxwidgets gui'''
        import gui
        gui.run(self.dev)

    async def help_handler(self):
        '''display keypress bindings'''
        print()
        for k in self.keypress_handlers:
            print("%s - %s" % (k, self.keypress_handlers[k].__doc__))
        print()

    async def verbosity_handler(self):
        '''toggle tap driver verbosity'''
        self.verbose = not self.verbose
        print("[+] verbosity %s" % ("enabled" if self.verbose else "disabled"))

    async def rxstats_handler(self):
        '''dump NIC MAC counters and receive state'''
        dev = self.dev
        s = dev.stats
        rxm = dev.emac.rx_mac_mode
        sb = self.status_block
        print()
        print("[s] MAC rx in:   ucast=%d mcast=%d bcast=%d" % (
            s.ifHCInUcastPkts, s.ifHCInMulticastPkts, s.ifHCInBroadcastPkts))
        print("[s] MAC rx errs: fcs=%d align=%d undersize=%d toolong=%d "
              "jabber=%d frag=%d" % (
            s.dot3StatsFCSErrors, s.dot3StatsAlignmentErrors,
            s.etherStatsUndersizePkts, s.dot3StatsFramesTooLongs,
            s.etherStatsJabbers, s.etherStatsFragments))
        print("[s] MAC tx out:  ucast=%d mcast=%d bcast=%d  (TX sanity)" % (
            s.iHCOutUcastPkts, s.iHCOutMulticastPkts, s.iHCOutBroadcastPkts))
        print("[s] rx_mac_mode: enable=%d promiscuous=%d accept_runts=%d "
              "rss=%d  rules default class=%d" % (
            rxm.enable, rxm.promiscuous_mode, rxm.accept_runts, rxm.rss_enable,
            dev.emac.rx_rules_conf.no_rules_matches_default_class))
        print("[s] status block: rpci=%x rr0_pi=%x rr1_pi=%x rr2_pi=%x "
              "rr3_pi=%x sbdci=%x" % (
            sb.rpci, sb.rr0_pi, sb.rr1_pi, sb.rr2_pi, sb.rr3_pi, sb.sbdci))
        fa = dev.hc.flow_attention
        attn = [n for n in ('sbdi', 'sbdc', 'sbdrs', 'sdi', 'sdc', 'rbdi',
                'rbdc', 'rlp', 'rls', 'rdi', 'rdc', 'rcb_incorrect',
                'dmac_discard', 'hc', 'ma', 'mbuf_low_water')
                if getattr(fa, n)]
        print("[s] flow attention: %s" % (" ".join(attn) if attn else "(none)"))

        # The RX pipeline between the MAC and the return ring: RLP rule-
        # classification status and counters, and the chip's own view of
        # the producer and return ring indices (rdi/rbdi local_*).
        try:
            rlp = dev.rlp
            rs = rlp.status
            print("[s] rlp status:  class_zero=%d mapping_oor=%d stats_ovf=%d"
                  % (rs.class_zero_attention,
                     rs.mapping_out_of_range_attention,
                     rs.stats_overflow_attention))
            rc = rlp.config
            print("[s] rlp config:  default_q=%d bad_frames_class=%d "
                  "active_lists=%d lists_per_grp=%d" % (
                      rc.default_interrupt_distribution_queue,
                      rc.bad_frames_class, rc.number_of_active_lists,
                      rc.number_of_lists_per_distribution_group))
            ctrs = " ".join("%d:%d" % (i, rlp.stat_counter[i].counters_value)
                            for i in range(23)
                            if rlp.stat_counter[i].counters_value)
            print("[s] rlp counters:%s" % (" " + ctrs if ctrs else " (all zero)"))
            print("[s] rlp lists non-empty: %04x"
                  % rlp.selector_not_empty_bits.list_non_empty_bits)
            rbdi = dev.rbdi
            print("[s] rbdi: bds_avail_on_disabled_ring=%d local_std_rbd_pi=%x"
                  % (rbdi.status.receive_bds_available_on_disabled_rbd_ring,
                     rbdi.local_std_rbd_pi))
            rdi = dev.rdi
            print("[s] rdi:  illegal_rr_size=%d frame_too_large=%d "
                  "local_std_rbd_ci=%x local_rr0_pi=%x" % (
                      rdi.status.illegal_return_ring_size,
                      rdi.status.frame_size_too_large_for_bd,
                      rdi.local_std_rbd_ci, rdi.local_rr_pi[0]))
            print("[s] rbdc error=%d  bufman: mbuf_low=%d error=%d" % (
                dev.rbdc.status.error,
                dev.bufman.status.mbuf_low_attention,
                dev.bufman.status.error))
            print("[s] driver: std_rbd_pi=%x std_rbd_ci=%x prod_mailbox=%x" % (
                self._std_rbd_pi, self._std_rbd_ci,
                dev.hpmb.box[tg.mb_rbd_standard_producer].low))
            # The next producer BDs the chip will consume; a zero addr or
            # bogus index/flags here points at a stalled RX ring.
            rxb = ctypes.cast(self.rx_ring_vaddr, ctypes.POINTER(tg.rbd))
            for j in range(sb.rpci, sb.rpci + 3):
                b = rxb[j % self.rx_ring_len]
                print("[s]   prod bd[%d]: addr=%08x:%08x len=%x idx=%d "
                      "flags=%04x" % (j % self.rx_ring_len, b.addr_hi,
                      b.addr_low, b.length, b.index, b.flags.word))
        except Exception as e:
            print("[s] RX pipeline dump failed: %r" % e)
        print()

    async def quit_handler(self):
        '''terminate tap driver execution and close device'''
        self.running = False
        self.loop.stop()

    async def unknown_keypress_handler(self, k):
        print("read unknown keypress '%s'" % k)

    async def keypress_dispatch(self):
        r = await self.loop.run_in_executor(None, self._wait_for_keypress)
        if not self.running:
            # quit_handler has cleared self.running and stopped the loop;
            # _wait_for_keypress returned None without blocking. Don't
            # dispatch or re-arm -- the default executor is being shut
            # down, and another run_in_executor would raise.
            return
        if r in self.keypress_handlers:
            asyncio.ensure_future(self.keypress_handlers[r]())
        else:
            asyncio.ensure_future(self.unknown_keypress_handler(r))
        asyncio.ensure_future(self.keypress_dispatch())

    def _watch_for_sb_update(self):
        logger.info("watching for status block update")
        while self.running:
            if self.status_block.updated:
                logger.info("status block updated")
                return
            time.sleep(.01)
        logger.info("status block not updated, terminating watch")

    async def interrupt_watcher(self):
        if hasattr(self, "_wait_for_interrupt"):
            waiter = self._wait_for_interrupt
        else:
            waiter = self._watch_for_sb_update

        await self.loop.run_in_executor(None, waiter)
        await self.handle_interrupt()
        if self.running:
            asyncio.ensure_future(self.interrupt_watcher())

    def _send_b(self, buf, buf_sz):
        '''Hand a DMA buffer holding one frame to the NIC's send ring.'''
        i = self._tx_pi
        self._tx_buffers[i] = buf
        paddr = self.mm.get_paddr(buf)
        txb = cast(self.tx_ring_vaddr, POINTER(tg.sbd))
        txb[i].addr_hi = paddr >> 32
        txb[i].addr_low = paddr & 0xffffffff
        txb[i].length = buf_sz
        txb[i].flags.packet_end = 1
        i = (i + 1) % self.tx_ring_len
        self.dev.hpmb.box[tg.mb_sbd_host_producer].low = i
        _ = self.dev.hpmb.box[tg.mb_sbd_host_producer].low  # flush the posted write
        self._tx_pi = i
        self.stats.pkt_out(buf_sz)

    async def tap_watcher(self):
        buf = self.mm.alloc(0x800)
        buf, n = await self.loop.run_in_executor(
            None, self._get_tap_packet, buf, 0x800)
        if self.verbose:
            logger.info("tap_watcher: %d bytes from the host feth", n)
        if n < 64:
            ctypes.memset(buf + n, 0, 64 - n)
            n = 64
        self._send_b(buf, n)
        if self.running:
            asyncio.ensure_future(self.tap_watcher())

    async def arrive_device(self):
        await self.device_setup()
        # The host feth must answer to the NIC's MAC or the host stack
        # drops its unicast traffic; device_setup has just read it.
        if hasattr(self, "_adopt_nic_mac"):
            self._adopt_nic_mac()
        await self.enable_rx()
        await self.enable_tx()
        # negotiate the PHY and set emac.mode.port_mode -- the EMAC will
        # not pass traffic until the link parameters are programmed.
        await self.link_detect()
        rxm = self.dev.emac.rx_mac_mode
        logger.info("rx mac mode: promiscuous=%d accept_runts=%d enable=%d",
                    rxm.promiscuous_mode, rxm.accept_runts, rxm.enable)
        # PG 7.1 step 74 -- enable the host interrupt. dev.init() leaves
        # it masked; until it is cleared the chip raises no MSI.
        self.dev.hpmb.box[tg.mb_interrupt].low = 0
        self.dev.unmask_interrupts()
        asyncio.ensure_future(self.interrupt_watcher())
        asyncio.ensure_future(self.tap_watcher())

    def run(self):
        self.running = True
        self.keypress_handlers = {
            'g': self.gui_handler,
            'h': self.help_handler,
            'q': self.quit_handler,
            's': self.rxstats_handler,
            'v': self.verbosity_handler,
        }

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self.keypress_dispatch())
        self.loop.create_task(self.arrive_device())
        self.loop.run_forever()
        self.loop.run_until_complete(self.loop.shutdown_default_executor())
        self.loop.close()
