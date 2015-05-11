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

#define set_and_wait(x) do { x = 1; while (!x); } while (0)

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

	while (!ma.mode.enable)
		ma.mode.enable = 1;
	while (!bufman.mode.enable)
		bufman.mode.enable = 1;
	while (!rdma.mode.enable)
		rdma.mode.enable = 1;
	while (!rbdi.mode.enable)
		rbdi.mode.enable = 1;

	u32 start = *timer;
	while (*timer >= start && *timer < (start + 100));

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

typedef void (*reply_t)(void *src, u32 len, u8 cmd);

void post_buf(void *_src, u32 len, u8 cmd)
{
	int i;

	if (len > 256)
		len = 256;

	u32 *src = (u32 *)_src;
	for (i = 0; i < len; i++)
		gencomm[i + 1] = *src++;

	gencomm[0] = 0x88b50000 | (cmd << 8);
}
	
void send_buf(void *_src, u32 len, u8 cmd)
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
    mb->data.word[13] = 0x88b50000 | (PROTO_VER << 8) | cmd;

    u32 *src = (u32 *)_src;
    i = 4;
    while (i < 20 && (i - 4) < len)
	    mb->data.word[10 + i++] = *src++;

    while (i < 20)
        mb->data.word[10 + i++] = 0;

    ftq.mac_tx.q.word = (buf << 16) | buf;
}

int handle(reply_t reply, u8 cmd, u32 arg1, u32 arg2)
{
    u64 data;
    u32 *data_hi, *data_low;

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

        default:
	    (*reply)(&arg1, 2, 0xff);
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

void dev_init() 
{
    set_and_wait(ma.mode.enable);
    set_and_wait(bufman.mode.enable);

    grc.rxcpu_event.word = 0xffffffff;
    grc.rxcpu_event.word = 0;

    grc.rxcpu_event_enable.word = 0;    
    grc.rxcpu_event_enable.emac = 1;
    grc.misc_config.gphy_keep_power_during_reset = 1;

    ftq.reset.word = 0xffffffff;
    ftq.reset.word = 0;
    while (ftq.reset.word);

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

    set_and_wait(emac.tx_mac_mode.enable);
    set_and_wait(emac.rx_mac_mode.enable);

    set_and_wait(wdma.mode.enable);
    set_and_wait(rdma.mode.enable);

    mac_cpy((void *)0xc0000412, my_mac);
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
        if (grc.rxcpu_event.timer) {
            send_buf(test_buf, 13, 0);
	    reset_timer();
        }
	if (grc.rxcpu_event.emac) {
		check_link();
	}
	if (grc.rxcpu_event.rdiq) {
	    if (ftq.rdiq.peek.valid == 1 && ftq.rdiq.peek.pass == 0) {
		u32 mbuf = ftq.rdiq.peek.head_rxmbuf_ptr;

		if (0x88b5 != (rxmbuf[mbuf].data.word[13] >> 16)) {
			ftq.rdiq.peek.pass = 1;
		} else { 
			u32 mbufs = ftq.rdiq.peek.word & 0x3ffff;
			u32 tmp = rxmbuf[mbuf].data.word[13];
			u8 ver = (tmp & 0xff00) >> 8;
			u8 cmd = tmp & 0xff;
			u32 arg1 = rxmbuf[mbuf].data.word[14];
			u32 arg2 = rxmbuf[mbuf].data.word[15];

			mac_cpy(((u8 *)&rxmbuf[mbuf].data.word[11]) + 2, remote_mac);
			
			ftq.rdiq.peek.skip = 1;
			
			ftq.mbuf_clust_free.q.word = mbufs;
			
			handle(send_buf, cmd, arg1, arg2);
		}
	    }
	    grc.rxcpu_event.rdiq = 0;
	}
	if ((gencomm[0] >> 16) == 0x88b5) {
		if (!(gencomm[0] & 0xff00)) {
			u8 cmd = gencomm[0] & 0xff;
			u32 arg1 = gencomm[1];
			u32 arg2 = gencomm[2];

			handle(post_buf, cmd, arg1, arg2);
		}
	}
    } 

    return 0;
}
