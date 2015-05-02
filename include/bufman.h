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

#ifndef _BUFMAN_H_
#define _BUFMAN_H_

struct bufman_mode {
    union {
        struct {
            u32 txfifo_underrun_protection :1;
            u32 reserved :25;
            u32 reset_rxmbuf_pointer :1;
            u32 mbuf_low_attention_enable :1;
            u32 test_mode :1;
            u32 attention_enable :1;
            u32 enable :1;
            u32 reset :1;
        };
        u32 word;
    };
};

struct bufman_status {
    u32 test_mode :27;
    u32 mbuf_low_attention :1;
    u32 reserved :1;
    u32 error :1;
    u32 reserved2 :2;
};

struct bufman_mbuf_pool_bar {
    u32 reserved :9;
    u32 mbuf_base_addr :23;
};

struct bufman_mbuf_pool_length {
    u32 reserved :9;
    u32 mbuf_length :23;
};

struct bufman_rdma_mbuf_low_watermark {
    u32 reserved :26;
    u32 count :6;
};

struct bufman_dma_mbuf_low_watermark {
    u32 reserved :23;
    u32 count :9;
};

struct bufman_mbuf_high_watermark {
    u32 reserved :23;
    u32 count :9;
};

struct bufman_risc_mbuf_cluster_allocation_request {
    u32 allocation_request :1;
    u32 reserved :31;
};

struct bufman_risc_mbuf_cluster_allocation_response {
    u32 mbuf;
};

struct bufman_hardware_diagnostic_1 {
    u32 reserved :6;
    u32 last_txmbuf_deallocation_head_ptr :6;
    u32 reserved2 :4;
    u32 last_txmbuf_deallocation_tail_ptr :6;
    u32 reserved3 :4;
    u32 next_txmbuf_allocation_ptr :6;
};

struct bufman_hardware_diagnostic_2 {
    u32 reserved :7;
    u32 rxmbuf_count :9;
    u32 reserved2 :1;
    u32 txmbuf_count :6;
    u32 rxmbuf_left :9;
};

struct bufman_hardware_diagnostic_3 {
    u32 reserved :7;
    u32 next_rxmbuf_deallocation_ptr :9;
    u32 reserved2 :7;
    u32 next_rxmbuf_allocation_ptr :9; /* spec bugged */
};

struct bufman_receive_flow_threshold {
    u32 reserved :23;
    u32 mbuf_threshold :9;
};

struct bufman_regs {
    struct bufman_mode mode;
    struct bufman_status status;
    struct bufman_mbuf_pool_bar mbuf_pool_base_address;
    struct bufman_mbuf_pool_length mbuf_pool_length;

    struct bufman_rdma_mbuf_low_watermark rdma_mbuf_low_watermark;
    struct bufman_dma_mbuf_low_watermark dma_mbuf_low_watermark;
    struct bufman_mbuf_high_watermark mbuf_high_watermark;
    struct bufman_risc_mbuf_cluster_allocation_request
        rx_risc_mbuf_cluster_allocation_request;

    struct bufman_risc_mbuf_cluster_allocation_response 
        rx_risc_mbuf_cluster_allocation_response;
    struct bufman_risc_mbuf_cluster_allocation_request
	tx_risc_mbuf_cluster_allocation_request;
    struct bufman_risc_mbuf_cluster_allocation_response
	tx_risc_mbuf_cluster_allocation_response;
    u32 dma_desc_pool_addr;

    u32 dma_desc_pool_size;
    u32 dma_low_water;
    u32 dma_high_water;
    u32 rx_dma_alloc_request;

    u32 rx_dma_alloc_response;
    u32 tx_dma_alloc_request;
    u32 tx_dma_alloc_response;
    struct bufman_hardware_diagnostic_1 hardware_diagnostic_1;

    struct bufman_hardware_diagnostic_2 hardware_diagnostic_2;
    struct bufman_hardware_diagnostic_3 hardware_diagnostic_3;
    struct bufman_receive_flow_threshold receive_flow_threshold;
};

#endif
