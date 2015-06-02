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

#include "map.h"
#include "mbuf.h"
#include "mbox.h"
#include "rdi.h"
#include "proto.h"
#include "utypes.h"


#define GATE_BASE_GCW 0xc

#define set_and_wait(x) do { x = 1; while (!x); } while (0)
#define wait(x) do { \
			u32 start = *timer; \
			while (*timer >= start && *timer < (start + x)); \
		} while (0)
	
char *test_buf = "aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz";

u8 my_mac[6] = { 0 };
u8 remote_mac[6] = { 0xff, 0xff, 0xff, 0xff, 0xff, 0xff };

void mac_cpy(const u8 *src, u8 *dst)
{
	for (int i = 0; i < 6; i++)
		dst[i] = src[i];
}

void dma_read_qword(u32 addr_hi, u32 addr_low, u32 *data_hi, u32 *data_low)
{
	volatile u32 *timer = &grc.timer;

	while (rbdi.mode.enable)
		rbdi.mode.enable = 0;

	lpmb.box[mb_rbd_standard_producer].low = 0;

	rbdi.mode.reset = 1;
	while (rbdi.mode.reset);

	rdi.std_rcb.host_addr_hi = addr_hi;
	rdi.std_rcb.host_addr_low = addr_low;
	rdi.std_rcb.ring_size = 0x200;
	rdi.std_rcb.max_frame_len = 0;
	rdi.std_rcb.nic_addr = 0x6000;
	rdi.std_rcb.disable_ring = 0;
	
	lpmb.box[mb_rbd_standard_producer].low = 1;

    	pci.command.bus_master = 1;
	rdma.mode.enable = 1;
	rbdi.mode.enable = 1;

	wait(100);

	*data_hi = *((u32 *)0x6000);
	*data_low = *((u32 *)0x6004);	
}

u32 local_read_dword(u32 addr)
{
	u32 *p = (u32 *)addr;
	return *p;
}

void local_write_dword(u32 addr, u32 val)
{
	u32 *p = (u32 *)addr;
	*p = val;
}

typedef void (*reply_t)(void *src, u32 len, u16 cmd);

void post_buf(void *_src, u32 len, u16 cmd)
{
	int i;

	if (len > 256)
		len = 256;

	u32 *src = (u32 *)_src;
	for (i = 0; i < len; i++)
		gencomm[i + GATE_BASE_GCW + 1] = *src++;

	gencomm[GATE_BASE_GCW] = 0x88b50000 | cmd;
}
	
void send_buf(void *_src, u32 len, u16 cmd)
{
    int i;
    u32 buf = 0xad;
    struct mbuf *mb = (struct mbuf *)(0x8000 + (buf << 7));

    mb->hdr.c = 0;
    mb->hdr.f = 1;
    mb->hdr.length = 80;
    mb->next_frame_ptr = 0;
    mb->hdr.next_mbuf = buf + 1;

    mb->data.frame.status_ctrl = 0;
    
    mb->data.frame.len = 80;
    mb->data.frame.qids = 0xc;
    
    mb->data.frame.mbuf = 1;

    mac_cpy(remote_mac, (u8 *)(&mb->data.word[10]));
    mac_cpy(my_mac, ((u8 *)&mb->data.word[11]) + 2);
    mb->data.word[13] = 0x88b50000 | cmd;

    u32 *src = (u32 *)_src;
    i = 4;
    while (i < 20 && (i - 4) < len)
	    mb->data.word[10 + i++] = *src++;

    while (i < 20)
        mb->data.word[10 + i++] = 0;

    ftq.mac_tx.q.word = (buf << 16) | buf;
}

void send_msi(u32 addr_hi, u32 addr_low, u32 data)
{
    pci.msi_upper_address = addr_hi;
    pci.msi_lower_address = addr_low;
    pci.msi_data = data;
    msi.mode.msi_message = 0;

    pci.command.bus_master = 1;
    pci.msi_cap_hdr.msi_enable = 1;
    msi.mode.enable = 1;
    msi.status.msi_pci_request = 1;
}

