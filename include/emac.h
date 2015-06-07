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

#ifndef _EMAC_H_
#define _EMAC_H_

#include "../include/utypes.h"

struct emac_mode {
    u32 ext_magic_pkt_en :1;
    u32 magic_pkt_free_running_mode_en :1;
    u32 mac_loop_back_mode_ctrl :1;
    u32 en_ape_tx_path :1;
    u32 en_ape_rx_path :1;
    u32 free_running_acpi :1;
    u32 halt_interesting_packets_pme :1;
    u32 keep_frame_in_wol :1;
    u32 en_fhde :1;
    u32 en_rde :1;
    u32 en_tde :1;
    u32 reserved20 :1;
    u32 acpi_power_on :1;
    u32 magic_packet_detection :1;
    u32 send_config_command :1;
    u32 flush_tx_statistics :1;
    u32 clear_tx_statistics :1;
    u32 en_tx_statistics :1;
    u32 flush_rx_statistics :1;
    u32 clear_rx_statistics :1;
    u32 en_rx_statistics :1;
    u32 reserved10 :1;
    u32 max_defer :1;
    u32 en_tx_bursting :1;
    u32 tagged_mac_control :1;
    u32 reserved5 :2;
    u32 loopback :1;
    u32 port_mode :2;
    u32 half_duplex :1;
    u32 global_reset :1;
};

struct emac_status {
    u32 reserved29 :3;
    u32 interesting_packet_pme_attention :1;
    u32 tx_statistic_overrun :1;
    u32 rx_statistic_overrun :1;
    u32 odi_error :1;
    u32 ap_error :1;
    u32 mii_interrupt :1;
    u32 mii_completion :1;
    u32 reserved13 :9;
    u32 link_state_changed :1;
    u32 reserved0 :12;
};

struct emac_event_enable {
    u32 reserved30 :2;
    u32 tx_offload_error_interrupt :1;
    u32 interesting_packet_pme_attn_en :1;
    u32 tx_statistics_overrun :1;
    u32 rx_statistics_overrun :1;
    u32 odi_error :1;
    u32 ap_error :1;
    u32 mii_interrupt :1;
    u32 mii_completion :1;
    u32 reserved13 :9;
    u32 link_state_changed :1;
    u32 reserved0 :12;
};

struct emac_led_control {
    union {
        struct {
	    u32 override_blink_rate :1;
	    u32 blink_period :12;
	    u32 reserved16 :3;
	    u32 speed_10_100_mode :1;
	    u32 shared_traffic_link_led_mode :1;
	    u32 mac_mode :1;
	    u32 led_mode :2;
	    u32 traffic_led_status :1;
	    u32 ten_mbps_led_status :1;
	    u32 hundred_mbps_led_status :1;
	    u32 gig_mbps_led_status :1;
	    u32 traffic_led :1;
	    u32 blink_traffic_led :1;
	    u32 override_traffic_led :1;
	    u32 ten_mbps_led :1;
	    u32 hundred_mbps_led :1;
	    u32 gig_mbps_led :1;
	    u32 override_link_leds :1;
	};
	u32 word;
    };
};

struct transmit_mac_mode {
    u32 rr_weight :5;
    u32 transmit_ftq_arbitration_mode :3;
    u32 reserved21 :3;
    u32 txmbuf_burst_size :4;
    u32 do_not_insert_gcm_gmac_iv :1;
    u32 do_not_drop_packet_if_malformed :1;
    u32 do_not_drop_if_sa_found_in_rx_direction :1;
    u32 do_not_drop_if_unsupported_ipv6_extension_or_ipv4_option_found :1;
    u32 do_not_drop_if_sa_invalid :1;
    u32 do_not_drop_if_ah_esp_header_not_found :1;
    u32 en_tx_ah_offload :1;
    u32 en_rx_esp_offload :1;
    u32 enable_bad_txmbuf_lockup_fix :1;
    u32 link_aware_enable :1;
    u32 enable_long_pause :1;
    u32 enable_big_backoff :1;
    u32 enable_flow_control :1;
    u32 reserved2 :2;
    u32 enable :1;
    u32 reset :1;
};

