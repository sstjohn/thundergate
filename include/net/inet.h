/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015-2026  Saul St. John
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

/*
 * Packet layouts for the on-core TCP/IP stack.
 *
 * The Tigon3 MIPS core is big-endian, so the multi-byte fields below are
 * already in network byte order -- no host/network swapping is needed.
 * Every header is __attribute__((packed)): there is no padding, and the
 * compiler is told the fields may be unaligned, so it byte-assembles any
 * access rather than emitting the lwl/lwr instructions the core lacks.
 *
 * IPv4 and MAC addresses are kept as byte arrays for the same reason --
 * a 4-byte array never forces an unaligned 32-bit load.
 */

#ifndef _NET_INET_H_
#define _NET_INET_H_

#include "utypes.h"

/* --- EtherTypes ----------------------------------------------------------- */
#define ETH_P_IP    0x0800
#define ETH_P_ARP   0x0806

#define ETH_ALEN    6   /* MAC address length */
#define IP_ALEN     4   /* IPv4 address length */

/* --- ARP (RFC 826) -------------------------------------------------------- */
#define ARP_HTYPE_ETHER  1
#define ARP_PTYPE_IP     ETH_P_IP
#define ARP_OP_REQUEST   1
#define ARP_OP_REPLY     2

struct arp_pkt {
    u16 htype;            /* hardware type: ARP_HTYPE_ETHER */
    u16 ptype;            /* protocol type: ARP_PTYPE_IP */
    u8  hlen;             /* hardware address length: ETH_ALEN */
    u8  plen;             /* protocol address length: IP_ALEN */
    u16 op;               /* ARP_OP_REQUEST / ARP_OP_REPLY */
    u8  sha[ETH_ALEN];    /* sender hardware address */
    u8  spa[IP_ALEN];     /* sender protocol (IPv4) address */
    u8  tha[ETH_ALEN];    /* target hardware address */
    u8  tpa[IP_ALEN];     /* target protocol address */
} __attribute__((packed));

/* --- IPv4 (RFC 791) ------------------------------------------------------- */
#define IP_PROTO_ICMP   1
#define IP_PROTO_UDP    17

#define IP_VERSION      4
#define IP_FRAG_MASK    0x3fff   /* fragment-offset + MF bits of frag_off */

struct ip_hdr {
    u8  ver_ihl;          /* version:4 (high nibble), IHL:4 (low nibble) */
    u8  tos;
    u16 total_len;        /* header + payload, in bytes */
    u16 id;
    u16 frag_off;         /* flags:3, fragment offset:13 */
    u8  ttl;
    u8  protocol;         /* IP_PROTO_* */
    u16 checksum;
    u8  src[IP_ALEN];
    u8  dst[IP_ALEN];
} __attribute__((packed));

#define IP_VER(h)   ((h)->ver_ihl >> 4)
#define IP_IHL(h)   ((h)->ver_ihl & 0x0f)   /* in 32-bit words */

/* --- ICMP (RFC 792) ------------------------------------------------------- */
#define ICMP_TYPE_ECHO_REPLY    0
#define ICMP_TYPE_ECHO_REQUEST  8

struct icmp_hdr {
    u8  type;             /* ICMP_TYPE_* */
    u8  code;
    u16 checksum;
    u16 id;               /* echo identifier */
    u16 seq;              /* echo sequence number */
} __attribute__((packed));

/* --- UDP (RFC 768) -------------------------------------------------------- */
struct udp_hdr {
    u16 src_port;
    u16 dst_port;
    u16 len;              /* header + payload, in bytes */
    u16 checksum;         /* 0 == not computed */
} __attribute__((packed));

#endif
