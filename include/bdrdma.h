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

#ifndef _BDRDMA_H_
#define _BDRDMA_H_

#include "utypes.h"

struct bdrdma_mode {
    u32 reserved26 :6;
    u32 addr_oflow_err_log_en :1;
    u32 reserved18 :7;
    u32 pci_req_burst_len :2;

    u32 reserved14 :2;
    u32 attention_enables :12;
    u32 enable :1;
    u32 reserved0 :1;
};

struct bdrdma_status {
    u32 reserved10 :21;
    u32 malformed_tlp_or_poison_tlp_err_det :1;
    u32 local_mem_wr_longer_than_dma_len_err :1;
    u32 pci_fifo_overread_err :1;
    u32 pci_fifo_underread_err :1;
    u32 pci_fifo_overrun_err :1;
    u32 pci_host_addr_oflow_err :1;
    u32 dma_rd_compltn_timeout :1;
    u32 compltn_abrt_err :1;
    u32 unsup_req_err_det :1;
    u32 reserved0 :2;
};

struct bdrdma_len_dbg {
    u32 rdmad_length_b_2 :16;
    u32 rdmad_length_b_1 :16;
};

struct bdrdma_rstates_dbg {
    u32 rbdi_cnt :16;
    u32 reserved2 :14;
    u32 rstate1 :2;
};

struct bdrdma_rstate2_dbg {
    u32 host_addr :28;
    u32 rstate2 :4;
};

struct bdrdma_bd_status_dbg {
    u32 rlctrl :9;
    u32 dmad_load_and_mem_ok :1;
    u32 int_rh_dmad_load :1;
    u32 rh_dmad_load_fst :1;
    u32 rh_dmad_done_syn3 :1;
    u32 rh_dmad_load_en :1;
    u32 rh_dmad_no_empty :1;
    u32 hold_dmad_n_empty :1;
  
    u32 rwr_ptr :2;
    u32 rrd_ptr :2;
    u32 dmad_pnt2 :2;
    u32 dmad_pnt1 :2;
    u32 dmad_pnt0 :2;
    u32 dmad_pnt :2;
    u32 reserved3 :1;
    u32 bd_non_mbuf :1;
    u32 fst_bd_mbuf :1;
    u32 lst_bd_mbuf :1;
};

struct bdrdma_req_ptr_dbg {
    u32 ih_dmad_len :16;
    u32 reserved13 :3;
    u32 txmbuf_left :8;
    u32 rh_dmad_load_en :1;
    u32 rftq_d_dmad_pnt :2;
    u32 rftq_b_dmad_pnt :2;
};

struct bdrdma_hold_d_dmad_dbg {
    u32 reserved4 :28;
    u32 rhold_b_dmad :2;
    u32 reserved0 :2;
};

struct bdrdma_len_and_addr_idx_dbg {
    u32 rdma_rd_length :16;
    u32 reserved0 :16;
};

struct bdrdma_addr_idx_dbg {
    u32 reserved5 :23;
    u32 h_host_addr_i :5;
};

struct bdrdma_pcie_dbg_status {
    u32 lt_term :4;
    u32 reserved27 :1;
    u32 lt_too_lg :1;
    u32 lt_dma_reload :1;
    u32 lt_dma_good :1;
    u32 cur_trans_active :1;
    u32 dr_pci_req :1;
    u32 dr_pci_word_swap :1;
    u32 dr_pci_byte_swap :1;
    u32 new_slow_core_clk_mode :1;
    u32 rbd_non_mbuf :1;
    u32 rfst_bd_mbuf :1;
    u32 rlsd_bd_mbuf :1;
    u32 dr_pci_len :16;
};

struct bdrdma_pcie_dma_rd_req_addr_dbg {
    u32 dr_pci_ad_hi :16;
    u32 dr_pci_ad_lo :16;
};

struct bdrdma_pcie_dma_req_len_dbg {
    u32 reserved16 :16;
    u32 rdma_len :16;
};

struct bdrdma_fifo1_dbg {
    u32 reserved9 :23;
    u32 c_write_addr :9;
};

struct bdrdma_fifo2_dbg {
    u32 reserved18 :14;
    u32 rlctrl_in :9;
    u32 c_read_addr :9;
};

struct bdrdma_rsvrd_ctrl {
    u32 reserved21 :11;
    u32 sel_fed_en_bd :1;
    u32 fifo_high_mark_bd :8;
    u32 fifo_low_mark_bd :8;
    u32 slow_clock_fix_dis_bd :1;
    u32 hw_fix_cq25155_en :1;
    u32 reserved0 :2;
};

struct bdrdma_regs {
    struct bdrdma_mode mode;
    struct bdrdma_status status;
    struct bdrdma_len_dbg len_dbg;
    struct bdrdma_rstates_dbg rstates_dbg;
    
    struct bdrdma_rstate2_dbg rstate2_dbg;
    struct bdrdma_bd_status_dbg bd_status_dbg;
    struct bdrdma_req_ptr_dbg req_ptr_dbg;
    struct bdrdma_hold_d_dmad_dbg hold_d_dmad_dbg;

    struct bdrdma_len_and_addr_idx_dbg len_and_addr_idx_dbg;
    struct bdrdma_addr_idx_dbg addr_idx_dbg;
    struct bdrdma_pcie_dbg_status pcie_dbg_status;
    struct bdrdma_pcie_dma_rd_req_addr_dbg pcie_dma_rd_req_addr_dbg;
    
    struct bdrdma_pcie_dma_req_len_dbg pcie_dma_req_len_dbg;
    struct bdrdma_fifo1_dbg fifo1_dbg;
    struct bdrdma_fifo2_dbg fifo2_dbg;
    u32 ofs_3c;

    u32 ofs_40;
    u32 ofs_44;
    u32 ofs_48;
    u32 ofs_4c;

    u32 ofs_50;
    u32 ofs_54;
    u32 ofs_58;
    u32 ofs_5c;

    u32 ofs_60;
    u32 ofs_64;
    u32 ofs_68;
    u32 ofs_6c;

    u32 bdrdma_reserved_cntrl;
    u32 bdrdma_flow_reserved_cntrl;
    u32 bdrdma_corruption_en_ctrl;
    u32 ofs_7c;
};

#endif
