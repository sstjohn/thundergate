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
 * ARP (RFC 826): answer requests for our address, and keep a small cache
 * of address pairs so the IPv4 layer can resolve next-hop MACs.
 */

#include "fw.h"
#include "net/net.h"
#include "net/inet.h"

/* Power of two, so the round-robin replacement modulo is just a mask --
 * the Tigon3 core has no divide instruction. */
#define ARP_CACHE_SIZE 8

struct arp_entry {
    u8 ip[IP_ALEN];
    u8 mac[ETH_ALEN];
    u8 valid;
};

static struct arp_entry arp_cache[ARP_CACHE_SIZE];
static u32 arp_next;   /* next slot to overwrite when the cache is full */

static int ip_eq(const u8 *a, const u8 *b)
{
    return a[0] == b[0] && a[1] == b[1] && a[2] == b[2] && a[3] == b[3];
}

static void ip_cpy(const u8 *src, u8 *dst)
{
    dst[0] = src[0];
    dst[1] = src[1];
    dst[2] = src[2];
    dst[3] = src[3];
}

const u8 *arp_lookup(const u8 *ip)
{
    int i;

    for (i = 0; i < ARP_CACHE_SIZE; i++)
        if (arp_cache[i].valid && ip_eq(arp_cache[i].ip, ip))
            return arp_cache[i].mac;

    return 0;
}

void arp_cache_put(const u8 *ip, const u8 *mac)
{
    int i;

    /* refresh an existing entry if we already know this address */
    for (i = 0; i < ARP_CACHE_SIZE; i++) {
        if (arp_cache[i].valid && ip_eq(arp_cache[i].ip, ip)) {
            mac_cpy(mac, arp_cache[i].mac);
            return;
        }
    }

    /* otherwise claim the next slot, round-robin */
    i = arp_next;
    arp_next = (arp_next + 1) % ARP_CACHE_SIZE;
    ip_cpy(ip, arp_cache[i].ip);
    mac_cpy(mac, arp_cache[i].mac);
    arp_cache[i].valid = 1;
}

/* Assemble an ARP packet in net_txbuf and transmit it. */
static void arp_send(u16 op, const u8 *target_mac, const u8 *target_ip,
                     const u8 *eth_dst)
{
    struct eth_hdr *eth = (struct eth_hdr *)net_txbuf;
    struct arp_pkt *arp = (struct arp_pkt *)(net_txbuf + sizeof(struct eth_hdr));

    mac_cpy(eth_dst, eth->dest);
    mac_cpy(net_if.mac, eth->src);
    eth->type = ETH_P_ARP;

    arp->htype = ARP_HTYPE_ETHER;
    arp->ptype = ARP_PTYPE_IP;
    arp->hlen = ETH_ALEN;
    arp->plen = IP_ALEN;
    arp->op = op;
    mac_cpy(net_if.mac, arp->sha);
    ip_cpy(net_if.ip, arp->spa);
    mac_cpy(target_mac, arp->tha);
    ip_cpy(target_ip, arp->tpa);

    net_tx(net_txbuf, sizeof(struct eth_hdr) + sizeof(struct arp_pkt));
}

void arp_request(const u8 *ip)
{
    static const u8 unknown[ETH_ALEN] = { 0, 0, 0, 0, 0, 0 };
    static const u8 broadcast[ETH_ALEN] =
        { 0xff, 0xff, 0xff, 0xff, 0xff, 0xff };

    arp_send(ARP_OP_REQUEST, unknown, ip, broadcast);
}

void arp_input(const u8 *frame, u32 len)
{
    const struct arp_pkt *arp;

    if (len < sizeof(struct eth_hdr) + sizeof(struct arp_pkt))
        return;
    arp = (const struct arp_pkt *)(frame + sizeof(struct eth_hdr));

    if (arp->htype != ARP_HTYPE_ETHER || arp->ptype != ARP_PTYPE_IP)
        return;

    /* learn the sender, whatever the operation */
    arp_cache_put(arp->spa, arp->sha);

    /* answer requests addressed to our IPv4 address */
    if (arp->op == ARP_OP_REQUEST && ip_eq(arp->tpa, net_if.ip))
        arp_send(ARP_OP_REPLY, arp->sha, arp->spa, arp->sha);
}
