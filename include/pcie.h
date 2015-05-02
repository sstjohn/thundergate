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

#ifndef _PCIE_H_
#define _PCIE_H_

struct pcie_tl_regs {
    u32 tlp_control;
    u32 transaction_config;
    u32 ofs_08;
    u32 ofs_0c;

    u32 wdma_req_upper_addr_diag;
    u32 wdma_req_lower_addr_diag;
    u32 wdma_length_byte_enable_req_diag;
    u32 rdma_req_upper_addr_diag;

    u32 rdma_req_lower_addr_diag;
    u32 rdma_length_req_diag;
    u32 msi_dma_req_upper_addr_diag;
    u32 msi_dma_req_lower_addr_diag;

    u32 msi_dma_length_req_diag;
    u32 slave_req_length_type_diag;
    u32 flow_control_inputs_diag;
    u32 xmt_state_machines_and_gated_reqs_diag;

    u32 address_ack_xfer_count_and_arb_length_diag;
    u32 dma_completion_header_diag_0;
    u32 dma_completion_header_diag_1;
    u32 dma_completion_header_diag_2;

    u32 dma_completion_misc_diag_0;
    u32 dma_completion_misc_diag_1;
    u32 dma_completion_misc_diag_2;
    u32 split_controller_req_length_address_ack_remaining_diag;

    u32 split_controller_misc_diag_0;
    u32 split_controller_misc_diag_1;
    u32 tlp_bus_dev_func_num;
    u32 tlp_debug;

    u32 retry_buffer_free;
    u32 target_debug_1;
    u32 target_debug_2;
    u32 target_debug_3;

    u32 target_debug_4;
};

struct pcie_dl_regs {
    u32 dl_control;
    u32 dl_status;
    u32 dl_attention;
    u32 dl_attention_mask;

    u32 next_transmit_seq_no;
    u32 acked_transmit_seq_no;
    u32 purged_transmit_seq_no;
    u32 receive_req_no;

    u32 dl_replay;
    u32 dl_ack_timeout;
    u32 power_mgmt_threshold;
    u32 retry_buffer_write_ptr;

    u32 retry_buffer_read_ptr;
    u32 retry_buffer_purged_ptr;
    u32 retry_buffer_read_write_debug_port;
    u32 error_count_threshold;

    u32 tlp_error_counter;
    u32 dllp_error_counter;
    u32 nak_received_counter;
    u32 data_link_test;

    u32 packet_bist;
    u32 link_pcie_1_1_control;
};

struct pcie_pl_regs {
    u32 phy_mode;
    u32 phy_link_status;
    u32 phy_link_ltssm_control;
    u32 phy_link_training_link_number;
    
    u32 phy_link_training_lane_number;
    u32 phy_link_training_n_fts;
    u32 phy_attention;
    u32 phy_attention_mask;

    u32 phy_receive_error_counter;
    u32 phy_receive_framing_error_counter;
    u32 phy_receive_error_threshold;
    u32 phy_test_control;

    u32 phy_serdes_control_override;
    u32 phy_timing_parameter_override;
    u32 phy_hardware_diag_1;
    u32 phy_hardware_diag_2;
};

#endif
