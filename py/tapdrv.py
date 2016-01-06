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
import tglib as tg
import struct
import os
import select
import reutils
import platform

verbose = 0
sys_name = platform.system()

if sys_name == "Linux":
    import fcntl
    
    import clib as c
    from tunlib import *
    tap_close = os.close
elif sys_name == "Windows":
    from winlib import *
    tap_close = del_tap_if
else:
    raise NotImplementedError("tap driver only available on linux and windows")
   
from time import sleep
usleep = lambda x: sleep(x / 1000000.0)

from ctypes import cast, pointer, POINTER, sizeof

class TapDriver(object):
    def __init__(self, dev):
        self.dev = dev
        self.mm = dev.interface.mm

    def __enter__(self):
        print "[+] driver initialization begins"
        if sys_name == "Linux":
            fd = os.open("/dev/net/tun", os.O_RDWR)
            ifr = struct.pack('16sH', 'tap0', IFF_TAP | IFF_NO_PI)
            fcntl.ioctl(fd, TUNSETIFF, ifr)
            self.tfd = fd
        elif sys_name == "Windows":
            self.tfd = create_tap_if()

        self._device_setup()

        return self

    def __exit__(self, t, v, traceback):
        self.dev.close()
        tap_close(self.tfd)
        print "[+] driver terminated"
                
    def __init_xx_ring(self, bdtype):
        mm = self.mm
        ring_len = mm.page_sz / ctypes.sizeof(bdtype)
        if ring_len > 512:
            ring_len = 512

        for i in range(4):
            ring_len |= (ring_len >> (2 ** i))

        ring_len = ring_len - (ring_len >> 1)

        vaddr = mm.alloc(ring_len * ctypes.sizeof(bdtype))
        return (vaddr, ring_len)

    def _init_tx_rings(self):
        mm = self.mm
        self.tx_ring_vaddr, self.tx_ring_len = self.__init_xx_ring(tg.sbd)
        self.tx_ring_paddr = mm.get_paddr(self.tx_ring_vaddr)
        self._tx_pi = 0

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


    def _init_rx_rings(self):
        dev = self.dev
        mm = self.mm

        dev.rdi.mini_rcb.disable_ring = 1
        print "[+] mini receive producer ring disabled"

        self.rx_ring_vaddr, self.rx_ring_len = self.__init_xx_ring(tg.rbd)
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

    def _init_rr_rings(self):
        dev = self.dev
        mm = self.mm

        ring_vaddr, self.rr_rings_len = self.__init_xx_ring(tg.rbd)
        self.rr_rings_vaddr = [ring_vaddr]
        
        print "[+] receive return ring 0 of size %d allocated at %x" % (self.rr_rings_len, ring_vaddr)

        for i in range(1, len(dev.mem.rxrcb)):
            ring_vaddr, tmp = self.__init_xx_ring(tg.rbd)
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

    def _populate_rx_ring(self, count = None):
        if count == None:
            count = self.rx_ring_len - 1
        assert count < self.rx_ring_len
        mm = self.mm
        r = ctypes.cast(self.rx_ring_vaddr, ctypes.POINTER(tg.rbd))
        self.rx_ring_bds = r
        self.rx_ring_buffers = []
        for i in range(self.rx_ring_len):
            buf = mm.alloc(0x600)
            self.rx_ring_buffers += [buf]

            pbuf = mm.get_paddr(buf)
            r[i].addr_hi = pbuf >> 32
            r[i].addr_low = pbuf & 0xffffffff
            r[i].index = i
            r[i].length = 0x600
            r[i].flags.disabled = 0

        print "[+] produced %d rx buffers" % self.rx_ring_len
        self.dev.hpmb.box[tg.mb_rbd_standard_producer].low = count
        self._std_rbd_pi = count
        self._std_rbd_ci = 0

    def _device_setup(self):
        dev = self.dev
        mm = self.mm
        dev.drv = self
	print "[+] initializing device"
        dev.init()
        print "[+] resetting device"
        dev.reset()
        sleep(0.5)

        if dev.pci.misc_host_ctrl.enable_tagged_status_mode == 0:
            print "[+] enabling tagged status mode"
            dev.pci.misc_host_ctrl.enable_tagged_status_mode = 1

        dma_wmm = 0x6
        if dev.config.caps['pcie'].max_payload_size > 0:
            dma_wmm += 0x1

        if dev.pci.dma_rw_ctrl.dma_write_watermark != dma_wmm:
            print "[+] configuring dma write watermark"
            dev.pci.dma_rw_ctrl.dma_write_watermark = dma_wmm

        if not dev.pci.dma_rw_ctrl.disable_cache_alignment:
            print "[+] disabling pci dma alignment"
            dev.pci.dma_rw_ctrl.disable_cache_alignment = 1

        if dev.msi.mode.msix_multi_vector_mode:
            print "[+] disabling multi vector mode"
            dev.msi.mode.msix_multi_vector_mode = 0

        if not dev.grc.misc_local_control.interrupt_on_attention:
            print "[+] configuring interrupts on grc attention"
            dev.grc.misc_local_control.interrupt_on_attention = 1

        if not dev.grc.misc_local_control.auto_seeprom:
            print "[+] configuring automatic eeprom access mode"
            dev.grc.misc_local_control.auto_seeprom = 1

        if not dev.grc.misc_config.timer_prescaler == 0x41:
            print "[+] configuring grc timer prescaler"
            dev.grc.misc_config.timer_prescaler = 0x41

        if not dev.grc.mode.host_send_bds:
            print "[+] enabling host send bds"
            self.dev.grc.mode.send_no_pseudo_header_cksum = 1
            self.dev.grc.mode.host_send_bds = 1

        if not dev.grc.mode.host_stack_up:
            print "[+] setting host stack up"
            dev.grc.mode.host_stack_up = 1

        if dev.bufman.dma_mbuf_low_watermark.count != 0x2a:
            print "[+] setting dma mbuf low watermark"
            dev.bufman.dma_mbuf_low_watermark.count = 0x2a

        if dev.bufman.mbuf_high_watermark.count != 0xa0:
            print "[+] setting mbuf high watermark"
            dev.bufman.mbuf_high_watermark.count = 0xa0

        if dev.emac.low_watermark_max_receive_frame.count != 1:
            print "[+] configuring dma low watermark flow control"
            dev.emac.low_watermark_max_receive_frame.count = 1
        
        dev.bufman.mode.attention_enable = 1
        dev.bufman.block_enable()

        if dev.rbdi.std_ring_replenish_threshold.count != 0x19:
            print "[+] configuring standard rx producer ring replenish threshold"
            dev.rbdi.std_ring_replenish_threshold.count = 0x19

        self._init_rx_rings()

        dev.hpmb.box[tg.mb_rbd_standard_producer].low = 0

        dev.rbdi.std_ring_replenish_watermark.count = 0x20

        self._init_tx_rings()
        dev.hpmb.box[tg.mb_sbd_host_producer].low = 0

        self._init_rr_rings()

        self.mac_addr = [getattr(dev.emac.addr[0], "byte_%d" % (i + 1)) for i in range(6)]

        print ("[+] device mac addr: %02x" + (":%02x" * 5)) % tuple(self.mac_addr)

        print "[+] configuring tx mac"
        dev.emac.tx_random_backoff = sum(self.mac_addr) & 0x3ff
        dev.emac.tx_mac_lengths.ipg = 0x6
        dev.emac.tx_mac_lengths.ipg_crs = 0x2
        dev.emac.tx_mac_lengths.slot = 0x20
       
        print "[+] configuring rx mac"
        dev.emac.rx_mtu = 1500
        dev.emac.rx_rules_conf.no_rules_matches_default_class = 2
    
        print "[+] configuring receive list placement"
        dev.rlp.config.default_interrupt_distribution_queue = 0
        dev.rlp.config.bad_frames_class = 1
        dev.rlp.config.number_of_active_lists = 0x10
        dev.rlp.config.number_of_lists_per_distribution_group = 1

        print "[+] enabling rx statistics"
        dev.rlp.stats_enable_mask.a1_silent_indication = 1
        dev.rlp.stats_enable_mask.cpu_mactq_priority_disable = 1
        dev.rlp.stats_enable_mask.enable_cos_stats = 1
        dev.rlp.stats_enable_mask.enable_indiscard_stats = 1
        dev.rlp.stats_enable_mask.enable_inerror_stats = 1
        dev.rlp.stats_enable_mask.enable_no_more_rbd_stats = 0
        dev.rlp.stats_enable_mask.perst_l = 1
        dev.rlp.stats_enable_mask.rc_return_ring_enable = 0
        dev.rlp.stats_enable_mask.rss_priority = 0
        assert dev.rlp.stats_enable_mask.word == 0x7bffff
        dev.rlp.stats_control.statistics_enable = 1
 
        print "[+] enabling tx statistics"
        dev.sdi.statistics_mask.counters_enable_mask = 1
        dev.sdi.statistics_control.faster_update = 1
        dev.sdi.statistics_control.statistics_enable = 1
        
        dev.hc.block_disable()
        print "[+] configuring host coalesence"

        dev.hc.mode.status_block_size = 2
        dev.hc.mode.clear_ticks_mode_on_rx = 1

        dev.hc.rx_coal_ticks = 0x48
        dev.hc.tx_coal_ticks = 0x14
        dev.hc.rx_max_coal_bds = 0x05
        dev.hc.tx_max_coal_bds = 0x35
        dev.hc.rc_max_coal_bds_in_int = 0x05
        dev.hc.tx_max_coal_bds_in_int = 0x05

        self.status_block_vaddr = mm.alloc(sizeof(tg.status_block))
        self.status_block = cast(self.status_block_vaddr, POINTER(tg.status_block))[0]

        self.status_block_paddr = mm.get_paddr(self.status_block_vaddr)
        
        dev.hc.status_block_host_addr_hi = self.status_block_paddr >> 32
        dev.hc.status_block_host_addr_low = self.status_block_paddr & 0xffffffff

        dev.hc.block_enable()

        dev.rbdc.mode.attention_enable = 1
        dev.rbdc.block_enable()

        dev.rlp.block_enable()

        if not dev.emac.mode.en_fhde:
            print "[+] enabling frame header dma engine"
            dev.emac.mode.en_fhde = 1

        if not dev.emac.mode.en_rde:
            print "[+] enabling receive dma engine"
            dev.emac.mode.en_rde = 1

        if not dev.emac.mode.en_tde:
            print "[+] enabling transmit dma engine"
            dev.emac.mode.en_tde = 1

        print "[+] clearing rx statistics"
        dev.emac.mode.clear_rx_statistics = 1

        print "[+] clearing tx statistics"
        dev.emac.mode.clear_tx_statistics = 1

        while dev.emac.mode.clear_rx_statistics:
            pass

        while dev.emac.mode.clear_tx_statistics:
            pass

        if not dev.emac.mode.en_rx_statistics:
            print "[+] enabling rx statistics"
            dev.emac.mode.en_rx_statistics = 1

        if not dev.emac.mode.en_tx_statistics:
            print "[+] enabling tx statistics"
            dev.emac.mode.en_tx_statistics = 1

        if not dev.emac.event_enable.link_state_changed:
            print "[+] enabling emac attention on link statue changed"
            dev.emac.event_enable.link_state_changed = 1

        if not dev.grc.mode.int_on_mac_attn:
            print "[+] enabling interrupt on mac attention"
            dev.grc.mode.int_on_mac_attn = 1

        print "[+] configuringing write dma engine"
        dev.wdma.mode.write_dma_pci_target_abort_attention_enable = 1
        dev.wdma.mode.write_dma_pci_master_abort_attention_enable = 1
        dev.wdma.mode.write_dma_pci_parity_attention_enable = 1
        dev.wdma.mode.write_dma_pci_host_address_overflow_attention_enable = 1
        dev.wdma.mode.write_dma_pci_fifo_overrun_attention_enable = 1
        dev.wdma.mode.write_dma_pci_fifo_underrun_attention_enable = 1
        dev.wdma.mode.write_dma_pci_fifo_overwrite_attention_enable = 1
        dev.wdma.mode.write_dma_local_memory = 1
        dev.wdma.mode.write_dma_pci_parity_error_attention_enable = 1
        dev.wdma.mode.write_dma_pci_host_address_overflow_error_attention_enable = 1
        dev.wdma.mode.status_tag_fix_enable = 1
        dev.wdma.mode.reserved2 = 0
        dev.wdma.block_enable()

        print "[+] configuring read dma engine"
        dev.rdma.mode.read_dma_pci_target_abort_attention_enable = 1
        dev.rdma.mode.read_dma_pci_master_abort_attention_enable = 1
        dev.rdma.mode.read_dma_pci_parity_error_attention_enable = 1
        dev.rdma.mode.read_dma_pci_host_address_overflow_error_attention_enable = 1
        dev.rdma.mode.read_dma_pci_fifo_overrun_attention_enable = 1
        dev.rdma.mode.read_dma_pci_fifo_underrun_attention_enable = 1
        dev.rdma.mode.read_dma_pci_fifo_overread_attention_enable = 1
        dev.rdma.mode.read_dma_local_memory_write_longer_than_dma_length_attention_enable = 1
        dev.rdma.mode.read_dma_pci_x_split_transaction_timeout_expired_attention_enable = 0
        dev.rdma.mode.bd_sbd_corruption_attn_enable = 0
        dev.rdma.mode.mbuf_rbd_corruption_attn_enable = 0
        dev.rdma.mode.mbuf_sbd_corruption_attn_enable = 0
        dev.rdma.mode.reserved3 = 0
        dev.rdma.mode.pci_request_burst_length = 3
        dev.rdma.mode.reserved2 = 0
        dev.rdma.mode.jumbo_2k_mmrr_mode = 1
        dev.rdma.mode.mmrr_disable = 0
        dev.rdma.mode.address_overflow_error_logging_enable = 0
        dev.rdma.mode.post_dma_debug_enable = 0
        dev.rdma.mode.hardware_ipv4_post_dma_processing_enable = 0
        dev.rdma.mode.hardware_ipv6_post_dma_processing_enable = 0
        dev.rdma.mode.in_band_vtag_enable = 0
        dev.rdma.mode.reserved = 0
        dev.rdma.block_enable()

        dev.rdc.mode.attention_enable = 1
        dev.rdc.block_enable()

        dev.sdc.block_enable()

        dev.sbdc.mode.attention_enable = 1
        dev.sbdc.block_enable()

        dev.rbdi.mode.receive_bds_available_on_disabled_rbd_ring_attn_enable = 1
        dev.rbdi.block_enable()

        dev.rdi.mode.illegal_return_ring_size = 1
        dev.rdi.block_enable()

        dev.sdi.mode.multiple_segment_enable = 0
        dev.sdi.mode.hardware_pre_dma_enable = 0
        dev.sdi.block_enable()

        dev.sbdi.mode.attention_enable = 1
        dev.sbdi.block_enable()

        dev.sbds.mode.attention_enable = 1
        dev.sbds.block_enable()

        self._populate_rx_ring()

        print "[+] enabling transmit mac"
        dev.emac.tx_mac_mode.enable_bad_txmbuf_lockup_fix = 1
        dev.emac.tx_mac_mode.enable_flow_control = 1
        dev.emac.tx_mac_mode.enable = 1
        
        usleep(100)

        print "[+] enabling receive mac"
        #dev.emac.mac_hash_0 = 0xffffffff
        #dev.emac.mac_hash_1 = 0xffffffff
        #dev.emac.mac_hash_2 = 0xffffffff
        #dev.emac.mac_hash_3 = 0xffffffff
        dev.emac.rx_mac_mode.promiscuous_mode = 1
        dev.emac.rx_mac_mode.accept_runts = 1
        #dev.emac.rx_mac_mode.enable_flow_control = 1
        dev.emac.rx_mac_mode.rss_enable = 1
        #dev.emac.rx_mac_mode.rss_ipv4_hash_enable = 1
        #dev.emac.rx_mac_mode.rss_tcpipv4_hash_enable = 1
        #dev.emac.rx_mac_mode.rss_ipv6_hash_enable = 1
        #dev.emac.rx_mac_mode.rss_tcpipv6_hash_enable = 1
        dev.emac.rx_mac_mode.enable = 1

        usleep(100)

        print "[+] configuring led"
        dev.emac.led_control.word = 0x800

        dev.emac.low_watermark_max_receive_frames = 1

    def _link_detect(self):
        print "[+] detecting link"
        res = self.dev.gphy.autonegotiate()
        if not res & 0x8000:
            print "[-] no link detected"
            self._set_tapdev_status(False)
            self._hcd = 0
        else:
            hcd = (res & 0x700) >> 8
            self._hcd = hcd
            if (hcd & 0x6) == 6:
                txpause = self.dev.gphy.may_send_pause()
                rxpause = self.dev.gphy.may_recv_pause()
                if hcd & 1:
                    print "[+] full duplex gige link negotated (res: %08x, txpause: %s, rxpause: %s)" % (res, txpause, rxpause)
                    self.dev.emac.mode.half_duplex = 1
                else:
                    print "[+] half duplex gige link negotated (res: %08x, txpause: %s, rxpause: %s)" % (res, txpause, rxpause)
                    self.dev.emac.mode.half_duplex = 0

                self.dev.emac.mode.port_mode = 2

                self.dev.emac.rx_mac_mode.enable_flow_control = 1 if rxpause else 0
                self.dev.emac.tx_mac_mode.enable_flow_control = 1 if txpause else 0

            elif (hcd > 0):
                if hcd == 5:
                    print "[+] full duplex 100base-tx link negotiated"
                    self.dev.emac.mode.half_duplex = 0
                elif hcd == 4:
                    print "[+] 100base-t4 link negotiated"
                    self.dev.emac.mode.half_duplex = 0
                elif hcd == 3:
                    print "[+] half duplex 100base-tx link negotiated"
                    self.dev.emac.mode.half_duplex = 1
                elif hcd == 2:
                    print "[+] full duplex 10base-t link negotiated"
                    self.dev.emac.mode.half_duplex = 0
                elif hcd == 1:
                    print "[+] half duplex 10base-t link negotiated"
                    self.dev.emac.mode.half_duplex = 1

                self.dev.emac.mode.port_mode = 1

                self.dev.emac.rx_mac_mode.enable_flow_control = 0
                self.dev.emac.tx_mac_mode.enable_flow_control = 0

            else:
                raise Exception("autonegotiaton failed, hcd %x" % hcd)
            self._set_tapdev_status(True)
    

    def _handle_interrupt(self):
        dev = self.dev
        if verbose:
            print "[+] handling interrupt"
        
        _ = dev.hpmb.box[tg.mb_interrupt].low
        tag = 0

        while self.status_block.updated:
            tag = self.status_block.status_tag
            if verbose:
                print "[+] status tag %x" % tag
            tag = tag << 24

            self.status_block.updated = 0
            if verbose:
                print "[+] status block updated! link: %d, attention: %d" % (self.status_block.link_status, self.status_block.attention)

            if dev.emac.status.link_state_changed:
                self._link_detect()
                dev.emac.status.link_state_changed = 1
                
            for i in range(len(dev.mem.rxrcb)):
                pi = getattr(self.status_block, "rr%d_pi" % i)
                ci = self.rr_rings_ci[i]

                if pi != ci:
                    if verbose:
                        print "[+] rr %d: pi is %x, ci was %x," % (i, pi, ci),

                    if pi < ci:
                        count = self.rr_rings_len - ci 
                        count += pi
                    else:
                        count = pi - ci
                    
                    if verbose:
                        print "%d bds received" % count
                    rbds = ctypes.cast(self.rr_rings_vaddr[i], ctypes.POINTER(tg.rbd))
                    while count > 0:
                        ci += 1
                        if ci > self.rr_rings_len:
                            ci = 1
                        rbd = rbds[ci - 1]

                        if verbose:
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

                        buf = ctypes.cast(self.rx_ring_buffers[rbd.index], ctypes.POINTER(ctypes.c_char * rbd.length))[0]
                        
                        if sys_name == "Linux":
                            os.write(self.tfd, buf.raw)
                        else:
                            o = OVERLAPPED(hEvent = CreateEvent(None, True, False, None))
                            if verbose:
                                print "[!] attempting to write to the tap device"
                            if not WriteFile(self.tfd, buf.raw, rbd.length, None, pointer(o)):
                                err = WinError()
                                if err.winerror != ERROR_IO_PENDING:
                                    raise err
                                if WAIT_FAILED == WaitForSingleObject(o.hEvent, INFINITE):
                                    raise WinError()
                            CloseHandle(o.hEvent)

                        count -= 1

                    mb = getattr(tg, "mb_rbd_rr%d_consumer" % i)
                    dev.hpmb.box[mb].low = ci
                    self.rr_rings_ci[i] = ci
            
            new_ci = self.status_block.rpci
            old_ci = self._std_rbd_ci
            count = 0
            if new_ci != old_ci:
                if verbose:
                    print "[+] rbdp ci now %x, was %x" % (new_ci, old_ci)
                rbds = ctypes.cast(self.rx_ring_vaddr, ctypes.POINTER(tg.rbd))
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

                if verbose:
                    print "[+] moving std rbd pi to %x" % self._std_rbd_pi
                self.dev.hpmb.box[tg.mb_rbd_standard_producer].low = self._std_rbd_pi

            if verbose:
                print "[+] sbd ci: %x" % self.status_block.sbdci

        if verbose:
            print "[+] interrupt handling concluded"
        self.dev.hpmb.box[tg.mb_interrupt].low = tag
        _ = self.dev.hpmb.box[tg.mb_interrupt].low

    def send(self, data, flags=None):
        if len(data) < 64:
            data = data + ('\x00' * (64 - len(data)))
        b_vaddr = self.mm.alloc(len(data))
        b = ctypes.cast(b_vaddr, ctypes.POINTER(ctypes.c_char * len(data)))
        b[0] = (ctypes.c_char * len(data)).from_buffer_copy(data)
        
        self._send_b(b_vaddr, len(data), flags=flags)

    def _send_b(self, buf, buf_sz, flags=None):
        i = self._tx_pi
        if verbose:
            print "[+] sending buffer at %x len 0x%x using sbd #%d" % (buf, buf_sz, i)
        paddr = self.mm.get_paddr(buf)
        txb = ctypes.cast(self.tx_ring_vaddr, ctypes.POINTER(tg.sbd))
        txb[i].addr_hi = paddr >> 32
        txb[i].addr_low = paddr & 0xffffffff
        txb[i].length = buf_sz
        txb[i].flags.packet_end = 1
        if flags != None:
            for j in flags:
                setattr(txb[i].flags, j, 1)

        i += 1
        if i == self.tx_ring_len:
            i = 0

        self.dev.hpmb.box[tg.mb_sbd_host_producer].low = i
        _ = self.dev.hpmb.box[tg.mb_sbd_host_producer].low
        self._tx_pi = i
        if verbose:
            print "[+] host sbd pi now %x" % i

    def run(self):
        if sys_name == "Windows":
            tg_evt = IoctlAsync(IOCTL_TGWINK_PEND_INTR, self.dev.interface.cfgfd, 8)
            tap_evt = ReadAsync(self.tfd, 1518)
            events = (HANDLE * 2)(tg_evt.req.hEvent, tap_evt.req.hEvent)
            tg_is_ready = tg_evt.check
            tap_is_ready = tap_evt.check
            tg_evt.submit()
            def wait_for_something():
                res = WaitForMultipleObjects(2, cast(pointer(events), POINTER(c_void_p)), False, INFINITE)
                if WAIT_FAILED == res:
                    raise WinError()
            def get_serial():
                serial = cast(tg_evt.buffer, POINTER(c_uint64)).contents.value
                tg_evt.reset()
                return serial
            def get_packet():
                if verbose:
                    print "[!] getting a packet from tap device"
                length = tap_evt.req.InternalHigh
                pkt = self.mm.alloc(length)
                ctypes.memmove(pkt, tap_evt.buffer, length)
                tap_evt.reset()
                return (pkt, length)
            def _set_tapdev_status(self, connected):
                if verbose:
                    print "[!] setting tapdev status to %s" % ("up" if connected else "down")
                o = OVERLAPPED(hEvent = CreateEvent(None, True, False, None))
                try:
                    val = c_int32(1 if connected else 0)
                    if not DeviceIoControl(self.tfd, TAP_WIN_IOCTL_SET_MEDIA_STATUS, pointer(val), 4, pointer(val), 4, None, pointer(o)):
                        err = WinError()
                        if err.winerror == ERROR_IO_PENDING:
                            if WAIT_FAILED == WaitForSingleObject(o.hEvent, INFINITE):
                                raise WinError()
                        elif err.winerror == 0:
                            pass
                        else:
                            raise err
                    if connected:
                        tap_evt.submit()
                finally:
                    CloseHandle(o.hEvent)
            TapDriver._set_tapdev_status = _set_tapdev_status
        else:
            self.read_fds = [self.dev.interface.eventfd, self.tfd]
            self.ready = []
            def tg_is_ready():
                return (self.dev.interface.eventfd in self.ready) 
            def tap_is_ready():
                return (self.tfd in self.ready)
            def wait_for_something():
                self.ready, _, _ = select.select(self.read_fds, [], [])
            def get_serial():
                return struct.unpack("L", os.read(self.dev.interface.eventfd, 8))
            def get_packet():
                b = self.mm.alloc(0x800)
                l = c.read(self.tfd, b, 0x800)
                return (b, l)
            def _set_tapdev_status(self, connected):
                pass
            TapDriver._set_tapdev_status = _set_tapdev_status

        self._link_detect()
        self.dev.unmask_interrupts()
        print "[+] waiting for interrupts..."

        while True:
            wait_for_something()
            if tg_is_ready():
                serial = get_serial()
                print "handling interrupt with serial number %d" % serial
                self._handle_interrupt()
            if tap_is_ready():
                pkt, sz = get_packet()
                self._send_b(pkt, sz)
