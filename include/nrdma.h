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

#ifndef _NRDMA_H_
#define _NRDMA_H_

#include "utypes.h"

struct nrdma_mode {
	u32 reserved26 :6;
	u32 addr_oflow_err_log_en :1;
	u32 reserved18 :7;
	u32 pci_req_burst_len :2;
	u32 reserved14 :2;
	u32 attn_ens :12;
	u32 enable :1;
	u32 reset :1;
};

struct nrdma_status {
	u32 reserved11 :21;
	u32 malformed_or_poison_tlp_err_det :1;
	u32 rdma_local_mem_wr_longer_than_dma_len_err :1;
	u32 rdma_pci_fifo_oflow_err :1;
	u32 rdma_pci_fifo_urun_err :1;
	u32 rdma_pci_fifo_orun_err :1;
	u32 rdma_pci_host_addr_oflow_err :1;
	u32 dma_rd_comp_to :1;
	u32 comp_abort_err :1;
	u32 unsupp_req_err_det :1;
	u32 reserved0 :2;
};

struct nrdma_programmable_ipv6_extension_header {
	u32 hdr_type2_en :1;
	u32 hdr_type1_en :1;
	u32 reserved16 :14;
	u32 hdr_type2 :8;
	u32 hdr_type1 :8;
};

struct nrdma_rstates_debug {
	u32 reserved11 :21;
	u32 sdi_dr_wr :1;
	u32 dr_sdi_wr_ack :1;
	u32 non_lso_sel :1;
	u32 non_lso_q_full :1;
	u32 non_lso_busy :1;
	u32 rstate3 :2;
	u32 reserved3 :1;
	u32 rstate1 :3;
};

struct nrdma_rstate2_debug {
	u32 reserved5 :27;
	u32 rstate2 :5;
};

struct nrdma_bd_status_debug {
	u32 reserved3 :29;
	u32 bd_non_mbuf :1;
	u32 fst_bd_mbuf :1;
	u32 lst_bd_mbuf :1;
};

struct nrdma_req_ptr_debug {
	u32 ih_dmad_length :16;
	u32 reserved13 :3;
	u32 txmbuf_left :8;
	u32 rh_dmad_load_en :1;
	u32 rftq_d_dmad_pnt :2;
	u32 reserved0 :2;
};

struct nrdma_hold_d_dmad_debug {
	u32 reserved2 :30;
	u32 rhold_d_dmad :2;
};

struct nrdma_length_and_address_debug {
	u32 rdma_rd_length :16;
	u32 reserved6 :10;
	u32 mbuf_addr_idx :6;
};

struct nrdma_mbuf_byte_count_debug {
	u32 reserved4 :28;
	u32 rmbuf_byte_cnt :4;
};

