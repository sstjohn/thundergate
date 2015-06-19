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

#ifndef _RDMA_H_
#define _RDMA_H_

#include "utypes.h"

struct rdma_mode {
        u32 reserved :2;
        u32 in_band_vtag_enable :1;
        u32 hardware_ipv6_post_dma_processing_enable :1;
        u32 hardware_ipv4_post_dma_processing_enable :1;
        u32 post_dma_debug_enable :1;
        u32 address_overflow_error_logging_enable :1;
        u32 mmrr_disable :1;
        u32 jumbo_2k_mmrr_mode :1;
        u32 reserved2 :5;
        u32 pci_request_burst_length :2;
        u32 reserved3 :2;
        u32 mbuf_sbd_corruption_attn_enable :1;
        u32 mbuf_rbd_corruption_attn_enable :1;
        u32 bd_sbd_corruption_attn_enable :1;
        u32 read_dma_pci_x_split_transaction_timeout_expired_attention_enable :1;
        u32 read_dma_local_memory_write_longer_than_dma_length_attention_enable :1;
        u32 read_dma_pci_fifo_overread_attention_enable :1;
        u32 read_dma_pci_fifo_underrun_attention_enable :1;
        u32 read_dma_pci_fifo_overrun_attention_enable :1;
        u32 read_dma_pci_host_address_overflow_error_attention_enable :1;
        u32 read_dma_pci_parity_error_attention_enable :1;
        u32 read_dma_pci_master_abort_attention_enable :1;
        u32 read_dma_pci_target_abort_attention_enable :1;
        u32 enable :1;
        u32 reset :1;
};

struct rdma_status {
    u32 reserved :18;
    u32 mbuf_sbd_corruption_attention :1;
    u32 mbuf_rbd_corruption_attention :1;
    u32 bd_sbd_corruption_attention :1;
    u32 read_dma_pci_x_split_transaction_timeout_expired :1;
    u32 read_dma_local_memory_write_longer_than_dma_length_error :1;
    u32 read_dma_pci_fifo_overread_error :1;
    u32 read_dma_pci_fifo_underrun_error :1;
    u32 read_dma_pci_fifo_overrun_error :1;
    u32 read_dma_pci_host_address_overflow_error :1;
    u32 read_dma_completion_timer_timeout :1;
    u32 read_dma_completer_abort :1;
    u32 read_dma_unsupported_request :1;
    u32 reserved2 :2;
};

struct rdma_programmable_ipv6_extension_header {
    u32 type_2_en :1;
    u32 type_1_en :1;
    u32 reserved16 :14;
    u32 ext_hdr_type_2 :8;
    u32 ext_hdr_type_1 :8;
};

struct rdma_rstates_debug {
    u32 reserved6 :26;
    u32 rstate3 :2;
    u32 reserved3 :1;
    u32 rstate1 :3;
};

struct rdma_rstate2_debug {
    u32 reserved5 :27;
    u32 rstate2 :5;
};

struct rdma_bd_status_debug {
    u32 reserved3 :29;
    u32 bd_non_mbuf :1;
    u32 fst_bd_mbuf :1;
    u32 lst_bd_mbuf :1;
};

struct rdma_req_ptr_debug {
    u32 ih_dmad_length :16;
    u32 reserved10 :6;
    u32 txmbuf_left :6;
    u32 rh_dmad_load_en :1;
    u32 rftq_d_dmad_pnt :2;
    u32 rftq_b_dmad_pnt :1;
};

struct rdma_hold_d_dmad_debug {
    u32 reserved2 :30;
    u32 rhold_d_dmad :2;
};

struct rdma_length_and_address_index_debug {
    u32 rdma_rd_length :16;
    u32 mbuf_addr_idx :16;
};

struct rdma_mbuf_byte_count_debug {
    u32 reserved4 :28;
    u32 rmbuf_byte_cnt :4;
};

struct rdma_pcie_mbuf_byte_count_debug {
    u32 lt_term :4;
    u32 reserved27 :1;
    u32 lt_too_lg :1;
    u32 lt_dma_reload :1;
    u32 lt_dma_good :1;
    u32 cur_trans_active :1;
    u32 drpcireq :1;
    u32 dr_pci_word_swap :1;
    u32 dr_pci_byte_swap :1;
    u32 new_slow_core_clk_mode :1;
    u32 rbd_non_mbuf :1;
    u32 rfst_bd_mbuf :1;
    u32 rlst_bd_mbuf :1;
    u32 dr_pci_len :16;
};

struct rdma_pcie_read_request_address_debug {
    u32 dr_pci_ad_hi :16;
    u32 dr_pci_ad_lo :16;
};

struct rdma_fifo1_debug {
    u32 reserved8 :24;
    u32 c_write_addr :8;
};

struct rdma_fifo2_debug {
    u32 reserved16 :16;
    u32 rlctrl_in :8;
    u32 c_read_addr :8;
};

struct rdma_packet_request_debug_1 {
    u32 reserved8 :24;
    u32 pkt_req_cnt :8;
};

struct rdma_packet_request_debug_2 {
    u32 sdc_ack_cnt;
};

