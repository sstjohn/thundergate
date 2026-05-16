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
 * IPv4 (RFC 791): receive and validate datagrams addressed to us and hand
 * the payload to ICMP/UDP; build and transmit outbound datagrams.
 *
 * No fragmentation or reassembly -- fragmented datagrams are dropped, and
 * outbound datagrams are limited to what the transmit path carries in one
 * frame.
 */

#include "fw.h"
#include "net/net.h"
#include "net/inet.h"
#include "net/checksum.h"

#define ETH_HDR_LEN 14   /* sizeof(struct eth_hdr) */
#define IP_HDR_LEN  20   /* sizeof(struct ip_hdr)  */

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

/* Is `ip` reachable directly on our subnet, rather than via the gateway? */
static int ip_onlink(const u8 *ip)
{
    int i;

    for (i = 0; i < IP_ALEN; i++)
        if ((ip[i] & net_if.netmask[i]) != (net_if.ip[i] & net_if.netmask[i]))
            return 0;
    return 1;
}

void ip_input(const u8 *frame, u32 len)
{
    const struct eth_hdr *eth = (const struct eth_hdr *)frame;
    const struct ip_hdr *ip;
    u32 ihl, total, plen;
    const u8 *payload;

    if (len < (ETH_HDR_LEN + IP_HDR_LEN))
        return;
    ip = (const struct ip_hdr *)(frame + ETH_HDR_LEN);

    if (IP_VER(ip) != IP_VERSION)
        return;
    ihl = IP_IHL(ip) * 4;                  /* header length in bytes */
    if (ihl < IP_HDR_LEN || (ETH_HDR_LEN + ihl) > len)
        return;
    if (net_cksum((const u8 *)ip, ihl) != 0)
        return;                            /* bad header checksum */
    if (ip->frag_off & IP_FRAG_MASK)
        return;                            /* a fragment: no reassembly */
    if (!ip_eq(ip->dst, net_if.ip))
        return;                            /* not addressed to us */

    total = ip->total_len;
    if (total > (len - ETH_HDR_LEN))
        total = len - ETH_HDR_LEN;         /* clamp to the bytes received */
    if (total < ihl)
        return;
    payload = (const u8 *)ip + ihl;
    plen = total - ihl;

    /* learn the sender, so a reply needs no separate ARP exchange */
    arp_cache_put(ip->src, eth->src);

    if (ip->protocol == IP_PROTO_ICMP)
        icmp_input((const u8 *)ip, payload, plen);
    else if (ip->protocol == IP_PROTO_UDP)
        udp_input((const u8 *)ip, payload, plen);
}

void ip_output(const u8 *dst_ip, u8 proto, u32 plen)
{
    struct eth_hdr *eth = (struct eth_hdr *)net_txbuf;
    struct ip_hdr *ip = (struct ip_hdr *)(net_txbuf + ETH_HDR_LEN);
    const u8 *next_hop, *dst_mac;
    u32 total = IP_HDR_LEN + plen;
    static u16 ip_id;

    if ((ETH_HDR_LEN + total) > NET_TX_MAX)
        return;                            /* too large for one frame */

    /* next hop: the destination if on-link, otherwise the gateway */
    next_hop = ip_onlink(dst_ip) ? dst_ip : net_if.gateway;
    dst_mac = arp_lookup(next_hop);
    if (dst_mac == 0) {
        arp_request(next_hop);
        return;          /* dropped; the request primes the cache for a retry */
    }

    ip->ver_ihl = (IP_VERSION << 4) | (IP_HDR_LEN / 4);
    ip->tos = 0;
    ip->total_len = total;
    ip->id = ip_id++;
    ip->frag_off = 0;
    ip->ttl = 64;
    ip->protocol = proto;
    ip->checksum = 0;
    ip_cpy(net_if.ip, ip->src);
    ip_cpy(dst_ip, ip->dst);
    ip->checksum = net_cksum((const u8 *)ip, IP_HDR_LEN);

    mac_cpy(dst_mac, eth->dest);
    mac_cpy(net_if.mac, eth->src);
    eth->type = ETH_P_IP;

    net_tx(net_txbuf, ETH_HDR_LEN + total);
}
