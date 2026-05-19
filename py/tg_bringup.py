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

# The Tigon3 register bring-up shared by the tap/, _tap/ and _aiotap/
# drivers. The register pokes are identical across all three and purely
# synchronous (MMIO), so they live here once. Each driver keeps its own
# ring code and event loop, and drives bring-up in this order:
#   dev.init(); dev.reset()
#   configure_device(dev, drv)
#   <driver-specific ring setup>
#   enable_tx_mac(dev) / enable_rx_mac(dev)

import logging
from ctypes import sizeof, cast, POINTER

import tglib as tg

logger = logging.getLogger(__name__)


def prepare_block(block, registerflags, silent=False):
    bname = block.block_name
    for register in registerflags:
        flags = registerflags[register]
        oreg = getattr(block, register)
        if isinstance(flags, dict):
            for flag in flags:
                ival = flags[flag]
                if getattr(oreg, flag) != ival:
                    if not silent:
                        verb = "configuring" if ival > 1 else "setting" if ival else "clearing"
                        logger.debug("%s %s (%s.%s)", verb, flag.replace("_", " "),
                                     bname, register)
                    setattr(oreg, flag, ival)
        elif oreg != flags:
            if not silent:
                logger.debug("configuring %s.%s", bname, register)
            setattr(block, register, flags)


def read_mac_addr(dev):
    return [getattr(dev.emac.addr[0], "byte_%d" % (i + 1)) for i in range(6)]