u32 read_nvram(u32 ofs)
{
	u32 r;

	nvram.sw_arb.req_set0 = 1;
	while (!nvram.sw_arb.arb_won0);
	nvram.access.enable = 1;

	nvram.data_address = ofs;

	nvram.command.last = 1;
	nvram.command.first = 1;
	nvram.command.erase = 0;
	nvram.command.wr = 0;
	nvram.command.doit = 1;

	while (!nvram.command.done);
	r = nvram.read_data;

	nvram.access.enable = 0;
	nvram.sw_arb.req_clr0 = 1;

	return r;
}

void write_nvram(u32 ofs, u32 val)
{
	nvram.sw_arb.req_set0 = 1;
	while (!nvram.sw_arb.arb_won0);
	
	nvram.access.enable = 1;
	nvram.access.write_enable = 1;
	
	nvram.data_address = ofs;
	nvram.write_data = val;

	nvram.command.last = 1;
	nvram.command.first = 1;
	nvram.command.erase = 0;
	nvram.command.wr = 1;
	nvram.command.doit = 1;

	while (!nvram.command.done);

	nvram.access.write_enable = 1;
	nvram.access.enable = 0;
	nvram.sw_arb.req_clr0 = 1;
}

void cap_ctrl(u32 cap, u32 enabled)
{
	u32 mask = 0;
	
	if (cap & CAP_POWER_MANAGEMENT)
		mask |= 0x8;
	if (cap & CAP_VPD)
		mask |= 0x4;
	if (cap & CAP_MSI)
		mask |= 0x2;
	if (cap & CAP_MSIX)
		mask |= 0x1;

	u32 tmp = reg[0x6440 >> 2];
	if (enabled)
		tmp |= mask;
	else
		tmp &= ~mask;
	reg[0x6440 >> 2] = tmp;
}

void hide_func(u32 func, u32 hidden)
{
    u32 mask = (1 << (func - 1)) & 7;
    u32 val = cpmu.control.hide_pcie_function;
    if (hidden)
	val |= mask;
    else
        val &= ~mask;
    cpmu.control.hide_pcie_function = val;
}

void pme_assert()
{
	if (!pci.pm_ctrl_status.pme_enable)
		pci.pm_ctrl_status.pme_enable = 1;
	grc.misc_local_control.pme_assert = 1;
}

int handle(reply_t reply, u16 cmd, u32 arg1, u32 arg2, u32 arg3)
{
    u64 data;
    u32 *data_hi, *data_low;
    u32 tmp;

    switch(cmd) {
        case PING_CMD:
	    (*reply)(0, 0, PING_REPLY);
            break;

	case READ_LOCAL_CMD:
	    (*reply)((void *)arg1, arg2, READ_LOCAL_REPLY);
	    break;

	case WRITE_LOCAL_CMD:
	    local_write_dword(arg1, arg2);
	    (*reply)(0, 0, WRITE_LOCAL_ACK);
	    break;

        case READ_DMA_CMD:
	    data_hi = (u32 *)&data;
	    data_low = data_hi + 1;

            dma_read_qword(arg1, arg2, data_hi, data_low);
            (*reply)(&data, 2, READ_DMA_REPLY);
            break;

	case SEND_MSI_CMD:
	    send_msi(arg1, arg2, arg3);
	    (*reply)(0, 0, SEND_MSI_ACK);
	    break;

	case CAP_CTRL_CMD:
	    cap_ctrl(arg1, arg2);
	    (*reply)(0, 0, CAP_CTRL_ACK);
            break;

	case HIDE_FUNC_CMD:
	    hide_func(arg1, arg2);
	    (*reply)(0, 0, HIDE_FUNC_ACK);
	    break;

	case PME_ASSERT_CMD:
	    pme_assert();
	    (*reply)(0, 0, PME_ASSERT_ACK);
	    break;

	case READ_NVRAM_CMD:
	    tmp = read_nvram(arg1);
            (*reply)(&tmp, 1, READ_NVRAM_ACK);
	    break;

	case WRITE_NVRAM_CMD:
	    write_nvram(arg1, arg2);
	    (*reply)(0, 0, WRITE_NVRAM_ACK);
	    break;

        default:
	    (*reply)(&arg1, 2, ERROR_REPLY);
            break;
    }
}

