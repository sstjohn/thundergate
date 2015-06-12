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

struct pcie_tl_tlp_ctrl {
	u32 excessive_current_fix_en :1;
	u32 reserved30 :1;
	u32 int_mode_fix_en :1;
	u32 reserved28 :1;
	u32 unexpected_completion_err_fix_en :1;
	u32 type1_vendor_defined_msg_fix_en :1;
	u32 data_fifo_protect :1;
	u32 address_check_en :1;
	u32 tc0_check_en :1;
	u32 crc_swap :1;
	u32 ca_err_dis :1;
	u32 ur_err_dis :1;
	u32 rsv_err_dis :1;
	u32 mps_chk_en :1;
	u32 ep_err_dis :1;
	u32 bytecount_chk_en :1;
	u32 reserved14 :2;
	u32 dma_read_traffic_class :3;
	u32 dma_write_traffic_class :3;
	u32 reserved6 :2;
	u32 completion_timeout :6;
};

struct pcie_tl_transaction_config {
	u32 retry_buffer_timining_mod_en :1;
	u32 reserved30 :1;
	u32 one_shot_msi_en :1;
	u32 reserved28 :1;
	u32 select_core_clock_override :1;
	u32 cq9139_fix_en :1;
	u32 cmpt_pwr_check_en :1;
	u32 cq12696_fix_en :1;
	u32 device_serial_no_override :1;
	u32 cq12455_fix_en :1;
	u32 tc_vc_filtering_check_en :1;
	u32 dont_gen_hot_plug_msg :1;
	u32 ignore_hot_plug_msg :1;
	u32 msi_multimsg_cap :3;
	u32 data_select_limit :4;
	u32 pcie_1_1_pl_en :1;
	u32 pcie_1_1_dl_en :1;
	u32 pcie_1_1_tl_en :1;
	u32 reserved7 :2;
	u32 pcie_power_budget_cap_en :1;
	u32 lom_configuration :1;
	u32 concate_select :1;
	u32 ur_status_bit_fix_en :1;
	u32 vendor_defined_msg_fix_en :1;
	u32 power_state_write_mem_enable :1;
	u32 reserved0 :1;
};

struct pcie_tl_regs {
    struct pcie_tl_tlp_ctrl tlp_ctrl;
    struct pcie_tl_transaction_config transaction_config;
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
