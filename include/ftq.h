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

#ifndef _FTQ_H_
#define _FTQ_H_

struct ftq_reset {
    union {
        u32 word;
        struct {
            u32 reserved :15;
            u32 receive_data_completion :1;
            u32 reserved2 :1;
            u32 receive_list_placement :1;
            u32 receive_bd_complete :1;
            u32 reserved3 :1;
            u32 mac_tx :1;
            u32 host_coalescing :1;
            u32 send_data_completion :1;
            u32 reserved4 :1;
            u32 dma_high_prio_write :1;
            u32 dma_write :1;
            u32 reserved5 :1;
            u32 send_bd_completion :1;
            u32 reserved6 :1;
            u32 dma_high_prio_read :1;
            u32 dma_read :1;
            u32 reserved7 :1;
        };
    };
};

struct ftq_enqueue_dequeue {
    union {
        struct {
            u32 ignored1 :10;
            u32 head_txmbuf_ptr :6;
            u32 ignored2 :10;
            u32 tail_txmbuf_ptr :6;
        };
        u32 word;
    };
};

struct ftq_write_peek {
    union {
        struct {
	    u32 reserved :11;
	    u32 valid :1;
	    u32 skip :1;
	    u32 pass :1;
	    u32 head_rxmbuf_ptr :9;
	    u32 tail_rxmbuf_ptr :9;
	};
	u32 word;
    };
};

struct ftq_queue_regs {
    u32 control;
    u32 count;
    struct ftq_enqueue_dequeue q;
    struct ftq_write_peek peek;
};

struct ftq_regs {
    struct ftq_reset reset;
    u32 ofs_04;
    u32 ofs_08;
    u32 ofs_0c;

    struct ftq_queue_regs dma_read;
    struct ftq_queue_regs dma_high_read;
    struct ftq_queue_regs dma_comp_discard;
    struct ftq_queue_regs send_bd_comp;

    struct ftq_queue_regs send_data_init;
    struct ftq_queue_regs dma_write;
    struct ftq_queue_regs dma_high_write;
    struct ftq_queue_regs sw_type1;

    struct ftq_queue_regs send_data_comp;
    struct ftq_queue_regs host_coalesce;
    struct ftq_queue_regs mac_tx;
    struct ftq_queue_regs mbuf_clust_free;

    struct ftq_queue_regs rcv_bd_comp;
    struct ftq_queue_regs rcv_list_plmt;
    struct ftq_queue_regs rdiq;
    struct ftq_queue_regs rcv_data_comp;

    struct ftq_queue_regs sw_type2;
};

#endif