struct transmit_mac_status {
    union {
        struct {
	    u32 reserved :26;
	    u32 odi_overrun :1;
	    u32 odi_underrun :1;
	    u32 link_up :1;
	    u32 sent_xon :1;
	    u32 sent_xoff :1;
	    u32 currently_xoffed :1;
	};
	u32 word;
    };
};

struct transmit_mac_lengths {
    u32 reserved :18;
    u32 ipg_crs :2;
    u32 ipg :4;
    u32 slot :8;
};

struct receive_mac_mode {
    u32 disable_hw_fix_24175 :1;
    u32 disable_hw_fix_29914 :1;
    u32 disable_8023_len_chk_fix :1;
    u32 reserved28 :1;
    u32 reserved27 :1;
    u32 status_ready_new_disable :1;
    u32 ipv4_frag_fix :1;
    u32 ipv6_enable :1;
    u32 rss_enable :1;
    u32 rss_hash_mask_bits :3;
    u32 rss_tcpipv6_hash_enable :1;
    u32 rss_ipv6_hash_enable :1;
    u32 rss_tcpipv4_hash_enable :1;
    u32 rss_ipv4_hash_enable :1;
    u32 reserved14 :2;
    u32 ape_promisc_mode_en :1;
    u32 cq42199_fix_dis :1;
    u32 filter_broadcast :1;
    u32 keep_vlan_tag_diag :1;
    u32 no_crc_check :1;
    u32 promiscuous_mode :1;
    u32 length_check :1;
    u32 accept_runts :1;
    u32 keep_oversized :1;
    u32 keep_pause :1;
    u32 keep_mfc :1;
    u32 enable_flow_control :1;
    u32 enable :1;
    u32 reset :1;
};

struct receive_mac_status {
    union {
        struct {
	    u32 reserved :26;
	    u32 acpi_packet_rcvd :1;
	    u32 magic_packet_rcvd :1;
	    u32 rx_fifo_overrun :1;
	    u32 xon_received :1;
	    u32 xoff_received :1;
	    u32 remote_transmitter_xoffed :1;
	};
	u32 word;
    };
};


struct emac_mac_addr {
    union {
        struct {
            u32 byte_2 :8;
            u32 byte_1 :8;
            u32 reserved :16;
        };
        u32 word_hi;
    };
    union {
        struct {
            u32 byte_3 :8;
            u32 byte_4 :8;
            u32 byte_5 :8;
            u32 byte_6 :8;
        };
        u32 word_low;
    };
};

struct emac_rx_rule_control {
    union {
        struct {
            u32 enable :1;
            u32 and_with_next :1;
            u32 activate_rxcpu :1;
            u32 reserved :1;
            u32 reserved2 :1;
            u32 mask :1;
            u32 discard :1;
            u32 map :1;
            u32 reserved3 :6;
            u32 comparison_op :2;
            u32 header_type :3;
            u32 pclass :5;
            u32 offset :8;
        };
        u32 word;
    };
};

struct receive_mac_rules_configuration {
    u32 reserved :27;
    u32 no_rules_matches_default_class :3;
    u32 reserved2 :2;
};

struct emac_low_watermark_max_receive_frame {
    u32 reserved :11;
    u32 txfifo_almost_empty_thresh :5;
    u32 count :16;
};

struct emac_mii_status {
    u32 communications_register_overlap_error :1;
    u32 reserved2 :29;
    u32 mode_10mbps :1;
    u32 link_status :1;
};

struct emac_mii_mode {
    u32 communication_delay_fix_disable :1;
    u32 reserved21 :10;
    u32 mii_clock_count :5;
    u32 enable_constant_mdc_clock_speed :1;
    u32 reserved10 :5;
    u32 phy_address :5;
    u32 port_polling :1;
    u32 reserved3 :1;
    u32 auto_control :1;
    u32 use_short_preamble :1;
    u32 fast_clock :1;
};

struct emac_autopolling_status {
    u32 reserved :31;
    u32 error :1;
};

struct emac_mii_communication {
    u32 reserved30 :2;
    u32 start_busy :1;
    u32 read_failed :1;
    u32 read_command :1;
    u32 write_command :1;
    u32 phy_addr :5;
    u32 reg_addr :5;
    u32 data :16;
};

