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

#ifndef _GRC_H_
#define _GRC_H_

struct grc_mode {
    u32 pcie_hi1k_en :1;
    u32 multi_cast_enable :1;
    u32 pcie_dl_sel :1;
    u32 int_on_flow_attn :1;
    u32 int_on_dma_attn :1;
    u32 int_on_mac_attn :1;
    u32 int_on_rxcpu_attn :1;
    u32 int_on_txcpu_attn :1;
    u32 receive_no_pseudo_header_cksum :1;
    u32 pcie_pl_sel :1;
    u32 nvram_write_enable :1;
    u32 send_no_pseudo_header_cksum :1;
    u32 time_sync_enable :1;
    u32 eav_mode_enable :1;
    u32 host_send_bds :1;
    u32 host_stack_up :1;
    u32 force_32bit_pci_bus_mode :1;
    u32 no_int_on_recv :1;
    u32 no_int_on_send :1;
    u32 dma_write_sys_attn :1;
    u32 allow_bad_frames :1;
    u32 no_crc :1;
    u32 no_frame_cracking :1;
    u32 split_hdr_mode :1;
    u32 cr_func_sel :2;
    u32 word_swap_data :1;
    u32 byte_swap_data :1;
    u32 reserved5 :1;
    u32 word_swap_bd :1;
    u32 byte_swap_bd :1;
    u32 int_send_tick :1;
};

struct grc_misc_config {
    u32 bond_id_7 :1;
    u32 bond_id_6 :1;
    u32 disable_grc_reset_on_pcie_block :1;
    u32 bond_id_5 :1;
    u32 bond_id_4 :1;
    u32 gphy_keep_power_during_reset :1;
    u32 reserved1 :1;
    u32 ram_powerdown :1;
    u32 reserved2 :1;
    u32 bias_iddq :1;
    u32 gphy_iddq :1;
    u32 powerdown :1;
    u32 vmain_prsnt_state :1;
    u32 power_state :2;
    u32 bond_id_3 :1;
    u32 bond_id_2 :1;
    u32 bond_id_1 :1;
    u32 bond_id_0 :1;
    u32 reserved3 :5;
    u32 timer_prescaler :7;
    u32 grc_reset :1;
};

struct grc_misc_local_control {
    u32 wake_on_link_up :1;
    u32 wake_on_link_down :1;
    u32 disable_traffic_led_fix :1;
    u32 reserved :2;
    u32 pme_assert :1;
    u32 reserved1 :1;
    u32 auto_seeprom :1;
    u32 reserved2 :1;
    u32 ctrl_ssram_type :1;
    u32 bank_select :1;
    u32 reserved3 :3;
    u32 enable_ext_memory :1;
    u32 gpio2_output :1;
    u32 gpio1_output :1;
    u32 gpio0_output :1;
    u32 gpio2_output_enable :1;
    u32 gpio1_output_enable :1;
    u32 gpio0_output_enable :1;
    u32 gpio2_input :1;
    u32 gpio1_input :1;
    u32 gpio0_input :1;
    u32 reserved4 :2;
    u32 energy_detection_pin :1;
    u32 uart_disable :1;
    u32 interrupt_on_attention :1;
    u32 set_interrupt :1;
    u32 clear_interrupt :1;
    u32 interrupt_state :1;
};

struct grc_cpu_event {
    union {
        struct {
            u32 flash :1;
            u32 vpd :1;
            u32 timer :1;
            u32 sw_event_11 :1;
            u32 flow_attn :1;
            u32 rx_cpu_attn :1;
            u32 emac :1;
            u32 reserved24 :1;
            u32 sw_event_10 :1;
            u32 hi_prio_mbox :1;
            u32 low_prio_mbox :1;
            u32 dma_attn :1;
            u32 sw_event_9 :1;
            u32 hi_dma_rd :1;
            u32 hi_dma_wr :1;
            u32 sw_event_8 :1;
            u32 host_coalescing :1;
            u32 sw_event_7 :1;
            u32 receive_data_comp :1;
            u32 sw_event_6 :1;
            u32 rx_sw_queue :1;
            u32 dma_rd :1;
            u32 dma_wr :1;
            u32 rdiq :1;
            u32 sw_event_5 :1;
            u32 recv_bd_comp :1;
            u32 sw_event_4 :1;
            u32 recv_list_selector :1;
            u32 sw_event_3 :1;
            u32 recv_list_placement :1;
            u32 sw_event_1 :1;
            u32 sw_event_0 :1;
        };
        u32 word;
    };
};

