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

#ifndef _TCP_SEG_CTRL_H_
#define _TCP_SEG_CTRL_H_

struct tsc_length_offset {
	u32 reserved23 :9;
	u32 mbuf_offset :7;
	u32 length :16;
};

struct tsc_dma_flags {
	u32 reserved20 :12;
	u32 mbuf_offset_valid :1;
	u32 last_fragment :1;
	u32 no_word_swap :1;
	u32 status_dma :1;
	u32 mac_source_addr_sel :2;
	u32 mac_source_addr_ins :1;
	u32 tcp_udp_cksum_en :1;
	u32 ip_cksum_en :1;
	u32 force_raw_cksum_en :1;
	u32 data_only :1;
	u32 header :1;
	u32 vlan_tag_present :1;
	u32 force_interrupt :1;
	u32 last_bd_in_frame :1;
	u32 coalesce_now :1;
	u32 mbuf :1;
	u32 invoke_processor :1;
	u32 dont_generate_crc :1;
	u32 no_byte_swap :1;
};

struct tsc_vlan_tag {
	u32 reserved16 :16;
	u32 vlan_tag :16;
};

struct tsc_pre_dma_cmd_xchng {
	u32 ready :1;
	u32 pass_bit :1;
	u32 skip :1;
	u32 unsupported_mss :1;
	u32 reserved7 :21;
	u32 bd_index :7;
};

struct tcp_seg_ctrl_regs {
    u32 lower_host_addr;
    u32 upper_host_addr;
    struct tsc_length_offset length_offset;
    struct tsc_dma_flags dma_flags;

    struct tsc_vlan_tag vlan_tag;
    struct tsc_pre_dma_cmd_xchng pre_dma_cmd_xchng;
};

#endif