struct nrdma_pcie_debug_status {
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

struct nrdma_pcie_dma_read_req_debug {
	u32 dr_pci_ad_hi :16;
	u32 dr_pci_ad_lo :16;
};

struct nrdma_pcie_dma_req_length_debug {
	u32 reserved16 :16;
	u32 rdma_len :16;
};

struct nrdma_fifo1_debug {
	u32 reserved9 :23;
	u32 c_write_addr :9;
};

struct nrdma_fifo2_debug {
	u32 reserved18 :14;
	u32 rlctrl_in :9;
	u32 c_read_addr :9;
};

struct nrdma_post_proc_pkt_req_cnt {
	u32 reserved8 :24;
	u32 pkt_req_cnt :8;
};

struct nrdma_mbuf_addr_debug {
	u32 reserved26 :6;
	u32 mactq_full :1;
	u32 txfifo_almost_urun :1;
	u32 tde_fifo_entry :8;
	u32 rcmp_head :16;
};

struct nrdma_tce_debug1 {
	u32 odi_state_out :4;
	u32 odi_state_in :4;
	u32 fifo_odi_data_code :2;
	u32 fifo_odi_data :22;
};

struct nrdma_tce_debug2 {
	u32 det_abort_cnt :8;
	u32 reserved0 :24;
};

struct nrdma_tce_debug3 {
	u32 reserved28 :4;
	u32 tx_pkt_cnt :8;
	u32 reserved17 :2;
	u32 tce_ma_req :1;
	u32 tce_ma_cmd_len :3; /* (3:0) ?? */
	u32 reserved0 :12;
};

struct nrdma_reserved_control {
	u32 txmbuf_margin_nlso :11;
	u32 reserved20 :1;
	u32 fifo_high_mark :8;
	u32 fifo_low_mark :8;
	u32 slow_clock_fix_dis :1;
	u32 en_hw_fix_25155 :1;
	u32 reserved1 :1;
	u32 select_fed_enable :1;
};

struct nrdma_flow_reserved_control {
	u32 reserved24 :8;
	u32 fifo_threshold_mbuf_req_msb :8;
	u32 mbuf_threshold_mbuf_req :8;
	u32 reserved4 :4;
	u32 fifo_hi_mark :1;
	u32 fifo_lo_mark :1;
	u32 reserved1 :1;
	u32 fifo_threshold_mbuf_req_lmsb :1;
};

struct nrdma_corruption_enable_control {
	u32 lcrc_dr_fix_en :1;
	u32 new_length_fix_en :1;
	u32 reserved22 :8;
	u32 cq51816_nlso_fix_en :1;
	u32 cq51036_nlso_fix_en :1;
	u32 reserved15 :5;
	u32 sbd_8b_less_fix_en3 :1;
	u32 sbd_8b_less_fix_en2 :1;
	u32 mem_too_large_fix_en2 :1;
	u32 mem_too_large_fix_en1 :1;
	u32 mem_too_large_fix_en :1;
	u32 sbd_9b_less_fix_en_fast_return :1;
	u32 sbd_9b_less_fix_en :1;
	u32 cq35774_hw_fix_en :1;
	u32 reserved :7;
};

struct nrdma_regs {
	struct nrdma_mode mode; 
	struct nrdma_status status; 
	struct nrdma_programmable_ipv6_extension_header programmable_ipv6_extension_header; 
	struct nrdma_rstates_debug rstates_debug; 
	
	struct nrdma_rstate2_debug rstate2_debug; 
	struct nrdma_bd_status_debug bd_status_debug; 
	struct nrdma_req_ptr_debug req_ptr_debug; 
	struct nrdma_hold_d_dmad_debug hold_d_dmad_debug; 
	
	struct nrdma_length_and_address_debug len_and_addr_debug; 
	struct nrdma_mbuf_byte_count_debug mbuf_byte_cnt_debug; 
	struct nrdma_pcie_debug_status pcie_debug_status; 
	struct nrdma_pcie_dma_read_req_debug pcie_dma_read_req_debug; 
	
	struct nrdma_pcie_dma_req_length_debug pcie_dma_req_length_debug; 
	struct nrdma_fifo1_debug fifo1_debug; 
	struct nrdma_fifo2_debug fifo2_debug; 
	u32 ofs_3c;

	struct nrdma_post_proc_pkt_req_cnt post_proc_pkt_req_cnt; 
	u32 ofs_44;
	u32 ofs_48;
	u32 ofs_4c;

	u32 ofs_50;
	u32 ofs_54;
	u32 ofs_58;
	u32 ofs_5c;

	struct nrdma_mbuf_addr_debug mbuf_addr_debug; 
	struct nrdma_tce_debug1 tce_debug1; 
	struct nrdma_tce_debug2 tce_debug2; 
	struct nrdma_tce_debug3 tce_debug3; 
	
	struct nrdma_reserved_control reserved_control; 
	struct nrdma_flow_reserved_control flow_reserved_control; 
	struct nrdma_corruption_enable_control corruption_enable_control; 
	struct ofs_7c;
};

#endif