def configure_device(dev, drv):
    '''The full Tigon3 register bring-up -- everything between dev.reset()
    and ring setup. Allocates the status block and stashes it, with the
    MAC address, on drv.'''
    mm = dev.interface.mm

    dma_wmm = 0x6
    try:
        if dev.config.caps['pcie'].max_payload_size > 0:
            dma_wmm += 0x1
    except KeyError:
        pass

    prepare_block(dev.pci, {
        'misc_host_ctrl': {'enable_tagged_status_mode': 1},
        'dma_rw_ctrl': {'dma_write_watermark': dma_wmm,
                        'disable_cache_alignment': 1},
    })

    prepare_block(dev.msi, {'mode': {'msix_multi_vector_mode': 0}})

    prepare_block(dev.grc, {
        'misc_local_control': {'interrupt_on_attention': 1, 'auto_seeprom': 1},
        'misc_config': {'timer_prescaler': 0x41},
        'mode': {'send_no_pseudo_header_cksum': 1, 'host_send_bds': 1,
                 'host_stack_up': 1},
    })

    prepare_block(dev.bufman, {
        'dma_mbuf_low_watermark': {'count': 0x2a},
        'mbuf_high_watermark': {'count': 0xa0},
        'mode': {'attention_enable': 1},
    })
    dev.bufman.block_enable()

    prepare_block(dev.rbdi, {
        'std_ring_replenish_threshold': {'count': 0x19},
        'std_ring_replenish_watermark': {'count': 0x20},
    })

    drv.mac_addr = read_mac_addr(dev)
    logger.info("ethernet mac addr: %02x:%02x:%02x:%02x:%02x:%02x",
                *drv.mac_addr)

    prepare_block(dev.emac, {
        'low_watermark_max_receive_frame': {'count': 1},
        'tx_mac_lengths': {'ipg': 0x6, 'ipg_crs': 0x2, 'slot': 0x20},
        # Default class for frames matching no receive rule. tglib's
        # struct receive_mac_rules_configuration is wrong: it places
        # no_rules_matches_default_class at bits 4:2, but the chip's field
        # is bits 7:3 (PG Table 23). So this value is shifted: writing 2
        # yields register 0x08, which the chip reads as class 1 -- exactly
        # tg3's RCV_RULE_CFG_DEFAULT_CLASS (0x08). Writing 1 would yield
        # 0x04 = class 0 = discard. Leave it 2 until include/emac.h is
        # fixed (field should be 5 bits at 7:3) and tglib regenerated.
        'rx_rules_conf': {'no_rules_matches_default_class': 2},
        'tx_random_backoff': sum(drv.mac_addr) & 0x3ff,
        'rx_mtu': 1500,
        'mode': {'en_fhde': 1, 'en_rde': 1, 'en_tde': 1,
                 'en_rx_statistics': 1, 'en_tx_statistics': 1},
        'event_enable': {'link_state_changed': 1},
    })

    # Disable every receive rule. The chip's rule checker classifies each
    # frame against these 8 rule slots before the no-rules default class
    # applies; left at their post-reset/bootcode state they hold leftover
    # rules that misclassify frames -- non-IP (ARP) gets dropped while IP
    # falls through to the default class. tg3 clears the whole rule array
    # at bring-up ("Initialize receive rules" in tg3.c). A zero control
    # word has the enable bit clear, so the rule is off.
    for i in range(len(dev.emac.rx_rule)):
        dev.emac.rx_rule[i].control.word = 0
        dev.emac.rx_rule[i].mask_value = 0

    prepare_block(dev.rlp, {
        'config': {'default_interrupt_distribution_queue': 0,
                   'bad_frames_class': 1,
                   'number_of_active_lists': 0x10,
                   'number_of_lists_per_distribution_group': 1},
        'stats_enable_mask': {'a1_silent_indication': 1,
                              'cpu_mactq_priority_disable': 1,
                              'enable_cos_stats': 1,
                              'enable_indiscard_stats': 1,
                              'enable_inerror_stats': 1,
                              'enable_no_more_rbd_stats': 0,
                              'perst_l': 1,
                              'rc_return_ring_enable': 0,
                              'rss_priority': 0},
        'stats_control': {'statistics_enable': 1},
    })

    prepare_block(dev.sdi, {
        'statistics_mask': {'counters_enable_mask': 1},
        'statistics_control': {'faster_update': 1, 'statistics_enable': 1},
    })

    drv.status_block_vaddr = mm.alloc(sizeof(tg.status_block))
    drv.status_block = cast(drv.status_block_vaddr, POINTER(tg.status_block))[0]
    drv.status_block_paddr = mm.get_paddr(drv.status_block_vaddr)

    dev.hc.block_disable()
    prepare_block(dev.hc, {
        'mode': {'status_block_size': 2, 'clear_ticks_mode_on_rx': 1},
        'rx_coal_ticks': 0x48,
        'tx_coal_ticks': 0x14,
        'rx_max_coal_bds': 0x05,
        'tx_max_coal_bds': 0x35,
        'rx_max_coal_bds_in_int': 0x05,
        'tx_max_coal_bds_in_int': 0x05,
        'status_block_host_addr_hi': drv.status_block_paddr >> 32,
        'status_block_host_addr_low': drv.status_block_paddr & 0xffffffff,
    })
    dev.hc.block_enable()

    dev.rbdc.mode.attention_enable = 1
    dev.rbdc.block_enable()

    dev.rlp.block_enable()

    # The statistics counters clear asynchronously; wait them out.
    dev.emac.mode.clear_rx_statistics = 1
    dev.emac.mode.clear_tx_statistics = 1
    while dev.emac.mode.clear_rx_statistics:
        pass
    while dev.emac.mode.clear_tx_statistics:
        pass

    prepare_block(dev.grc, {'mode': {'int_on_mac_attn': 1}})

    prepare_block(dev.wdma, {'mode': {
        'write_dma_pci_target_abort_attention_enable': 1,
        'write_dma_pci_master_abort_attention_enable': 1,
        'write_dma_pci_fifo_overrun_attention_enable': 1,
        'write_dma_pci_fifo_underrun_attention_enable': 1,
        'write_dma_pci_fifo_overwrite_attention_enable': 1,
        'write_dma_local_memory': 1,
        'write_dma_pci_parity_error_attention_enable': 1,
        'write_dma_pci_host_address_overflow_error_attention_enable': 1,
        'status_tag_fix_enable': 1,
        'reserved2': 0,
    }})
    dev.wdma.block_enable()

    prepare_block(dev.rdma, {'mode': {
        'read_dma_pci_target_abort_attention_enable': 1,
        'read_dma_pci_master_abort_attention_enable': 1,
        'read_dma_pci_parity_error_attention_enable': 1,
        'read_dma_pci_host_address_overflow_error_attention_enable': 1,
        'read_dma_pci_fifo_overrun_attention_enable': 1,
        'read_dma_pci_fifo_underrun_attention_enable': 1,
        'read_dma_pci_fifo_overread_attention_enable': 1,
        'read_dma_local_memory_write_longer_than_dma_length_attention_enable': 1,
        'read_dma_pci_x_split_transaction_timeout_expired_attention_enable': 0,
        'bd_sbd_corruption_attn_enable': 0,
        'mbuf_rbd_corruption_attn_enable': 0,
        'mbuf_sbd_corruption_attn_enable': 0,
        'reserved3': 0,
        'pci_request_burst_length': 3,
        'reserved2': 0,
        'jumbo_2k_mmrr_mode': 1,
        'mmrr_disable': 0,
        'address_overflow_error_logging_enable': 0,
        'post_dma_debug_enable': 0,
        'hardware_ipv4_post_dma_processing_enable': 0,
        'hardware_ipv6_post_dma_processing_enable': 0,
        'in_band_vtag_enable': 0,
        'reserved': 0,
    }})
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

    dev.emac.led_control.word = 0x800


def enable_tx_mac(dev):
    prepare_block(dev.emac, {'tx_mac_mode': {
        'enable_bad_txmbuf_lockup_fix': 1,
        'enable': 1,
    }})


def enable_rx_mac(dev):
    # RSS off. With RSS on, IP frames are hashed through the indirection
    # table to a return ring while non-IP frames (ARP) fall to the
    # rules/class path; the paths diverge and ARP never reaches a drained
    # ring (rr0_pi advances only for IP frames). With RSS off the chip
    # runs legacy: every frame type is classified by the rules and placed
    # in the single return ring the driver drains as rr0. The default
    # class (no_rules_matches_default_class in configure_device) must
    # stay at 2: non-discard and clear of the rlp bad_frames_class (1).
    prepare_block(dev.emac, {'rx_mac_mode': {
        'promiscuous_mode': 1,
        'accept_runts': 1,
        'rss_enable': 0,
        'enable': 1,
    }})
