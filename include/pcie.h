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

struct pcie_tl_wdma_len_byte_en_req_diag {
	u32 request_length :16;
	u32 byte_enables :8;
	u32 reserved1 :7;
	u32 raw_request :1;
};

struct pcie_tl_rdma_len_req_diag {
	u32 request_length :16;
	u32 reserved1 :15;
	u32 raw_request :1;
};

struct pcie_tl_msi_len_req_diag {
	u32 request_length :16;
	u32 reserved1 :15;
	u32 raw_request :1;
};

struct pcie_tl_slave_req_len_type_diag {
	u32 reg_slv_len_req :6;
	u32 request_length :10;
	u32 reserved2 :14;
	u32 request_type :1;
	u32 raw_request :1;
};

struct pcie_tl_flow_control_inputs_diag {
	u32 reg_fc_input :5;
	u32 non_posted_header_avail :1;
	u32 posted_header_avail :1;
	u32 completion_header_avail :1;
	u32 posted_data_avail :12;
	u32 completion_data_avail :12;
};

struct pcie_tl_xmt_state_machines_gated_reqs_diag {
	u32 reg_sm_r0_r3 :1;
	u32 tlp_tx_data_state_machine :3;
	u32 tlp_tx_arb_state_machine :4;
	u32 reserved4 :20;
	u32 slave_dma_gated_req :1;
	u32 msi_dma_gated_req :1;
	u32 read_dma_gated_req :1;
	u32 write_dma_gated_req :1;
};

struct pcie_tl_tlp_bdf {
	u32 reserved17 :15;
	u32 config_write_indicator :1;
	u32 bus :8;
	u32 device :5;
	u32 function :3;
};

struct pcie_tl_regs {
    struct pcie_tl_tlp_ctrl tlp_ctrl;
    struct pcie_tl_transaction_config transaction_config;
    u32 ofs_08;
    u32 ofs_0c;

    u32 wdma_req_upper_addr_diag;
    u32 wdma_req_lower_addr_diag;
    struct pcie_tl_wdma_len_byte_en_req_diag wdma_len_byte_en_req_diag;
    u32 rdma_req_upper_addr_diag;

    u32 rdma_req_lower_addr_diag;
    struct pcie_tl_rdma_len_req_diag rdma_len_req_diag;
    u32 msi_dma_req_upper_addr_diag;
    u32 msi_dma_req_lower_addr_diag;

    struct pcie_tl_msi_len_req_diag msi_dma_len_req_diag;
    struct pcie_tl_slave_req_len_type_diag slave_req_len_type_diag;
    struct pcie_tl_flow_control_inputs_diag flow_control_inputs_diag;
    struct pcie_tl_xmt_state_machines_gated_reqs_diag xmt_state_machines_gated_reqs_diag;

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
    struct pcie_tl_tlp_bdf bdf;
    u32 tlp_debug;

    u32 retry_buffer_free;
    u32 target_debug_1;
    u32 target_debug_2;
    u32 target_debug_3;

    u32 target_debug_4;
};

struct pcie_dl_ctrl {
	u32 reserved19 :13;
	u32 pll_refsel_sw :1;
	u32 reserved17 :1;
	u32 power_management_ctrl_en :1;
	u32 power_down_serdes_transmitter :1;
	u32 power_down_serdes_pll :1;
	u32 power_down_serdes_receiver :1;
	u32 enable_beacon :1;
	u32 automatic_timer_threshold_en :1;
	u32 dllp_timeout_mech_en :1;
	u32 chk_rcv_flow_ctrl_credits :1;
	u32 link_enable :1;
	u32 power_management_ctrl :8;
};

struct pcie_dl_status {
	u32 reserved26 :6;
	u32 phy_link_state :3;
	u32 power_management_state :4;
	u32 power_management_substate :2;
	u32 data_link_up :1;
	u32 reserved11 :5;
	u32 pme_turn_off_status_in_d0 :1;
	u32 flow_ctrl_update_timeout :1;
	u32 flow_ctrl_recv_oflow :1;
	u32 flow_ctrl_proto_err :1;
	u32 data_link_proto_err :1;
	u32 replay_rollover :1;
	u32 replay_timeout :1;
	u32 nak_recvd :1;
	u32 dllp_error :1;
	u32 bad_tlp_seq_no :1;
	u32 tlp_error :1;
};