struct grc_cpu_semaphore {
    u32 reserved :31;
    u32 semaphore :1;
};

struct grc_pcie_misc_status {
    u32 reserved :8;
    u32 p1_pcie_ack_fifo_underrun :1;
    u32 p0_pcie_ack_fifo_underrun :1;
    u32 p1_pcie_ack_fifo_overrun :1;
    u32 p0_pcie_ack_fifo_overrun :1;
    u32 reserved2 :3;
    u32 pcie_link_in_l23 :1;
    u32 f0_pcie_powerstate :2;
    u32 f1_pcie_powerstate :2;
    u32 f2_pcie_powerstate :2;
    u32 f3_pcie_powerstate :2;
    u32 pcie_phy_attn :4;
    u32 pci_grc_intb_f3 :1;
    u32 pci_grc_intb_f2 :1;
    u32 pci_grc_intb_f1 :1;
    u32 pci_grc_inta :1;
};

struct grc_cpu_event_enable {
    union {
        struct {
            u32 flash :1;
            u32 vpd :1;
            u32 timer :1;
            u32 rom :1;
            u32 hc_module :1;
            u32 rx_cpu_module :1;
            u32 emac :1;
            u32 memory_map_enable :1;
            u32 reserved23 :1;
            u32 high_prio_mbox :1;
            u32 low_prio_mbox :1;
            u32 dma :1;
            u32 reserved19 :1;
            u32 reserved18 :1;
            u32 reserved17 :1;
            u32 asf_location_15 :1;
            u32 tpm_interrupt_enable :1;
            u32 asf_location_14 :1;
            u32 reserved13 :1;
            u32 asf_location_13 :1;
            u32 unused_sdi :1;
            u32 sdc :1;
            u32 sdi :1;
            u32 rdiq :1;
            u32 asf_location_12 :1;
            u32 reserved6 :1;
            u32 asf_location_11 :1;
            u32 reserved4 :1;
            u32 asf_location_10 :1;
            u32 reserved2 :1;
            u32 asf_location_9 :1;
            u32 asf_location_8 :1;
        };
        u32 word;
    };
};

struct grc_secfg_1 {
    u32 cr_vddio_30v_reg_out_adj :4;
    u32 cr_vddio_18v_reg_out_adj :4;
    u32 si_eedata_pin_str_ctrl :3;
    u32 so_pin_str_ctrl :3;
    u32 sclk_pin_str_ctrl :3;
    u32 so_pin_str_ctrl2 :3;
    u32 flash_led_pin_sharing_ctrl :1;
    u32 sd_clk_pull_up_ctrl :1;
    u32 xd_r_b_n_pull_up_ctrl :1;
    u32 gpio0_sd_bus_pow_ctrl :1;
    u32 sd_bus_pow_led_ctrl :1;
    u32 sd_led_output_mode_ctrl :2;
    u32 sd_bus_pow_output_pol_ctrl :1;
    u32 sd_write_protect_pol_ctrl :1;
    u32 sd_mmc_card_detect_pol_ctrl :1;
    u32 mem_stk_ins_pol_ctrl :1;
    u32 xd_picture_card_det_pol_ctrl :1;
};

struct grc_secfg_2 {
    u32 reserved :24;
    u32 sd_write_prot_int_pu_pd_ovrd_ctrl :2;
    u32 reserved2 :2;
    u32 mem_stk_ins_int_pu_pd_ovrd_ctrl :2;
    u32 xd_picture_card_det_pu_pd_ovrd_ctrl :2;
};

struct grc_bond_id {
    u32 serdes_l0_exit_lat_sel :2;
    u32 umc_bg_wa :1;
    u32 uart_enable :1;
    u32 eav_disable :1;
    u32 sedata_oe_ctrl :1;
    u32 disable_auto_eeprom_reset :1;
    u32 eee_lpi_enable_hw_default :1;
    u32 pcie_gen2_mode :1;
    u32 vaux_prsnt :2;
    u32 non_cr_sku :1;
    u32 disable_gigabit :1;
    u32 disable_led_pin_sharing :1;
    u32 cr_regulator_power_down :1;
    u32 bond_id :17;
};

