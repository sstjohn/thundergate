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

from ctypes import sizeof, cast, POINTER
import trollius as asyncio
from trollius import From, Return, coroutine
import logging
logger = logging.getLogger(__name__)

import tglib as tg
from ring import init_rr_rings, init_rx_rings, init_tx_rings, populate_rx_ring

msleep = lambda t: asyncio.sleep(t / 1000.0)

def prepare_block(block, registerflags, silent = False):
    bname = block.block_name
    for register in registerflags:
        flags = registerflags[register]
        oreg = getattr(block, register)
        if isinstance(flags, dict):
            for flag in flags:
                ival = flags[flag]
                cval = getattr(oreg, flag)
                if cval != ival:
                    if not silent:
                        if ival > 1:
                            verb = "configuring"
                        elif ival:
                            verb = "setting"
                        else:
                            verb = "clearing"
                        fname = flag.replace("_", " ")
                        logger.debug("%s %s (%s.%s)" % (verb, fname, bname, register))
                    setattr(oreg, flag, ival)
        elif oreg != flags:
            if not silent:
                logger.debug("configuring %s.%s" % (bname, register))
            setattr(block, register, flags)

@coroutine
def device_setup(self):
    dev = self.dev
    mm = self.mm
    dev.drv = self
    logger.info("initializing device")
    dev.init()
    logger.info("resetting device")
    dev.reset()
    yield From(msleep(0.5))
    
    dma_wmm = 0x6
    try:
        if dev.config.caps['pcie'].max_payload_size > 0:
            dma_wmm += 0x1
    except: pass
    
    pci_regflags = {
        'misc_host_ctrl': {
            'enable_tagged_status_mode': 1,
        },
        'dma_rw_ctrl': {
            'dma_write_watermark': dma_wmm,
            'disable_cache_alignment': 1,
        },
    }
    prepare_block(dev.pci, pci_regflags)

    msi_regflags = {
        'mode': {
            'msix_multi_vector_mode': 0,
        },
    }
    prepare_block(dev.msi, msi_regflags)

    grc_regflags = {
            'misc_local_control': {
                'interrupt_on_attention': 1,
                'auto_seeprom': 1,
            },
            'misc_config': {
                'timer_prescaler': 0x41,
            },
            'mode': {
                'send_no_pseudo_header_cksum': 1,
                'host_send_bds': 1,
                'host_stack_up': 1,
            },
    }
    prepare_block(dev.grc, grc_regflags)

    bufman_regflags = {
        'dma_mbuf_low_watermark': {
            'count': 0x2a,
        },
        'mbuf_high_watermark': {
            'count': 0xa0,
        },
        'mode': {
            'attention_enable': 1
        },
    }
    prepare_block(dev.bufman, bufman_regflags)
    dev.bufman.block_enable()
    
    rbdi_regflags = {
        'std_ring_replenish_threshold': {
            'count': 0x19,
        },
        'std_ring_replenish_watermark': {
            'count': 0x20,
        },
    }
    prepare_block(dev.rbdi, rbdi_regflags)

    self.mac_addr = [getattr(dev.emac.addr[0], "byte_%d" % (i + 1)) for i in range(6)]
    logger.info(("ethernet mac addr: %02x" + (":%02x" * 5)) % tuple(self.mac_addr))

    logger.info("configuring ethernet mac")
    emac_regflags = {
        'low_watermark_max_receive_frame': {
            'count': 1,
        },
        'tx_mac_lengths': {
            'ipg': 0x6,
            'ipg_crs': 0x2,
            'slot': 0x20,
        },
        'rx_rules_conf': {
            'no_rules_matches_default_class': 2,
        },
        'tx_random_backoff': sum(self.mac_addr) & 0x3ff,
        'rx_mtu': 1500,
    }
    prepare_block(dev.emac, emac_regflags)

    logger.info("configuring receive list placement")
    rlp_regflags = {
        'config': {
            'default_interrupt_distribution_queue': 0,
            'bad_frames_class': 1,
            'number_of_active_lists': 0x10,
            'number_of_lists_per_distribution_group': 1,
        },
        'stats_enable_mask': {
            'a1_silent_indication': 1,
            'cpu_mactq_priority_disable': 1,
            'enable_cos_stats': 1,
            'enable_indiscard_stats': 1,
            'enable_inerror_stats': 1,
            'enable_no_more_rbd_stats': 0,
            'perst_l': 1,
            'rc_return_ring_enable': 0,
            'rss_priority': 0,
        },
        'stats_control': {
            'statistics_enable': 1,
        },
    }
    prepare_block(dev.rlp, rlp_regflags)

    logger.info("enabling tx statistics")
    sdi_regflags = {
        'statistics_mask': {
            'counters_enable_mask': 1
        },
        'statistics_control': {
            'faster_update': 1,
            'statistics_enable': 1,
        },
    }
    prepare_block(dev.sdi, sdi_regflags)
    
    logger.info("allocating status block")
    self.status_block_vaddr = mm.alloc(sizeof(tg.status_block))
    self.status_block = cast(self.status_block_vaddr, POINTER(tg.status_block))[0]
    self.status_block_paddr = mm.get_paddr(self.status_block_vaddr)

    logger.info("configuring host coalesence")
    dev.hc.block_disable()
    hc_regflags = {
        'mode': {
            'status_block_size': 2,
            'clear_ticks_mode_on_rx': 1,
        },
        'rx_coal_ticks': 0x48,
        'tx_coal_ticks': 0x14,
        'rx_max_coal_bds': 0x05,
        'tx_max_coal_bds': 0x35,
        'rx_max_coal_bds_in_int': 0x05,
        'tx_max_coal_bds_in_int': 0x05,
        'status_block_host_addr_hi': self.status_block_paddr >> 32,
        'status_block_host_addr_low': self.status_block_paddr & 0xffffffff,
    }
    prepare_block(dev.hc, hc_regflags)
    dev.hc.block_enable()

    logger.info("enabling rbdc")
    dev.rbdc.mode.attention_enable = 1
    dev.rbdc.block_enable()

    logger.info("enabling rlp")
    dev.rlp.block_enable()

    logger.debug("clearing rx statistics")
    dev.emac.mode.clear_rx_statistics = 1

    logger.debug("clearing tx statistics")
    dev.emac.mode.clear_tx_statistics = 1

    while dev.emac.mode.clear_rx_statistics:
        pass

    while dev.emac.mode.clear_tx_statistics:
        pass

    logger.info("configuring emac")
    emac_regflags = {
        'mode': {
            'en_fhde': 1,
            'en_rde': 1,
            'en_tde': 1,
            'en_rx_statistics': 1,
            'en_tx_statistics': 1,
        },
        'event_enable': {
            'link_state_changed': 1,
        },
    }
    prepare_block(dev.emac, emac_regflags)

    logger.info("configuring grc")
    grc_regflags = {
        'mode': {
            'int_on_mac_attn': 1,
        },
    }
    prepare_block(dev.grc, grc_regflags)

    logger.info("configuringing write dma engine")
    wdma_regflags = {
        "mode": {
            "write_dma_pci_target_abort_attention_enable": 1,
            "write_dma_pci_master_abort_attention_enable": 1,
            "write_dma_pci_fifo_overrun_attention_enable": 1,
            "write_dma_pci_fifo_underrun_attention_enable": 1,
            "write_dma_pci_fifo_overwrite_attention_enable": 1,
            "write_dma_local_memory": 1,
            "write_dma_pci_parity_error_attention_enable": 1,
            "write_dma_pci_host_address_overflow_error_attention_enable": 1,
            "status_tag_fix_enable": 1,
            "reserved2": 0,
        },
    }
    prepare_block(dev.wdma, wdma_regflags)
    dev.wdma.block_enable()

    logger.info("configuring read dma engine")
    rdma_regflags = {
        "mode": {
            "read_dma_pci_target_abort_attention_enable": 1,
            "read_dma_pci_master_abort_attention_enable": 1,
            "read_dma_pci_parity_error_attention_enable": 1,
            "read_dma_pci_host_address_overflow_error_attention_enable": 1,
            "read_dma_pci_fifo_overrun_attention_enable": 1,
            "read_dma_pci_fifo_underrun_attention_enable": 1,
            "read_dma_pci_fifo_overread_attention_enable": 1,
            "read_dma_local_memory_write_longer_than_dma_length_attention_enable": 1,
            "read_dma_pci_x_split_transaction_timeout_expired_attention_enable": 0,
            "bd_sbd_corruption_attn_enable": 0,
            "mbuf_rbd_corruption_attn_enable": 0,
            "mbuf_sbd_corruption_attn_enable": 0,
            "reserved3": 0,
            "pci_request_burst_length": 3,
            "reserved2": 0,
            "jumbo_2k_mmrr_mode": 1,
            "mmrr_disable": 0,
            "address_overflow_error_logging_enable": 0,
            "post_dma_debug_enable": 0,
            "hardware_ipv4_post_dma_processing_enable": 0,
            "hardware_ipv6_post_dma_processing_enable": 0,
            "in_band_vtag_enable": 0,
            "reserved": 0,
        },
    }
    prepare_block(dev.rdma, rdma_regflags)
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

    print "[+] configuring led"
    dev.emac.led_control.word = 0x800

@coroutine
def _enable_tx_mac(self):
    logger.info("enabling transmit mac")
    dev.emac.tx_mac_mode.enable_bad_txmbuf_lockup_fix = 1
    #dev.emac.tx_mac_mode.enable_flow_control = 1
    dev.emac.tx_mac_mode.enable = 1
    
    yield From(msleep(100)) 

@coroutine
def _enable_rx_mac(self):
    logger.info("enabling receive mac")
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

    yield From(msleep(100))


    dev.emac.low_watermark_max_receive_frames = 1

@coroutine
def enable_rx(self):
    yield From(init_rx_rings(self))
    yield From(init_rr_rings(self))
    yield From(populate_rx_ring(self))
    yield From(_enable_rx_mac(self))

@coroutine
def enable_tx(self):
    yield From(init_tx_rings(self))
    yield From(_enable_tx_mac(self))