struct emac_regulator_voltage_control {
    u32 reserved :8;
    
    u32 regclt_1_2v_core :4;
    u32 reserved2 :4;
    
    u32 spd1000_led_pin_output_override :1;
    u32 spd1000_led_pin_output_en_override :1;
    u32 spd1000_led_pin_override_en :1;
    u32 spd1000_led_pin_input :1;
    u32 spd100_led_pin_output_override :1;
    u32 spd100_led_pin_output_en_override :1;
    u32 spd100_led_pin_override_en :1;
    u32 spd100_led_pin_input :1;

    u32 link_led_pin_output_override :1;
    u32 link_led_pin_output_en_override :1;
    u32 link_led_pin_override_en :1;
    u32 link_led_pin_input :1;
    u32 traffic_led_pin_output_override :1;
    u32 traffic_led_pin_output_en_override :1;
    u32 traffic_led_pin_override_en :1;
    u32 traffic_led_pin_input :1;
};

struct emac_regs {
    struct emac_mode mode;
    struct emac_status status;
    struct emac_event_enable event_enable;
    struct emac_led_control led_control;
    struct emac_mac_addr addr[4];
    u32 wol_pattern_pointer;
    u32 wol_pattern_configuration;
    u32 tx_random_backoff;
    u32 rx_mtu;
    u32 ofs_40;
    u32 ofs_44;
    u32 ofs_48;
    struct emac_mii_communication mii_communication;
    struct emac_mii_status mii_status;
    struct emac_mii_mode mii_mode;
    struct emac_autopolling_status autopolling_status;
    struct transmit_mac_mode tx_mac_mode;
    struct transmit_mac_status tx_mac_status;
    struct transmit_mac_lengths tx_mac_lengths;
    struct receive_mac_mode rx_mac_mode;
    struct receive_mac_status rx_mac_status;
    u32 mac_hash_0;
    u32 mac_hash_1;
    u32 mac_hash_2;
    u32 mac_hash_3;
    struct {
        struct emac_rx_rule_control control;
        u32 mask_value;
    } rx_rule[8];

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

    struct receive_mac_rules_configuration rx_rules_conf;
    struct emac_low_watermark_max_receive_frame low_watermark_max_receive_frame;
    u32 ofs_108;
    u32 ofs_10c;

    u32 ofs_110;
    u32 ofs_114;
    u32 ofs_118;
    u32 ofs_11c;

    u32 ofs_120;
    u32 ofs_124;
    u32 ofs_128;
    u32 ofs_12c;

    u32 ofs_130;
    u32 ofs_134;
    u32 ofs_138;
    u32 ofs_13c;

    u32 ofs_140;
    u32 ofs_144;
    u32 ofs_148;
    u32 ofs_14c;

    u32 ofs_150;
    u32 ofs_154;
    u32 ofs_158;
    u32 ofs_15c;

    u32 ofs_160;
    u32 ofs_164;
    u32 ofs_168;
    u32 ofs_16c;

    u32 ofs_170;
    u32 ofs_174;
    u32 ofs_178;
    u32 ofs_17c;

    u32 ofs_180;
    u32 ofs_184;
    u32 ofs_188;
    u32 ofs_18c;

    struct emac_regulator_voltage_control regulator_voltage_control;
    u32 ofs_194;
    u32 ofs_198;
    u32 ofs_19c;

    u32 ofs_1a0;
    u32 ofs_1a4;
    u32 ofs_1a8;
    u32 ofs_1ac;

    u32 ofs_1b0;
    u32 ofs_1b4;
    u32 ofs_1b8;
    u32 ofs_1bc;

    u32 eav_tx_time_stamp_lsb;
    u32 eav_tx_time_stamp_msb;
    u32 eav_av_transmit_tolerance_window;
    u32 eav_rt_tx_quality_1;

    u32 eav_rt_tx_quality_2;
    u32 eav_rt_tx_quality_3;
    u32 eav_rt_tx_quality_4;
    u32 ofs_1dc;
};

#endif
