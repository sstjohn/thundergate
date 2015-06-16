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


void rx()
{
    if (ftq.rdiq.peek.valid == 1 && ftq.rdiq.peek.pass == 0) {
	u32 mbuf = ftq.rdiq.peek.head_rxmbuf_ptr;

	if (0x88b5 != (rxmbuf[mbuf].data.word[13] >> 16)) {
		if (state.flags & HANDSHAKE_MAGIC_SEEN)
			ftq.rdiq.peek.pass = 1;
		else {
			u32 mbufs = ftq.rdiq.peek.word & 0x3ffff;
			ftq.rdiq.peek.skip = 1;
			ftq.mbuf_clust_free.q.word = mbufs;
		}
	} else { 
		u32 mbufs = ftq.rdiq.peek.word & 0x3ffff;
		u32 tmp = rxmbuf[mbuf].data.word[13];
		u16 cmd = tmp & 0xffff;
		u32 arg1 = rxmbuf[mbuf].data.word[14];
		u32 arg2 = rxmbuf[mbuf].data.word[15];
		u32 arg3 = rxmbuf[mbuf].data.word[16];

		mac_cpy(((u8 *)&rxmbuf[mbuf].data.word[11]) + 2, state.remote_mac);
		state.dest_mac = state.remote_mac;

		ftq.rdiq.peek.skip = 1;
		
		ftq.mbuf_clust_free.q.word = mbufs;

		handle(tx_asf, cmd, arg1, arg2, arg3);
	}
    }
    grc.rxcpu_event.rdiq = 0;
}

void rx_setup() 
{
    emac.rx_rule[7].control.enable = 0;
    while (emac.rx_rule[7].control.enable);

    emac.rx_rule[7].control.word = 0;

    emac.rx_rule[7].control.offset = 12;
    emac.rx_rule[7].control.mask = 1;
    emac.rx_rule[7].control.activate_rxcpu = 1;
    emac.rx_rule[7].control.pclass = 1;

    emac.rx_rule[7].mask_value = (0xffff0000 | config.ctrl_etype);

    emac.rx_rule[7].control.enable = 1;
    while (!emac.rx_rule[7].control.enable);

    rlp.mode.enable = 1;
    grc.rxcpu_event_enable.rdiq = 1;
}
