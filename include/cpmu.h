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

#ifndef _CPMU_H_
#define _CPMU_H_

struct cpmu_control {
    u32 reserved1 :1;
    u32 reserved2 :1;
    u32 reserved3 :1;
    u32 always_force_gphy_dll_on :1;
    u32 enable_gphy_powerdown_in_dou :1;
    u32 reserved4 :1;
    u32 reserved5 :1;
    u32 reserved6 :1;
    u32 reserved7 :1;
    u32 reserved8 :1;
    u32 media_sense_power_mode_enable :1;
    u32 reserved9 :1;
    u32 legacy_timer_enable :1;
    u32 frequency_multiplier_enable :1;
    u32 gphy_10mb_receive_only_mode_enable :1;
    u32 play_dead_mode_enable :1;
    u32 link_speed_power_mode_enable :1;
    u32 hide_pcie_function :3;
    u32 link_aware_power_mode_enable :1;
    u32 link_idle_power_mode_enable :1;
    u32 card_reader_idle_enable :1;
    u32 card_read_iddq :1;
    u32 lan_iddq :1;
    u32 reserved10 :3;
    u32 power_down :1;
    u32 register_software_reset :1;
    u32 software_reset :1;
};

struct cpmu_clock {
    u32 reserved :11;
    u32 mac_clock_switch :5;
    u32 reserved2 :16;
};

struct cpmu_override {
    u32 reserved :18;
    u32 mac_clock_speed_override_enable :1;
    u32 reserved2 :13;
};

struct cpmu_status {
    u32 reserved :9;
    u32 wol_acpi_detection_enabled :1;
    u32 wol_magic_packet_detection_enabled :1;
    u32 ethernet_link :2;
    u32 link_idle :1;
    u32 reserved2 :2;
    u32 reserved3 :2;
    u32 vmain_power :1;
    u32 iddq :3;
    u32 power_state :2;
    u32 energy_detect :1;
    u32 cpmu_power :3;
    u32 pm_state_machine_state :4;
};

struct cpmu_pcie_status {
    u32 dl_active :1;
    u32 debug_vector_sel_2 :4;
    u32 debug_vector_2 :11;
    u32 phylinkup :1;
    u32 debug_vector_sel_1 :4;
    u32 debug_vector_1 :11;
};

struct cpmu_padring_control {
    u32 power_sm_or_state :4;
    u32 power_sm_override :1;
    u32 cr_io_hys_en :1;
    u32 cr_activity_led_en :1;
    u32 switching_regulator_power_off_option :1;
    u32 cr_bus_power_dis :1;
    u32 unknown :3;
    u32 pcie_serdes_pll_tuning_bypass :1;
    u32 pcie_serdes_lfck_rx_select_cnt0 :1;
    u32 pcie_serdes_lfck_rx_select_refclk :1;
    u32 reserved :1;
    u32 clkreq_l_in_low_power_mode_improvement :1;
    u32 cq31984_opt_2_fix_disable :1;
    u32 serdes_standalone_mode :1;
    u32 pipe_standalone_mode_control :1;
    u32 cq31984_opt_4_fix_enable :1;
    u32 cq31177_fix_disable :1;
    u32 cq30674_fix_enable :1;
    u32 chicken_bit_for_cq31116 :1;
    u32 cq31984_opt_3_fix_disable :1;
    u32 disable_default_gigabit_advertisement :1;
    u32 enable_gphy_reset_on_perst_l_deassertion :1;
    u32 cq39842_fix_disable :1;
    u32 cq39544_fix_disable :1;
    u32 reserved2 :1;
    u32 eclk_switch_using_link_status_disable :1;
    u32 perst_l_pad_hysteris_enable :1;
};

/* etc */

struct cpmu_regs {
    struct cpmu_control control;
    struct cpmu_clock no_link_or_10mb_policy;
    struct cpmu_clock megabit_policy;
    struct cpmu_clock gigabit_policy;

    struct cpmu_clock link_aware_policy;
    struct cpmu_clock d0u_policy;
    struct cpmu_clock link_idle_policy;
    u32 ofs_1c;
    
    u32 ofs_20;
    struct cpmu_clock override_policy;
    struct cpmu_override override_enable;
    struct cpmu_status status;
    
    struct cpmu_clock clock_status;
    struct cpmu_pcie_status pcie_status;
    u32 gphy_control_status;
    u32 ram_control;
    
    u32 cr_idle_detect_debounce_ctrl;
    u32 eee_debug;
    u32 core_idle_detect_debounce_ctrl;
    u32 pcie_idle_detect_debounce_ctrl;
    
    u32 energy_detect_debounce_timer;
    u32 dll_lock_timer;
    u32 chip_id;
    u32 mutex_request;
    
    u32 mutex_grant;
    u32 ofs_64;
    struct cpmu_padring_control padring_control;
    u32 ofs_6c;

    u32 link_idle_control;
    u32 link_idle_status;
    u32 play_dead_mode_iddq_debounce_control;
    u32 top_misc_control_1;

    u32 debug_bus;
    u32 debug_select;
    u32 ofs_88;
    u32 ofs_8c;

    u32 ltr_control;
    u32 ofs_94;
    u32 ofs_98;
    u32 ofs_9c;
    
    u32 swregulator_control_1;
    u32 swregulator_control_2;
    u32 swregulator_control_3;
    u32 misc_control;

    u32 eee_mode;
    u32 eee_debounce_timer1_control;
    u32 eee_debounce_timer2_control;
    u32 eee_link_idle_control;

    u32 eee_link_idle_status;
    u32 eee_statistic_counter_1;
    u32 eee_statistic_counter_2;
    u32 eee_statistic_counter_3;

    u32 eee_control;
    u32 current_measurement_control;
    u32 current_measurement_read_upper;
    u32 current_measurement_read_lower;

    u32 card_reader_idle_control;
    u32 card_reader_clock_policy;
    u32 card_reader_clock_status;
    u32 ofs_ec;

    u32 pll_control_1;
    u32 pll_control_2;
    u32 pll_control_3;
    u32 clock_gen_control;

    /* etc */
};

#endif
