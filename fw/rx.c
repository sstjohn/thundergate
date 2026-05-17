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

#include "fw.h"
#include "net/net.h"

/* Contiguous reassembly buffer for an inbound frame handed to the stack. */
static u8 net_rxbuf[NET_TX_MAX];

void rx()
{
    if (ftq.rdiq.peek.valid == 1 && ftq.rdiq.peek.pass == 0) {
        u32 mbuf = ftq.rdiq.peek.head_rxmbuf_ptr;

        if (0x88b5 != (rxmbuf[mbuf].data.word[13] >> 16)) {
            /* Not a control frame: gather it from the mbuf cluster into a
               contiguous buffer and hand it to the on-core TCP/IP stack. */
            u32 mbufs = ftq.rdiq.peek.word & 0x3ffff;
            u32 total = rxmbuf[mbuf].data.frame.len;
            u32 got = 0, cur = mbuf, first = 1;

            while (got < total && got < sizeof(net_rxbuf)) {
                volatile struct mbuf *m = &rxmbuf[cur];
                u32 off = first ? sizeof(struct mbuf_frame_desc) : 0;
                u32 n = m->hdr.length;
                u32 j;

                for (j = 0; j < n && got < total && got < sizeof(net_rxbuf); j++)
                    net_rxbuf[got++] = m->data.byte[off + j];

                if (!m->hdr.c)
                    break;
                cur = m->hdr.next_mbuf;
                first = 0;
            }

            ftq.rdiq.peek.skip = 1;
            ftq.mbuf_clust_free.q.word = mbufs;

            net_rx(net_rxbuf, got);
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

/* Configure receive rule `idx` to route frames whose EtherType (the
   16-bit field at frame offset 12) equals `etype` to the on-core CPU.
   Mirrors the proven control-protocol rule. */
static void rxcpu_rule(u32 idx, u16 etype)
{
    emac.rx_rule[idx].control.word = 0;
    emac.rx_rule[idx].control.offset = 12;
    emac.rx_rule[idx].control.mask = 1;
    emac.rx_rule[idx].control.activate_rxcpu = 1;
    emac.rx_rule[idx].control.pclass = 1;
    emac.rx_rule[idx].mask_value = (0xffff0000 | etype);
}

void rx_setup()
{
    rlp.mode.reset = 1;
    emac.rx_rule[5].control.enable = 0;
    emac.rx_rule[6].control.enable = 0;
    emac.rx_rule[7].control.enable = 0;
    while (rlp.mode.reset
           || emac.rx_rule[5].control.enable
           || emac.rx_rule[6].control.enable
           || emac.rx_rule[7].control.enable);

    /* The EMAC has 8 receive rules (0-7; see emac.h). Route IPv4
       (0x0800), ARP (0x0806) and the legacy control protocol
       (config.ctrl_etype, 0x88b5) to the on-core CPU; rx() dispatches
       all three. Each is a standalone EtherType match, so a frame
       matching any one is delivered to the core. (While these rules
       are active the host no longer receives ARP/IPv4 on this port --
       the core is the network endpoint.) */
    rxcpu_rule(5, 0x0800);
    rxcpu_rule(6, 0x0806);
    rxcpu_rule(7, config.ctrl_etype);

    rlp.config.number_of_lists_per_distribution_group = 1;
    rlp.config.number_of_active_lists = 0x10;
    rlp.config.bad_frames_class = 1;

    set_and_wait(rlp.mode.enable);
    set_and_wait(grc.rxcpu_event_enable.rdiq);
    set_and_wait(emac.rx_rule[5].control.enable);
    set_and_wait(emac.rx_rule[6].control.enable);
    set_and_wait(emac.rx_rule[7].control.enable);
}
