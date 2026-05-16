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
 * The Ethernet (L2) ingress dispatch and the stack's shared state.
 *
 * The hardware-touching transmit path and initialisation live in
 * coretx.c; keeping them out of this file leaves ether.c -- and the
 * arp/ip/icmp/udp protocol code -- free of any firmware/register
 * dependency, so it builds and is tested on the host (see fw/net/test/).
 */

#include "net/net.h"
#include "net/inet.h"

struct net_iface net_if;
u8 net_txbuf[NET_TX_MAX];

void net_rx(const u8 *frame, u32 len)
{
    const struct eth_hdr *f = (const struct eth_hdr *)frame;

    if (len < sizeof(struct eth_hdr))
        return;

    /* The core is big-endian, so f->type is already in network order. */
    if (f->type == ETH_P_ARP)
        arp_input(frame, len);
    else if (f->type == ETH_P_IP)
        ip_input(frame, len);
    /* Any other EtherType is ignored here; the 0x88b5 control protocol is
       handled directly by rx() and never reaches net_rx(). */
}
