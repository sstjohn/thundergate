/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015  Saul St. John
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "fw.h"

struct gate_config config = {
	DEFAULT_FLAGS,
	DEFAULT_CTRL_ETYPE,
	DEFAULT_CLOAK_VID,
	DEFAULT_CLOAK_DID,
	DEFAULT_CLOAK_CC,
};

struct gate_state state = {
	0,
	{ 0 },
	{ 0xff, 0xff, 0xff, 0xff, 0xff, 0xff },
	{ 0 },
	state.broadcast_mac
};

void init() 
{
    set_and_wait(ma.mode.enable);
    set_and_wait(bufman.mode.enable);

    cpmu.control.hide_pcie_function = 7;

    cpmu.megabit_policy.mac_clock_switch = 0;
    cpmu.link_aware_policy.mac_clock_switch = 0;
    cpmu.d0u_policy.mac_clock_switch = 0;
    cpmu.link_idle_policy.mac_clock_switch = 0;
    cpmu.no_link_or_10mb_policy.mac_clock_switch = 0;

    rxcpu.mode.icache_pref_en = 1;

    grc.rxcpu_event.word = 0xffffffff;
    grc.rxcpu_event.word = 0;

    grc.fastboot_pc.addr = 0x8008000;
    grc.fastboot_pc.enable = 1;

    grc.rxcpu_event_enable.word = 0;    
    grc.rxcpu_event_enable.emac = 1;

    if (gencomm[0] == 0x4b657654)
	    state.flags |= HANDSHAKE_MAGIC_SEEN;
    else
	    state.flags &= ~HANDSHAKE_MAGIC_SEEN;

    grc.misc_config.timer_prescaler = 0x7f;
    
    grc.power_management_debug.perst_override = 1;
     
    if (config.flags & CLOAK_EN)
        cloak_engage();
        
    if (config.flags & LOCAL_CTRL) {
	    cfg_port.bar_ctrl.bar0_sz = 1;
	    lgate_setup();
    } else {
	    cfg_port.bar_ctrl.bar0_sz = 0;
    }    

    cfg_port.bar_ctrl.rom_bar_sz = 0x6;
    grc.exp_rom_addr.base = read_nvram(0x1c);
    if (config.flags & OPROM_EN)
    	pci.state.rom_enable = 1;    

    ftq.reset.word = 0xffffffff;
    ftq.reset.word = 0;
    while (ftq.reset.word);

    emac.mode.port_mode = 2;

    set_and_wait(emac.mode.en_fhde);
    set_and_wait(emac.mode.en_rde);
    set_and_wait(emac.mode.en_tde);

    emac.mode.magic_packet_detection = 1;
    emac.mode.keep_frame_in_wol = 1;

    emac.event_enable.link_state_changed = 1;

    emac.rx_mac_mode.promiscuous_mode = 1;

    emac.tx_mac_mode.enable_bad_txmbuf_lockup_fix = 1;
    emac.tx_mac_lengths.slot = 0x20;
    emac.tx_mac_lengths.ipg_crs = 0x2;
    emac.tx_mac_lengths.ipg = 0x6;

    emac.mii_mode.enable_constant_mdc_clock_speed = 1;
    emac.mii_mode.phy_address = 1;
    emac.mii_mode.mii_clock_count = 0xb;

    set_and_wait(emac.tx_mac_mode.enable);
    set_and_wait(emac.rx_mac_mode.enable);

    wdma.mode.write_dma_pci_target_abort_attention_enable = 1;
    wdma.mode.write_dma_pci_master_abort_attention_enable = 1;
    wdma.mode.write_dma_pci_parity_error_attention_enable = 1;
    wdma.mode.write_dma_pci_host_address_overflow_error_attention_enable = 1;
    wdma.mode.write_dma_pci_fifo_overrun_attention_enable = 1;
    wdma.mode.write_dma_pci_fifo_underrun_attention_enable = 1;
    wdma.mode.write_dma_pci_fifo_overwrite_attention_enable = 1; 	
    set_and_wait(wdma.mode.enable);
    
    rdma.mode.read_dma_pci_target_abort_attention_enable = 1;
    rdma.mode.read_dma_pci_master_abort_attention_enable = 1;
    rdma.mode.read_dma_pci_parity_error_attention_enable = 1;
    rdma.mode.read_dma_pci_host_address_overflow_error_attention_enable = 1;
    rdma.mode.read_dma_pci_fifo_overrun_attention_enable = 1;
    rdma.mode.read_dma_pci_fifo_underrun_attention_enable = 1;
    rdma.mode.read_dma_pci_fifo_overread_attention_enable = 1;
    rdma.mode.read_dma_local_memory_write_longer_than_dma_length_attention_enable = 1;
    rdma.mode.jumbo_2k_mmrr_mode = 1;
    rdma.mode.hardware_ipv6_post_dma_processing_enable = 0;
    rdma.mode.in_band_vtag_enable = 0;
    rdma.mode.post_dma_debug_enable = 1;
    set_and_wait(rdma.mode.enable);

    set_and_wait(hc.mode.enable);

    nv_load_mac(state.my_mac);

    mac_cpy(state.my_mac, (void *)0xc0000412);

    gencomm[0] = 0xb49a89ab;

    pci.command.bus_master = 1;

    if (config.flags & PEER_CTRL)
    	rx_setup();

    if (config.flags & BEACON_EN)
    	beacon();

    check_link();
    
    main();
}
