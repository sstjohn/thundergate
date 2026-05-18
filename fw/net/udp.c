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
 * UDP (RFC 768): a console service. A datagram sent to CONSOLE_PORT carries
 * one line of REPL input; it is handed to the language interpreter linked
 * into this image and the interpreter's output is returned as a single
 * datagram to the sender. `nc -u <nic-ip> 7777` is thus an interactive
 * prompt served entirely by the NIC's RX CPU.
 */

#include "net/net.h"
#include "net/inet.h"
#include "net/checksum.h"
#include "console.h"

/* UDP port the REPL listens on. Datagrams to any other port are ignored. */
#define CONSOLE_PORT 7777

/* The UDP checksum covers an IPv4 pseudo-header (source and destination
 * address, a zero byte, the protocol, the UDP length) and then the UDP
 * segment itself. */
static u16 udp_checksum(const u8 *src_ip, const u8 *dst_ip,
                        const u8 *seg, u32 ulen)
{
    u8 pseudo[12];
    u32 sum;

    pseudo[0] = src_ip[0]; pseudo[1] = src_ip[1];
    pseudo[2] = src_ip[2]; pseudo[3] = src_ip[3];
    pseudo[4] = dst_ip[0]; pseudo[5] = dst_ip[1];
    pseudo[6] = dst_ip[2]; pseudo[7] = dst_ip[3];
    pseudo[8] = 0;
    pseudo[9] = IP_PROTO_UDP;
    pseudo[10] = ulen >> 8;
    pseudo[11] = ulen & 0xff;

    sum = net_cksum_partial(pseudo, sizeof(pseudo), 0);
    return net_cksum_seed(seg, ulen, sum);
}

void udp_input(const u8 *iphdr, const u8 *payload, u32 plen)
{
    const struct ip_hdr *ip = (const struct ip_hdr *)iphdr;
    const struct udp_hdr *req = (const struct udp_hdr *)payload;
    const char *out;
    struct udp_hdr *rep;
    u8 *seg;
    u32 ulen, dlen, olen, i;
    u16 ck;

    if (plen < sizeof(struct udp_hdr))
        return;
    ulen = req->len;                         /* UDP header + data */
    if (ulen < sizeof(struct udp_hdr) || ulen > plen)
        return;

    /* Only datagrams to the console port carry a REPL line. */
    if (req->dst_port != CONSOLE_PORT)
        return;

    /* The UDP checksum is optional; verify it only when one is present. */
    if (req->checksum != 0 &&
        udp_checksum(ip->src, net_if.ip, payload, ulen) != 0)
        return;

    dlen = ulen - sizeof(struct udp_hdr);

    /* Hand the datagram payload to the interpreter as one REPL line; it
       leaves its output in the console buffer. */
    con_out_reset();
    interp_eval_line((const char *)payload + sizeof(struct udp_hdr), dlen);
    out = con_out_buf();
    olen = con_out_len();                    /* bounded to one datagram */

    /* Build the reply datagram from the console buffer, ports swapped. */
    seg = net_txbuf + NET_L4_OFF;
    rep = (struct udp_hdr *)seg;
    rep->src_port = req->dst_port;
    rep->dst_port = req->src_port;
    rep->len = sizeof(struct udp_hdr) + olen;
    rep->checksum = 0;
    for (i = 0; i < olen; i++)
        seg[sizeof(struct udp_hdr) + i] = out[i];

    ck = udp_checksum(net_if.ip, ip->src, seg, rep->len);
    if (ck == 0)
        ck = 0xffff;                         /* a 0 checksum transmits as ~0 */
    net_put16((u8 *)&rep->checksum, ck);

    ip_output(ip->src, IP_PROTO_UDP, rep->len);
}