struct pcie_dl_attn {
	u32 reserved5 :27;
	u32 data_link_layer_attn_ind :1;
	u32 nak_rcvd_cntr_attn_ind :1;
	u32 dllp_err_cntr_attn_ind :1;
	u32 tlp_bad_seq_cntr_attn_ind :1;
	u32 tlp_err_cntr_attn_ind :1;
};

struct pcie_dl_attn_mask {
	u32 reserved8 :24;
	u32 attn_mask :3;
	u32 data_link_layer_attn_mask :1;
	u32 nak_rcvd_cntr_attn_mask :1;
	u32 dllp_err_cntr_attn_mask :1;
	u32 tlp_bad_seq_cntr_attn_mask :1;
	u32 tlp_err_cntr_attn_mask :1;
};

struct pcie_dl_seq_no {
	u32 reserved12 :20;
	u32 value :12;
};

struct pcie_dl_replay {
	u32 reserved23 :9;
	u32 timeout_value :13;
	u32 buffer_size :10;
};

struct pcie_dl_ack_timeout {
	u32 reserved11 :21;
	u32 value :11;
};

struct pcie_dl_pm_threshold {
	u32 reserved24 :8;
	u32 l0_stay_time :4;
	u32 l1_stay_time :4;
	u32 l1_threshold :8;
	u32 l0s_threshold :8;
};

struct pcie_dl_retry_buffer_ptr {
	u32 reserved11 :21;
	u32 value :11;
};

struct pcie_dl_test {
	u32 reserved16 :16;
	u32 store_recv_tlps :1;
	u32 disable_tlps :1;
	u32 disable_dllps :1;
	u32 force_phy_link_up :1;
	u32 bypass_flow_ctrl :1;
	u32 ram_core_clock_margin_test_en :1;
	u32 ram_overstress_test_en :1;
	u32 ram_read_margin_test_en :1;
	u32 speed_up_completion_timer :1;
	u32 speed_up_replay_timer :1;
	u32 speed_up_ack_latency_timer :1;
	u32 speed_up_pme_service_timer :1;
	u32 force_purge :1;
	u32 force_retry :1;
	u32 invert_crc :1;
	u32 send_bad_crc_bit :1;
};

struct pcie_dl_packet_bist {
	u32 reserved24 :8;
	u32 packet_checker_loaded :1;
	u32 recv_mismatch :1;
	u32 rand_tlp_len_en :1;
	u32 tlp_len :11;
	u32 random_ipg_len_en :1;
	u32 ipg_len :7;
	u32 transmit_start :1;
	u32 packet_generator_test_mode_en :1;
};

struct pcie_dl_regs {
    struct pcie_dl_ctrl dl_ctrl;
    struct pcie_dl_status dl_status;
    struct pcie_dl_attn dl_attn;
    struct pcie_dl_attn_mask dl_attn_mask;

    struct pcie_dl_seq_no next_transmit_seq_no;
    struct pcie_dl_seq_no acked_transmit_seq_no;
    struct pcie_dl_seq_no purged_transmit_seq_no;
    struct pcie_dl_seq_no receive_req_no;

    struct pcie_dl_replay replay;
    struct pcie_dl_ack_timeout ack_timeout;
    struct pcie_dl_pm_threshold power_mgmt_threshold;
    struct pcie_dl_retry_buffer_ptr retry_buffer_write_ptr;

    struct pcie_dl_retry_buffer_ptr retry_buffer_read_ptr;
    struct pcie_dl_retry_buffer_ptr retry_buffer_purged_ptr;
    u32 retry_buffer_read_write_debug_port;
    u32 error_count_threshold;

    u32 tlp_error_counter;
    u32 dllp_error_counter;
    u32 nak_received_counter;
    struct pcie_dl_test test;

    struct pcie_dl_packet_bist packet_bist;
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
