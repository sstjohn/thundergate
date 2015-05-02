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

#include <stdint.h>

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
	if (len > 256)
		len = 256;

	u32 *src = (u32 *)_src;
	for (int i = 0; i < len; i++)
		gencomm[i + 1] = *src++;

	gencomm[0] = 0x88b50000 | (cmd << 8);
}
	
void send_buf(void *_src, u32 len, u8 cmd)
{
    int i;
    u32 buf = 0xad;
    struct mbuf *mb = (struct mbuf *)(0x8000 + (buf << 7));

    mb->hdr.f = 1;
    mb->hdr.length = 80;
    mb->next_frame_ptr = 0;
    mb->hdr.next_mbuf = buf + 1;

    mb->data.frame.status_ctrl = 0;
    
    mb->data.frame.len = 80;
    mb->data.frame.qids = 0;
    
    mb->data.frame.ip_hdr_start = 0;
    mb->data.frame.tcp_udp_hdr_start = 0;

    mb->data.frame.data_start = 22;
    mb->data.frame.vlan_id = 0;

    mb->data.frame.ip_checksum = 0;
    mb->data.frame.tcp_udp_checksum = 0;

    mb->data.frame.rule_match = 0;
    mb->data.frame.rule_class = 0;
    mb->data.frame.rupt = 0;

    mb->data.frame.mbuf = buf;

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

    bufman.mode.attention_enable = 1;
    set_and_wait(bufman.mode.enable);

    ftq.reset.word = 0xffffffff;
    ftq.reset.word = 0;
    while (ftq.reset.word);

    set_and_wait(emac.mode.en_fhde);
    set_and_wait(emac.mode.en_rde);
    set_and_wait(emac.mode.en_tde);
    
    set_and_wait(wdma.mode.enable);

    //rdma.mode.word = 0x7fe;
    set_and_wait(rdma.mode.enable);

    rbdi.mode.receive_bds_available_on_disabled_rbd_ring_attn_enable = 1;
    set_and_wait(rbdi.mode.enable);
    
    set_and_wait(rbdc.mode.enable);

    rlp.mode.class_zero_attention_enable = 1;
    rlp.mode.mapping_out_of_range_attention_enable = 1;
    rlp.stats_enable_mask.rc_return_ring_enable = 1;
    set_and_wait(rlp.mode.enable);

    set_and_wait(rdi.mode.enable);

    rdc.mode.attention_enable = 1;
    set_and_wait(rdc.mode.enable);
   
    //set_and_wait(sdc.mode.enable);

    //sbdc.mode.attention_enable = 1;
    //set_and_wait(sbdc.mode.enable);

    //set_and_wait(sdi.mode.enable);

    //set_and_wait(sbdi.mode.enable);

    //set_and_wait(sbds.mode.enable);

    //emac.tx_mac_mode.enable_bad_txmbuf_lockup_fix = 1;
    set_and_wait(emac.tx_mac_mode.enable);

    set_and_wait(emac.rx_mac_mode.enable);

    my_mac[0] = emac.addr[0].byte_1;
    my_mac[1] = emac.addr[0].byte_2;
    my_mac[2] = emac.addr[0].byte_3;
    my_mac[3] = emac.addr[0].byte_4;
    my_mac[4] = emac.addr[0].byte_5;
    my_mac[5] = emac.addr[0].byte_6;

    grc.rxcpu_event.word = 0xffffffff;
    grc.rxcpu_event.word = 0;
}

int app() 
{
    dev_init();

    setup_rx_rules();
    reset_timer();

    while (1) {
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
			u8 ver = (tmp & 0xff00) >> 8;
			u8 cmd = tmp & 0xff;
			u32 arg1 = rxmbuf[mbuf].data.word[14];
			u32 arg2 = rxmbuf[mbuf].data.word[15];
			
			ftq.rdiq.peek.skip = 1;
			
			ftq.mbuf_clust_free.q.word = mbufs;
			
			handle(send_buf, cmd, arg1, arg2);
		}
	    }
	    grc.rxcpu_event.rdiq = 0;
	}
	if (gencomm[0] != 0x88b50000) {
		if (0x88b5 != (gencomm[0] >> 16)) {
			gencomm[0] = 0x88b50000;
		} else {
			if (!(gencomm[0] & 0xff00)) {
				u8 cmd = gencomm[0] & 0xff;
				u32 arg1 = gencomm[1];
				u32 arg2 = gencomm[2];

				handle(post_buf, cmd, arg1, arg2);
			}
		}
	}
    } 

    return 0;
}
