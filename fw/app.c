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

char *test_buf = 
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"0123456789012345678901234567890123456789012$";

u8 my_mac[6] = { 0 };
u8 broadcast_mac[6] = { 0xff, 0xff, 0xff, 0xff, 0xff, 0xff };
u8 remote_mac[6] = { 0 };

u8 *dest_mac = broadcast_mac;


void stall(u32 count)
{
    for (int i = count; i > 0; i--);
}

void wait(u32 count)
{
    volatile u32 *timer = &grc.timer;
    u32 start = *timer;
    u32 end;
    if (0xffffffff - count < start)
	end = 0xffffffff - count;
    else
	end = start + count;
    do {
        u32 now = *timer;
        if (end < start) {
            if ((now >= end) && (now < start))
	        break;
        } else {
            if (now >= end) 
	        break;
        } 
    } while (1);
}

void mac_cpy(const u8 *src, u8 *dst)
{
	for (int i = 0; i < 6; i++)
		dst[i] = src[i];
}

typedef void (*reply_t)(void *src, u32 len, u16 cmd);

void dma_read(u32 addr_hi, u32 addr_low, u32 length, reply_t reply)
{
	u32 bd_cnt = (7 + length) >> 3;

	rbdi.mode.reset = 1;
	rdma.mode.reset = 1;
	while (rbdi.mode.reset | rdma.mode.reset);

	lpmb.box[mb_rbd_standard_producer].low = 0;

	rdi.std_rcb.host_addr_hi = addr_hi;
	rdi.std_rcb.host_addr_low = addr_low;
	rdi.std_rcb.ring_size = 0x200;
	rdi.std_rcb.max_frame_len = 0;
	rdi.std_rcb.nic_addr = 0x6000;
	rdi.std_rcb.disable_ring = 0;

	rdma.mode.enable = 1;
	rbdi.mode.enable = 1;

	lpmb.box[mb_rbd_standard_producer].low = bd_cnt;


	(*reply)((void *)0x6000, length, READ_DMA_REPLY);
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
    int i = 0;
    u32 buf = 0xad;
    struct mbuf *mb = (struct mbuf *)(0x8000 + (buf << 7));
    u32 sub = buf << 16 | buf;

    u32 blen = len << 2;

    mb->hdr.c = blen > 80 ? 1 : 0;
    mb->hdr.f = 1;
    mb->hdr.length = 80;
    mb->next_frame_ptr = 0;
    mb->hdr.next_mbuf = buf + 1;

    mb->data.frame.status_ctrl = 0;
    
    mb->data.frame.len = (blen + 16) < 64 ? 64 : (blen + 16);
    mb->data.frame.qids = 0xc;
    
    mb->data.frame.mbuf = blen <= 80 ? 1 : (blen <= 200 ? 2 : 3);

    i = sizeof(mb->data.frame);
    mac_cpy(dest_mac, &mb->data.byte[i]);
    i += 6;
    mac_cpy(my_mac, &mb->data.byte[i]);
    i += 6;
    mb->data.word[i >> 2] = 0x88b50000 | cmd;
    i += 4;

    u8 *src = (u8 *)_src;
    for (; i < 120 && blen > 0; i++, blen--)
	    mb->data.byte[i] = *src++;

    while (i < 100)
	mb->data.byte[i++] = 0;

    if (blen > 0) {
	mb++;
	mb->hdr.c = 1;
	mb->hdr.f = 0;
	mb->hdr.length = blen > 120 ? 120 : blen;
	mb->hdr.next_mbuf = blen > 120 ? buf + 2 : 0;
	for (i = 0; i < 120 && blen > 0; i++, blen--)
		mb->data.byte[i] = *src++;
        sub++;
    }

    if (blen > 0) {
	mb++;
	mb->hdr.c = 1;
	mb->hdr.f = 0;
	mb->hdr.length = blen;
	mb->hdr.next_mbuf = 0;
	for (i = 0;  blen > 0; i++, blen--)
	    mb->data.byte[i] = *src++;
        sub++;
    }

    __sync_synchronize();

    ftq.mac_tx.q.word = sub;

    dest_mac = broadcast_mac;
}

void send_msi(u32 addr_hi, u32 addr_low, u32 data)
{
    pci.msi_upper_address = addr_hi;
    pci.msi_lower_address = addr_low;
    pci.msi_data = data;
    msi.mode.msi_message = 0;

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
	if (cap & CAP_POWER_MANAGEMENT)
		cfg_port.cap_ctrl.pm_en = !!enabled;
	if (cap & CAP_VPD)
		cfg_port.cap_ctrl.vpd_en = !!enabled;
	if (cap & CAP_MSI)
		cfg_port.cap_ctrl.msi_en = !!enabled;
	if (cap & CAP_MSIX)
		cfg_port.cap_ctrl.msix_en = !!enabled;
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

void handle(reply_t reply, u16 cmd, u32 arg1, u32 arg2, u32 arg3)
{
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
            dma_read(arg1, arg2, arg3, reply);
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

    cpmu.control.hide_pcie_function = 7;

    cpmu.megabit_policy.mac_clock_switch = 0;
    cpmu.link_aware_policy.mac_clock_switch = 0;
    cpmu.d0u_policy.mac_clock_switch = 0;
    cpmu.link_idle_policy.mac_clock_switch = 0;
 
    rxcpu.mode.icache_pref_en = 1;

    grc.rxcpu_event.word = 0xffffffff;
    grc.rxcpu_event.word = 0;

    grc.fastboot_pc.addr = 0x8008000;
    grc.fastboot_pc.enable = 1;

    grc.rxcpu_event_enable.word = 0;    
    grc.rxcpu_event_enable.emac = 1;

    grc.misc_config.timer_prescaler = 0x7f;
    
    grc.power_management_debug.perst_override = 1;
     
    while (nvram.auto_sense_status.busy);
    nvram.access.enable = 1;
    nvram.access.eprom_sda_oe_mode = 0;
    nvram.access.enable = 0;

    cfg_port.pci_id.word = 0x88b51682;
    cfg_port.pci_class.word = 0x00088000;
    
    cfg_port.bar_ctrl.rom_bar_sz = 0x6;
    grc.ofs_ec = read_nvram(0x1c);
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
            send_buf(test_buf, 76, 0);
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
			dest_mac = remote_mac;

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
