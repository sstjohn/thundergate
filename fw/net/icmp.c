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
 * ICMP (RFC 792): answer echo requests so the core responds to ping.
 */

#include "net/net.h"
#include "net/inet.h"
#include "net/checksum.h"

void icmp_input(const u8 *iphdr, const u8 *payload, u32 plen)
{
    const struct ip_hdr *ip = (const struct ip_hdr *)iphdr;
    const struct icmp_hdr *req = (const struct icmp_hdr *)payload;
    struct icmp_hdr *rep;
    u8 *seg;
    u32 i;

    if (plen < sizeof(struct icmp_hdr))
        return;
    if (req->type != ICMP_TYPE_ECHO_REQUEST || req->code != 0)
        return;                          /* only echo requests are answered */
    if (net_cksum(payload, plen) != 0)
        return;                          /* bad ICMP checksum */
    if (plen > (NET_TX_MAX - NET_L4_OFF))
        return;                          /* echo data too large to bounce */

    /* The reply is the request verbatim, with the type changed to
       echo-reply and the checksum recomputed over the new message. */
    seg = net_txbuf + NET_L4_OFF;
    for (i = 0; i < plen; i++)
        seg[i] = payload[i];

    rep = (struct icmp_hdr *)seg;
    rep->type = ICMP_TYPE_ECHO_REPLY;
    rep->checksum = 0;
    net_put16((u8 *)&rep->checksum, net_cksum(seg, plen));

    ip_output(ip->src, IP_PROTO_ICMP, plen);
}