void setup_rx_rules() 
{
    emac.rx_rule[7].control.enable = 0;
    while (emac.rx_rule[7].control.enable);

    emac.rx_rule[7].control.word = 0;

    emac.rx_rule[7].control.offset = 12;
    emac.rx_rule[7].control.mask = 1;
    emac.rx_rule[7].control.activate_rxcpu = 1;
    emac.rx_rule[7].control.pclass = 1;

    emac.rx_rule[7].mask_value = 0xffff88b5;

    emac.rx_rule[7].control.enable = 1;
    while (!emac.rx_rule[7].control.enable);

    rlp.mode.enable = 1;
    grc.rxcpu_event_enable.rdiq = 1;
}

void reset_timer()
{
    grc.rxcpu_event.timer = 0;
    grc.rxcpu_timer_reference = grc.timer + 1000000;
    grc.rxcpu_event_enable.timer = 1;
}

void nv_load_mac(u8 *mac)
{
    u64 tmp;

    while (nvram.auto_sense_status.busy);
    nvram.sw_arb.req_set0 = 1;
    while (!nvram.sw_arb.arb_won0);
    nvram.access.enable = 1;

    nvram.command.wr = 0;
    nvram.command.erase = 0;
    nvram.command.first = 1;
    nvram.command.last = 1;

    nvram.data_address = 0x7c;
    nvram.command.doit = 1;
    while (!nvram.command.done);

    tmp = nvram.read_data;
    tmp <<= 32;

    nvram.command.done = 1;

    nvram.data_address = 0x80;
    nvram.command.doit = 1;
    while (!nvram.command.done);
    tmp |= nvram.read_data;

    nvram.access.enable = 0;
    nvram.sw_arb.req_clr0 = 1;

    for (int i = 5; i >= 0; i--) {
	mac[i] = tmp & 0xff;
	tmp >>= 8;
    }
}

void dev_init() 
{
    set_and_wait(ma.mode.enable);
    set_and_wait(bufman.mode.enable);
    
    grc.power_management_debug.perst_override = 1;

    grc.rxcpu_event.word = 0xffffffff;
    grc.rxcpu_event.word = 0;

    grc.rxcpu_event_enable.word = 0;    
    grc.rxcpu_event_enable.emac = 1;

    grc.misc_local_control.auto_seeprom = 1;
    grc.misc_config.gphy_keep_power_during_reset = 1;
    grc.misc_config.disable_grc_reset_on_pcie_block = 1;
    grc.misc_config.timer_prescaler = 0x7f;

    *((u32 *)0xc0006408) = 0x00010691;

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

    emac.tx_mac_lengths.slot = 0x20;
    emac.tx_mac_lengths.ipg_crs = 0x2;
    emac.tx_mac_lengths.ipg = 0x6;

    emac.mii_mode.enable_constant_mdc_clock_speed = 1;
    emac.mii_mode.phy_address = 1;
    emac.mii_mode.mii_clock_count = 0xb;

    set_and_wait(emac.tx_mac_mode.enable);
    set_and_wait(emac.rx_mac_mode.enable);

    set_and_wait(wdma.mode.enable);
    set_and_wait(rdma.mode.enable);

    nv_load_mac(my_mac);

    mac_cpy(my_mac, (void *)0xc0000412);

    gencomm[GATE_BASE_GCW] = 0x88b50000;

    if (gencomm[0] == 0x4b657654)
	gencomm[0] = ~0x4b657654;
}

u16 phy_read(u16 reg)
{
	emac.mii_communication.read_command = 1;
	emac.mii_communication.write_command = 0;
	emac.mii_communication.phy_addr = 1;
	emac.mii_communication.reg_addr = reg;
	emac.mii_communication.start_busy = 1;

	while (emac.mii_communication.start_busy);

	return emac.mii_communication.data;
}

void phy_write(u16 reg, u16 val)
{
	emac.mii_communication.read_command = 0;
	emac.mii_communication.write_command = 1;
	emac.mii_communication.phy_addr = 1;
	emac.mii_communication.reg_addr = reg;
	emac.mii_communication.data = val;
	emac.mii_communication.start_busy = 1;

	while (emac.mii_communication.start_busy);
}

