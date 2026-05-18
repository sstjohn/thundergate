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
 * Host-side test of the on-core TCP/IP stack.
 *
 * The protocol code in fw/net/{checksum,ether,arp,ip,icmp,udp}.c builds
 * unchanged on the host. This harness supplies the two things it would
 * otherwise get from the firmware -- mac_cpy() and net_tx() -- captures
 * the frames the stack emits, and checks them against crafted requests.
 *
 * It exercises the protocol logic (dispatch, parsing, reply construction,
 * checksum round-trips) self-consistently. True network-byte-order
 * behaviour is a property of the big-endian core, verified on hardware.
 */

#include <stdio.h>

#include "net/net.h"
#include "net/inet.h"
#include "net/checksum.h"

/* --- the two things the stack would otherwise get from the firmware ---- */

void mac_cpy(const u8 *src, u8 *dst)
{
    int i;
    for (i = 0; i < ETH_ALEN; i++)
        dst[i] = src[i];
}

static u8 tx_buf[NET_TX_MAX];
static u32 tx_len;
static int tx_count;

void net_tx(const u8 *frame, u32 len)
{
    u32 i;
    if (len > sizeof(tx_buf))
        len = sizeof(tx_buf);
    for (i = 0; i < len; i++)
        tx_buf[i] = frame[i];
    tx_len = len;
    tx_count++;
}

/* --- fixtures ----------------------------------------------------------- */

static const u8 our_mac[ETH_ALEN]  = { 0x02, 0, 0xde, 0xad, 0xbe, 0xef };
static const u8 peer_mac[ETH_ALEN] = { 0x02, 0, 0x11, 0x22, 0x33, 0x44 };
static const u8 our_ip[IP_ALEN]    = { 192, 168, 1, 222 };
static const u8 peer_ip[IP_ALEN]   = { 192, 168, 1, 50 };

static int failures;

static void check(int cond, const char *what)
{
    printf("  %s  %s\n", cond ? "ok  " : "FAIL", what);
    if (!cond)
        failures++;
}

static void setup(void)
{
    int i;
    for (i = 0; i < ETH_ALEN; i++)
        net_if.mac[i] = our_mac[i];
    for (i = 0; i < IP_ALEN; i++) {
        net_if.ip[i] = our_ip[i];
        net_if.netmask[i] = 255;
        net_if.gateway[i] = our_ip[i];
    }
    net_if.netmask[3] = 0;     /* a /24 subnet */
    tx_count = 0;
}

/* --- tests -------------------------------------------------------------- */

static void test_arp(void)
{
    u8 req[sizeof(struct eth_hdr) + sizeof(struct arp_pkt)];
    struct eth_hdr *eth = (struct eth_hdr *)req;
    struct arp_pkt *arp = (struct arp_pkt *)(req + sizeof(struct eth_hdr));
    struct arp_pkt *rep;
    int i;

    printf("ARP request for our address -> reply:\n");
    for (i = 0; i < ETH_ALEN; i++)
        eth->dest[i] = 0xff;
    mac_cpy(peer_mac, eth->src);
    eth->type = ETH_P_ARP;
    arp->htype = ARP_HTYPE_ETHER;
    arp->ptype = ARP_PTYPE_IP;
    arp->hlen = ETH_ALEN;
    arp->plen = IP_ALEN;
    arp->op = ARP_OP_REQUEST;
    mac_cpy(peer_mac, arp->sha);
    for (i = 0; i < IP_ALEN; i++)  arp->spa[i] = peer_ip[i];
    for (i = 0; i < ETH_ALEN; i++) arp->tha[i] = 0;
    for (i = 0; i < IP_ALEN; i++)  arp->tpa[i] = our_ip[i];

    tx_count = 0;
    net_rx(req, sizeof(req));

    check(tx_count == 1, "one frame transmitted");
    rep = (struct arp_pkt *)(tx_buf + sizeof(struct eth_hdr));
    check(rep->op == ARP_OP_REPLY, "operation is ARP reply");
    check(rep->sha[0] == our_mac[0] && rep->sha[5] == our_mac[5],
          "sender hardware address is ours");
    check(rep->spa[3] == our_ip[3], "sender protocol address is ours");
    check(rep->tpa[3] == peer_ip[3], "target protocol address is the peer");
}

