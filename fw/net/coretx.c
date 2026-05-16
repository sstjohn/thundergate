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
 * The hardware half of the stack: initialisation from the firmware's
 * state/config, and frame transmit through the MAC transmit FTQ.
 *
 * This is the only stack file that depends on the Tigon3 registers and
 * mbuf layout, so it is the only one excluded from the host test build.
 */

#include "fw.h"
#include "net/net.h"
#include "net/inet.h"

/* Scratch transmit mbuf. Shared with tx_asf(): the firmware event loop is
 * single-threaded, so the control protocol and the stack never transmit
 * at the same time. */
#define NET_TX_MBUF 0xad

void net_init(void)
{
    int i;

    for (i = 0; i < 6; i++)
        net_if.mac[i] = state.my_mac[i];
    for (i = 0; i < 4; i++) {
        net_if.ip[i] = config.ip_addr[i];
        net_if.netmask[i] = config.netmask[i];
        net_if.gateway[i] = config.gateway[i];
    }
}

/*
 * Transmit a complete Ethernet frame.
 *
 * The frame is copied into a chain of up to three transmit mbufs and
 * handed to the MAC transmit FTQ. The layout mirrors tx_asf(): the first
 * mbuf holds a 40-byte transmit descriptor followed by 80 frame bytes,
 * each further mbuf holds 120.
 */
void net_tx(const u8 *frame, u32 len)
{
    u32 buf = NET_TX_MBUF;
    struct mbuf *mb = (struct mbuf *)(0x8000 + (buf << 7));
    u32 sub = (buf << 16) | buf;
    const u8 *p = frame;
    u32 i;

    if (len > NET_TX_MAX)
        len = NET_TX_MAX;

    /* First mbuf: 40-byte transmit descriptor, then frame bytes 40..119. */
    mb->hdr.c = (len > 80) ? 1 : 0;
    mb->hdr.f = 1;
    mb->hdr.length = 80;
    mb->next_frame_ptr = 0;
    mb->hdr.next_mbuf = buf + 1;

    mb->data.frame.status_ctrl = 0;
    mb->data.frame.len = (len < 64) ? 64 : len;   /* minimum Ethernet frame */
    mb->data.frame.qids = 0xc;
    mb->data.frame.mbuf = (len <= 80) ? 1 : ((len <= 200) ? 2 : 3);

    i = sizeof(struct mbuf_frame_desc);           /* 40 */
    for (; i < 120 && len > 0; i++, len--)
        mb->data.byte[i] = *p++;
    while (i < 104)                               /* pad a short frame to 64 */
        mb->data.byte[i++] = 0;

    /* Second mbuf, if the frame did not fit (carries up to 120 bytes). */
    if (len > 0) {
        mb++;
        mb->hdr.c = (len > 120) ? 1 : 0;
        mb->hdr.f = 0;
        mb->hdr.length = (len > 120) ? 120 : len;
        mb->hdr.next_mbuf = (len > 120) ? (buf + 2) : 0;
        for (i = 0; i < 120 && len > 0; i++, len--)
            mb->data.byte[i] = *p++;
        sub++;
    }

    /* Third mbuf. */
    if (len > 0) {
        mb++;
        mb->hdr.c = 0;
        mb->hdr.f = 0;
        mb->hdr.length = len;
        mb->hdr.next_mbuf = 0;
        for (i = 0; len > 0; i++, len--)
            mb->data.byte[i] = *p++;
        sub++;
    }

    ftq.mac_tx.q.word = sub;
}
