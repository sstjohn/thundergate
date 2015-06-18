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

#include "fw.h"

void tx_asf(void *_src, u32 len, u16 cmd)
{
    int i = 0;
    u32 buf = 0xad;
    struct mbuf *mb = (struct mbuf *)(0x8000 + (buf << 7));
    u32 sub = buf << 16 | buf;

    u32 blen = len << 2;

    mb->hdr.c = blen > 80 ? 1 : 0;
    mb->hdr.f = 1;
    mb->hdr.length = 80;
    mb->next_frame_ptr = 0;
    mb->hdr.next_mbuf = buf + 1;

    mb->data.frame.status_ctrl = 0;
    
    mb->data.frame.len = (blen + 16) < 64 ? 64 : (blen + 16);
    mb->data.frame.qids = 0xc;
    
    mb->data.frame.mbuf = blen <= 80 ? 1 : (blen <= 200 ? 2 : 3);

    i = sizeof(mb->data.frame);
    mac_cpy(state.dest_mac, &mb->data.byte[i]);
    i += 6;
    mac_cpy(state.my_mac, &mb->data.byte[i]);
    i += 6;
    mb->data.word[i >> 2] = (config.ctrl_etype << 16) | cmd;
    i += 4;

    u8 *src = (u8 *)_src;
    for (; i < 120 && blen > 0; i++, blen--)
	    mb->data.byte[i] = *src++;

    while (i < 104)
	mb->data.byte[i++] = 0;

    if (blen > 0) {
	mb++;
	mb->hdr.c = 1;
	mb->hdr.f = 0;
	mb->hdr.length = blen > 120 ? 120 : blen;
	mb->hdr.next_mbuf = blen > 120 ? buf + 2 : 0;
	for (i = 0; i < 120 && blen > 0; i++, blen--)
		mb->data.byte[i] = *src++;
        sub++;
    }

    if (blen > 0) {
	mb++;
	mb->hdr.c = 1;
	mb->hdr.f = 0;
	mb->hdr.length = blen;
	mb->hdr.next_mbuf = 0;
	for (i = 0;  blen > 0; i++, blen--)
	    mb->data.byte[i] = *src++;
        sub++;
    }

    ftq.mac_tx.q.word = sub;

    state.dest_mac = state.broadcast_mac;
}