static void test_icmp(void)
{
    u8 req[sizeof(struct eth_hdr) + sizeof(struct ip_hdr)
           + sizeof(struct icmp_hdr) + 16];
    struct eth_hdr *eth = (struct eth_hdr *)req;
    struct ip_hdr *ip = (struct ip_hdr *)(req + sizeof(struct eth_hdr));
    struct icmp_hdr *icmp = (struct icmp_hdr *)
        (req + sizeof(struct eth_hdr) + sizeof(struct ip_hdr));
    u8 *data = (u8 *)icmp + sizeof(struct icmp_hdr);
    u32 icmplen = sizeof(struct icmp_hdr) + 16;
    struct ip_hdr *rip;
    struct icmp_hdr *rep;
    int i, echoed;

    printf("ICMP echo request -> echo reply:\n");
    mac_cpy(our_mac, eth->dest);
    mac_cpy(peer_mac, eth->src);
    eth->type = ETH_P_IP;

    ip->ver_ihl = (IP_VERSION << 4) | 5;
    ip->tos = 0;
    ip->total_len = sizeof(struct ip_hdr) + icmplen;
    ip->id = 1;
    ip->frag_off = 0;
    ip->ttl = 64;
    ip->protocol = IP_PROTO_ICMP;
    ip->checksum = 0;
    for (i = 0; i < IP_ALEN; i++) { ip->src[i] = peer_ip[i]; ip->dst[i] = our_ip[i]; }
    net_put16((u8 *)&ip->checksum, net_cksum((u8 *)ip, sizeof(struct ip_hdr)));

    icmp->type = ICMP_TYPE_ECHO_REQUEST;
    icmp->code = 0;
    icmp->checksum = 0;
    icmp->id = 0x1234;
    icmp->seq = 7;
    for (i = 0; i < 16; i++)
        data[i] = (u8)('a' + i);
    net_put16((u8 *)&icmp->checksum, net_cksum((u8 *)icmp, icmplen));

    tx_count = 0;
    net_rx(req, sizeof(req));

    check(tx_count == 1, "one frame transmitted");
    rip = (struct ip_hdr *)(tx_buf + sizeof(struct eth_hdr));
    rep = (struct icmp_hdr *)(tx_buf + NET_L4_OFF);
    check(rip->protocol == IP_PROTO_ICMP, "reply is an ICMP datagram");
    check(net_cksum((u8 *)rip, sizeof(struct ip_hdr)) == 0,
          "reply IPv4 header checksum is valid");
    check(rip->dst[3] == peer_ip[3], "reply addressed to the peer");
    check(rep->type == ICMP_TYPE_ECHO_REPLY, "type is echo-reply");
    check(rep->id == 0x1234 && rep->seq == 7, "echo id and sequence preserved");
    check(net_cksum((u8 *)rep, icmplen) == 0, "reply ICMP checksum is valid");
    echoed = 1;
    for (i = 0; i < 16; i++)
        if (((u8 *)rep + sizeof(struct icmp_hdr))[i] != (u8)('a' + i))
            echoed = 0;
    check(echoed, "echo data returned intact");
}

static void test_udp(void)
{
    u8 req[sizeof(struct eth_hdr) + sizeof(struct ip_hdr)
           + sizeof(struct udp_hdr) + 8];
    struct eth_hdr *eth = (struct eth_hdr *)req;
    struct ip_hdr *ip = (struct ip_hdr *)(req + sizeof(struct eth_hdr));
    struct udp_hdr *udp = (struct udp_hdr *)
        (req + sizeof(struct eth_hdr) + sizeof(struct ip_hdr));
    u8 *data = (u8 *)udp + sizeof(struct udp_hdr);
    u32 ulen = sizeof(struct udp_hdr) + 8;
    struct udp_hdr *rep;
    int i, echoed;

    printf("UDP datagram -> echo reply:\n");
    mac_cpy(our_mac, eth->dest);
    mac_cpy(peer_mac, eth->src);
    eth->type = ETH_P_IP;

    ip->ver_ihl = (IP_VERSION << 4) | 5;
    ip->tos = 0;
    ip->total_len = sizeof(struct ip_hdr) + ulen;
    ip->id = 2;
    ip->frag_off = 0;
    ip->ttl = 64;
    ip->protocol = IP_PROTO_UDP;
    ip->checksum = 0;
    for (i = 0; i < IP_ALEN; i++) { ip->src[i] = peer_ip[i]; ip->dst[i] = our_ip[i]; }
    net_put16((u8 *)&ip->checksum, net_cksum((u8 *)ip, sizeof(struct ip_hdr)));

    udp->src_port = 4444;
    udp->dst_port = 7;            /* echo */
    udp->len = ulen;
    udp->checksum = 0;            /* optional -- the stack skips verifying it */
    for (i = 0; i < 8; i++)
        data[i] = (u8)(0x10 + i);

    tx_count = 0;
    net_rx(req, sizeof(req));

    check(tx_count == 1, "one frame transmitted");
    rep = (struct udp_hdr *)(tx_buf + NET_L4_OFF);
    check(rep->src_port == 7, "reply source port is the request's destination");
    check(rep->dst_port == 4444, "reply destination port is the request's source");
    check(rep->len == ulen, "reply length matches the request");
    echoed = 1;
    for (i = 0; i < 8; i++)
        if (((u8 *)rep + sizeof(struct udp_hdr))[i] != (u8)(0x10 + i))
            echoed = 0;
    check(echoed, "datagram data returned intact");
}

int main(void)
{
    printf("ThunderGate on-core TCP/IP stack -- host test\n\n");

    setup(); test_arp();
    setup(); test_icmp();
    setup(); test_udp();

    printf("\n%s\n", failures ? "*** FAILURES ***" : "all checks passed");
    return failures ? 1 : 0;
}
