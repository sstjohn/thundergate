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

#ifndef _BD_H_
#define _BD_H_

#include "../include/utypes.h"

struct sbd_flags {
    u16 l4_cksum_offload :1;
    u16 ip_cksum_offload :1;
    u16 packet_end :1;
    u16 jumbo_frame :1;
    u16 hdrlen_2 :1;
    u16 snap :1;
    u16 vlan_tag :1;
    u16 coalesce_now :1;
    u16 cpu_pre_dma :1;
    u16 cpu_post_dma :1;
    u16 hdrlen_3 :1;
    u16 hdrlen_4 :1;
    u16 hdrlen_5 :1;
    u16 hdrlen_6 :1;
    u16 hdrlen_7 :1;
    u16 no_crc :1;
};

struct sbd {
    u32 addr_hi;
    u32 addr_low;
    struct sbd_flags flags;
    u16 length;
    u16 vlan_tag;
    u16 reserved;
};

struct rbd_flags {
    union {
        struct {
            u16 is_ipv6 :1;
            u16 is_tcp :1;
            u16 l4_checksum_correct :1;
            u16 ip_checksum_correct :1;
            u16 reserved :1;
            u16 has_error :1;
            u16 rss_hash_type :3;
            u16 has_vlan_tag :1;
            u16 reserved2 :1;
            u16 reserved3 :1;
            u16 rss_hash_valid :1;
            u16 packet_end :1;
            u16 reserved4 :1;
            u16 reserved5 :1;
        };
        u16 word;
    };
};

struct rbd_error_flags {
    union {
        struct {
            u16 reserved1 :1;
            u16 reserved2 :1;
            u16 reserved3 :1;
            u16 reserved4 :1;
            u16 reserved5 :1;
            u16 reserved6 :1;
            u16 reserved7 :1;
            u16 giant_packet :1;
            u16 trunc_no_res :1;
            u16 len_less_64 :1;
            u16 mac_abort :1;
            u16 dribble_nibble :1;
            u16 phy_decode_error :1;
            u16 link_lost :1;
            u16 collision :1;
            u16 bad_crc :1;
        };
        u16 word;
    };
};

struct rbd {
    u32 addr_hi;
    u32 addr_low;
    u16 length;
    u16 index;
    u16 type;
    struct rbd_flags flags;
    u16 ip_cksum;
    u16 l4_cksum;
    struct rbd_error_flags error_flags;
    u16 vlan_tag;
    u32 rss_hash;
    u32 opaque;
};

struct rbd_ex {
    u32 addr1_hi;
    u32 addr1_low;
    u32 addr2_hi;
    u32 addr2_low;
    u32 addr3_hi;
    u32 addr3_low;
    u16 len1;
    u16 len2;
    u16 len3;
    u16 reserved;
    u32 addr0_hi;
    u32 addr0_low;
    u16 index;
    u16 len0;
    u16 type;
    u16 flats;
    u16 ip_cksum;
    u16 tcp_udp_cksum;
    u16 error_flags;
    u16 vlan_tag;
    u32 rss_hash;
    u32 opaque;
};

#endif