struct rdma_packet_request_debug_3 {
    u32 cs :4;
    u32 reserved26 :2;
    u32 lt_fst_seg :1;
    u32 lt_lst_seg :1;
    u32 lt_mem_ip_hdr_ofst :8;
    u32 lt_mem_tcp_hdr_ofst :8;
    u32 reserved7 :1;
    u32 pre_sdcq_pkt_cnt :7;
};

struct rdma_tcp_checksum_debug {
    u32 reserved30 :2;
    u32 fd_addr_req :6;
    u32 lt_mem_data_ofst :8;
    u32 lt_mem_tcp_chksum :16;
};

struct rdma_ip_tcp_header_checksum_debug {
    u32 lt_mem_ip_chksum :16;
    u32 lt_mem_tcphdr_chksum :16;
};

struct rdma_pseudo_checksum_debug {
    u32 lt_mem_pse_chksum_no_tcplen :16;
    u32 lt_mem_pkt_len :16;
};

struct rdma_mbuf_address_debug {
    u32 reserved30 :2;
    u32 mbuf1_addr :6;
    u32 reserved22 :2;
    u32 mbuf0_addr :6;
    u32 reserved14 :2;
    u32 pre_mbuf1_addr :6;
    u32 reserved6 :2;
    u32 pre_mbuf0_addr :6;
};

struct rdma_misc_ctrl_1 {
    u32 txmbuf_margin :11;
    u32 select_fed_enable :1;
    u32 fifo_high_mark :8;
    u32 fifo_low_mark :8;
    u32 slow_clock_fix_disable :1;
    u32 cq25155_fix_en :1;
    u32 late_col_fix_en :1;
    u32 sdi_shortq_en :1;
};

struct rdma_misc_ctrl_2 {
    u32 fifo_threshold_bd_req :8;
    u32 fifo_threshold_mbuf_req :8;
    u32 reserved14 :2;
    u32 mbuf_threshold_mbuf_req :6;
    u32 reserved7 :1;
    u32 clock_req_fix_en :1;
    u32 mbuf_threshold_clk_req :6;
};

struct rdma_misc_ctrl_3 {
    u32 reserved6 :26;
    u32 cq33951_fix_dis :1;
    u32 cq30888_fix1_en :1;
    u32 cq30888_fix2_en :1;
    u32 cq30808_fix_en :1;
    u32 reserved1 :1;
    u32 reserved0 :1;
};

struct rdma_regs {
    struct rdma_mode mode;
    struct rdma_status status;
    struct rdma_programmable_ipv6_extension_header programmable_ipv6_extension_header;
    struct rdma_rstates_debug rstates_debug;
    
    struct rdma_rstate2_debug rstate2_debug;
    struct rdma_bd_status_debug bd_status_debug;
    struct rdma_req_ptr_debug req_ptr_debug;
    struct rdma_hold_d_dmad_debug hold_d_dmad_debug;
    
    struct rdma_length_and_address_index_debug length_and_address_index_debug;
    struct rdma_mbuf_byte_count_debug mbuf_byte_count_debug;
    struct rdma_pcie_mbuf_byte_count_debug pcie_mbuf_byte_count_debug;
    struct rdma_pcie_read_request_address_debug pcie_read_request_address_debug;
    
    u32 pcie_dma_request_length_debug;
    struct rdma_fifo1_debug fifo1_debug;
    struct rdma_fifo2_debug fifo2_debug;
    u32 ofs_3c;

    struct rdma_packet_request_debug_1 packet_request_debug_1;
    struct rdma_packet_request_debug_2 packet_request_debug_2;    
    struct rdma_packet_request_debug_3 packet_request_debug_3;
    struct rdma_tcp_checksum_debug tcp_checksum_debug;

    struct rdma_ip_tcp_header_checksum_debug ip_tcp_header_checksum_debug;
    struct rdma_pseudo_checksum_debug pseudo_checksum_debug;    
    struct rdma_mbuf_address_debug mbuf_address_debug;
    u32 ofs_5c;

    u32 ofs_60;
    u32 ofs_64;
    u32 ofs_68;
    u32 ofs_6c;

    u32 ofs_70;
    u32 ofs_74;
    u32 ofs_78;
    u32 ofs_7c;

    u32 ofs_80;
    u32 ofs_84;
    u32 ofs_88;
    u32 ofs_8c;

    u32 ofs_90;
    u32 ofs_94;
    u32 ofs_98;
    u32 ofs_9c;

    u32 ofs_a0;
    u32 ofs_a4;
    u32 ofs_a8;
    u32 ofs_ac;

    u32 ofs_b0;
    u32 ofs_b4;
    u32 ofs_b8;
    u32 ofs_bc;

    u32 ofs_c0;
    u32 ofs_c4;
    u32 ofs_c8;
    u32 ofs_cc;

    u32 ofs_d0;
    u32 ofs_d4;
    u32 ofs_d8;
    u32 ofs_dc;

    u32 ofs_e0;
    u32 ofs_e4;
    u32 ofs_e8;
    u32 ofs_ec;

    u32 ofs_f0;
    u32 ofs_f4;
    u32 ofs_f8;
    u32 ofs_fc;
};


#endif
