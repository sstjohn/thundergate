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
 * Public interface of the on-core TCP/IP stack.
 *
 * The stack runs entirely on the Tigon3 MIPS core, independent of the
 * host. It layers ARP / IPv4 / ICMP / UDP onto the firmware's existing
 * raw-Ethernet path: net_rx() is called from rx() for non-control frames,
 * and net_tx() emits a frame through the MAC transmit FTQ.
 */

#ifndef _NET_NET_H_
#define _NET_NET_H_

#include "utypes.h"

/* The local interface addressing, populated by net_init(). */
struct net_iface {
    u8 mac[6];
    u8 ip[4];
    u8 netmask[4];
    u8 gateway[4];
};

extern struct net_iface net_if;

/* A shared scratch buffer the protocol layers build outbound frames into.
 * The firmware event loop is single-threaded, so one buffer is enough.
 * 320 bytes is the largest frame the three-mbuf transmit path carries. */
#define NET_TX_MAX 320
extern u8 net_txbuf[NET_TX_MAX];

void net_init(void);

/* L2 ingress / egress. A "frame" is a complete Ethernet frame: 6-byte
 * destination, 6-byte source, 2-byte EtherType, then the payload. */
void net_rx(const u8 *frame, u32 len);
void net_tx(const u8 *frame, u32 len);

/* mac_cpy() is the firmware's 6-byte copy helper (defined in fw/util.c);
 * declared here so the protocol modules need not include all of fw.h. */
void mac_cpy(const u8 *src, u8 *dst);

/* Per-protocol ingress handlers; `frame` points at the Ethernet header. */
void arp_input(const u8 *frame, u32 len);
void ip_input(const u8 *frame, u32 len);

/* ARP cache: arp_lookup() returns a cached MAC (or 0), arp_request()
 * broadcasts a query, arp_cache_put() records an address pair. */
const u8 *arp_lookup(const u8 *ip);
void arp_request(const u8 *ip);
void arp_cache_put(const u8 *ip, const u8 *mac);

/* Upper-layer ingress, dispatched by ip_input(); `ip` points at the IPv4
 * header, `payload`/`plen` at the transport segment within it. */
void icmp_input(const u8 *ip, const u8 *payload, u32 plen);
void udp_input(const u8 *ip, const u8 *payload, u32 plen);

/* Build and transmit an IPv4 datagram. The transport segment -- already
 * complete, with its own header and checksum -- must already sit in
 * net_txbuf at offset NET_L4_OFF; `plen` is its length and `proto` an
 * IP_PROTO_* value. ip_output() resolves the next-hop MAC via ARP. */
#define NET_L4_OFF 34   /* past the 14-byte Ethernet + 20-byte IPv4 headers */
void ip_output(const u8 *dst_ip, u8 proto, u32 plen);

#endif