struct grc_clock_ctrl {
    u32 pl_clock_disable :1;
    u32 dll_clock_disable :1;
    u32 tl_clock_disable :1;
    u32 pci_express_clock_to_core_clock :1;
    u32 reserved1 :1;
    u32 reserved2 :1;
    u32 reserved3 :1;
    u32 reserved4 :1;
    u32 reserved5 :1;
    u32 reserved6 :1;
    u32 reserved7 :1;
    u32 select_final_alt_clock_src :1;
    u32 slow_core_clock_mode :1;
    u32 led_polarity :1;
    u32 bist_function_ctrl :1;
    u32 asynchronous_bist_reset :1;
    u32 reserved8 :2;
    u32 select_alt_clock_src :1;
    u32 select_alt_clock :1;
    u32 reserved9 :2;
    u32 core_clock_disable :1;
    u32 reserved10 :1;
    u32 reserved11 :1;
    u32 reserved12 :2;
    u32 reserved13 :5;
};

struct grc_misc_control {
	u32 done_dr_fix4_en :1;
	u32 done_dr_fix3_en :1;
	u32 done_dr_fix2_en :1;
	u32 done_dr_fix_en :1;
	u32 clkreq_delay_dis :1;
	u32 lcrc_dr_fix2_en :1;
	u32 lcrc_dr_fix_en :1;
	u32 chksum_fix_en :1;
	u32 ma_addr_fix_en :1;
	u32 ma_prior_en :1;
	u32 underrun_fix_en :1;
	u32 underrun_clear :1;
	u32 overrun_clear :1;
	u32 reserved0 :19;
};

struct grc_fastboot_program_counter {
	u32 enable :1;
	u32 addr :31;
};

struct grc_power_management_debug {
	u32 pclk_sw_force_override_en :1;
	u32 pclk_sw_force_override_val :1;
	u32 pclk_sw_sel_override_en :1;
	u32 pclk_sw_sel_override_val :1;
	u32 pclk_sw_force_cond_a_dis :1;
	u32 pclk_sw_force_cond_b_dis :1;
	u32 pclk_sw_force_cond_c_en :1;
	u32 pclk_sw_sel_cond_a_dis :1;
	u32 pclk_sw_sel_cond_b_dis :1;
	u32 pclk_sw_sel_cond_c_dis :1;
	u32 reserved17 :5;
	u32 perst_override :1;
	u32 reserved6 :10;
	u32 pipe_clkreq_serdes :1;
	u32 pipe_aux_power_down :1;
	u32 pll_power_down :1;
	u32 clock_req_output_stat :1;
	u32 reserved1 :1;
	u32 pll_is_up :1;
};

struct grc_regs {
    struct grc_mode mode;
    struct grc_misc_config misc_config;
    struct grc_misc_local_control misc_local_control;
    u32 timer;

    struct grc_cpu_event rxcpu_event;
    u32 rxcpu_timer_reference;
    struct grc_cpu_semaphore rxcpu_semaphore;
    struct grc_pcie_misc_status pcie_misc_status;

    u32 card_reader_dma_read_policy;
    u32 card_reader_dma_write_policy;
    u32 ofs_28;
    u32 ofs_2c;

    u32 ofs_30;
    u32 ofs_34;
    u32 ofs_38;
    u32 ofs_3c;

    u32 ofs_40;
    u32 ofs_44;
    u32 ofs_48;
    struct grc_cpu_event_enable rxcpu_event_enable;

    u32 ofs_50;
    u32 ofs_54;
    u32 ofs_58;
    u32 ofs_5c;

    u32 ofs_60;
    u32 ofs_64;
    u32 ofs_68;
    u32 ofs_6c;

    u32 ofs_70;
    u32 ofs_74;
    u32 ofs_78;
    u32 ofs_7c;

    struct grc_secfg_1 secfg1;
    struct grc_secfg_2 secfg2;
    struct grc_bond_id bond_id;
    struct grc_clock_ctrl clock_ctrl;

    struct grc_misc_control misc_control;
    struct grc_fastboot_program_counter fastboot_pc;
    u32 ofs_98;
    u32 ofs_9c;

    u32 ofs_a0;
    struct grc_power_management_debug power_management_debug;
    u32 ofs_a8;
    u32 ofs_ac;
};

#endif