void phy_reset()
{
	phy_write(0, 0x8000);

	while (phy_read(0) & 0x8000);
}

void phy_loopback_en()
{
	phy_write(0, 1 << 14);

	while(phy_read(1) & (1 << 4));
}

void phy_auto_mdix()
{
	u16 val;
	phy_write(0x18, 0x7007);
	
	val = phy_read(0x18);
	val |= (1 << 9) | (1 << 15);
	phy_write(0x18, val);

	val = phy_read(0x10);
	val &= ~(1 << 14);
	phy_write(0x10, val);
}

void phy_nego()
{
	u16 val = (1 << 11) | (1 << 10) | (1 << 8) | (1 << 7);
	val |= (1 << 6) | (1 << 5) | 1;
	phy_write(0x4, val);

	phy_write(0x9, 1 << 9);

	val = (1 << 12) | (1 << 9);
	phy_write(0, val);
	
	while (!(phy_read(1) & (1 << 5)));
}

void check_link()
{
	u16 res;

	if (grc.mode.host_stack_up)
		return;

	if (!emac.tx_mac_status.link_up) {
		emac.status.link_state_changed = 1;
		return;
	}

	phy_reset();
	phy_auto_mdix();
	phy_loopback_en();
	phy_nego();

	res = (phy_read(0x19) & 0x703);
	emac.rx_mac_mode.enable_flow_control = !!(res & 2);
	emac.tx_mac_mode.enable_flow_control = !!(res & 1);
	res >>= 8;
	if ((res & 6) == 6) {
		emac.mode.port_mode = 2;

		if (res & 1)
			emac.mode.half_duplex = 0;
		else
			emac.mode.half_duplex = 1;
		
	} else {
		emac.mode.port_mode = 1;

		if ((res == 3) || (res == 1))
			emac.mode.half_duplex = 1;
		else
			emac.mode.half_duplex = 0;
	}

	emac.status.link_state_changed = 1;
}

int app() 
{
    dev_init();

    check_link();

    setup_rx_rules();
    
    reset_timer();

    while (1) {
	if (grc.rxcpu_event.emac) {
		check_link();
	}
        if (grc.rxcpu_event.timer) {
            send_buf(test_buf, 13, 0);
	    reset_timer();
        }
	if (grc.rxcpu_event.rdiq) {
	    if (ftq.rdiq.peek.valid == 1 && ftq.rdiq.peek.pass == 0) {
		u32 mbuf = ftq.rdiq.peek.head_rxmbuf_ptr;

		if (0x88b5 != (rxmbuf[mbuf].data.word[13] >> 16)) {
			ftq.rdiq.peek.pass = 1;
		} else { 
			u32 mbufs = ftq.rdiq.peek.word & 0x3ffff;
			u32 tmp = rxmbuf[mbuf].data.word[13];
			u16 cmd = tmp & 0xffff;
			u32 arg1 = rxmbuf[mbuf].data.word[14];
			u32 arg2 = rxmbuf[mbuf].data.word[15];
			u32 arg3 = rxmbuf[mbuf].data.word[16];

			mac_cpy(((u8 *)&rxmbuf[mbuf].data.word[11]) + 2, remote_mac);

			ftq.rdiq.peek.skip = 1;
			
			ftq.mbuf_clust_free.q.word = mbufs;

			handle(send_buf, cmd, arg1, arg2, arg3);
		}
	    }
	    grc.rxcpu_event.rdiq = 0;
	}
	u32 gb = gencomm[GATE_BASE_GCW];
	if (((gb >> 15) == (0x88b5 << 1)) && (gb & 0x7fff)) {
		u32 arg1 = gencomm[GATE_BASE_GCW + 1];
		u32 arg2 = gencomm[GATE_BASE_GCW + 2];
		u32 arg3 = gencomm[GATE_BASE_GCW + 3];

		handle(post_buf, gb & 0xffff, arg1, arg2, arg3);
        }
    } 

    return 0;
}
