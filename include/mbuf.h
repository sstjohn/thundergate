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

#ifndef _MBUF_H_
#define _MBUF_H_

#include "utypes.h"

struct mbuf_hdr {
#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
    u32 c           :1;
    u32 f           :1;
    u32 reserved    :7;
    u32 next_mbuf   :16;
    u32 length      :7;
#elif __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
    u32 length      :7;
    u32 next_mbuf   :16;
    u32 reserved    :7;
    u32 f           :1;
    u32 c           :1;
#else
#error unknown endianness
#endif
};

struct mbuf_frame_desc {
    u32 status_ctrl;

#if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
    u8 qids;
    u8 reserved;
    u16 len;

    u16 ip_hdr_start;
    u16 tcp_udp_hdr_start;

    u16 data_start;
    u16 vlan_id;

    u16 ip_checksum;
    u16 tcp_udp_checksum;

    u16 pseudo_checksum;
    u16 checksum_status;

    u16 rule_match;
    u8 rule_class;
    u8 rupt;

    u16 reserved2;
    u16 mbuf;
#elif __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
    u16 len;
    u8 reserved;
    u8 qids;

    u16 tcp_udp_hdr_start;
    u16 ip_hdr_start;

    u16 vlan_id;
    u16 data_start;

    u16 tcp_udp_checksum;
    u16 ip_checksum;

    u16 checksum_status;
    u16 pseudo_checksum;

    u8 rupt;
    u8 rule_class;
    u16 rule_match;

    u16 mbuf;
    u16 reserved2;
#else
#error unknown endianness
#endif
    u32 reserved3;

    u32 reserved4;
};

struct mbuf {
    struct mbuf_hdr hdr;
    u32 next_frame_ptr;
    union {
        struct mbuf_frame_desc frame;
	u32 word[30];
        u8 byte[120];
    } data;
};

#endif 
