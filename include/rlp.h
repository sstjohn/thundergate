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

#ifndef _RLP_H_
#define _RLP_H_

struct receive_list_placement_mode {
    u32 reserved :27;
    u32 stats_overflow_attention_enable :1;
    u32 mapping_out_of_range_attention_enable :1;
    u32 class_zero_attention_enable :1;
    u32 enable :1;
    u32 reset :1;
};

struct receive_list_placement_status {
    u32 reserved :27;
    u32 stats_overflow_attention :1;
    u32 mapping_out_of_range_attention :1;
    u32 class_zero_attention :1;
    u32 reserved2 :2;
};

struct receive_selector_not_empty_bits {
    u32 reserved :16;
    u32 list_non_empty_bits :16;
};

struct receive_list_placement_configuration {
    u32 reserved :17;
    u32 default_interrupt_distribution_queue :2;
    u32 bad_frames_class :5;
    u32 number_of_active_lists :5;
    u32 number_of_lists_per_distribution_group :3;
};

struct receive_list_placement_statistics_control {
    u32 reserved :29;
    u32 statistics_clear :1;
    u32 reserved2 :1;
    u32 statistics_enable :1;
};

struct receive_list_placement_statistics_enable_mask {
    union {
        struct {
            u32 reserved :6;
            u32 rss_priority :1;
            u32 rc_return_ring_enable :1;
            u32 cpu_mactq_priority_disable :1;
            u32 reserved2 :1;
            u32 enable_inerror_stats :1;
            u32 enable_indiscard_stats :1;
            u32 enable_no_more_rbd_stats :1;
            u32 reserved3 :15;
            u32 perst_l :1;
            u32 a1_silent_indication :1;
            u32 enable_cos_stats :1;
        };
        u32 word;
    };
};

struct receive_list_placement_statistics_increment_mask {
    u32 reserved :10;
    u32 counters_increment_mask :6;
    u32 reserved2 :15;
    u32 counters_increment_mask_again :1;
};

struct receive_list_local_statistics_counter {
    u32 reserved :22;
    u32 counters_value :10;
};

struct receive_list_lock {
    u32 grant :16;
    u32 request :16;
};

struct rlp_regs {
    struct receive_list_placement_mode mode;
    struct receive_list_placement_status status;
    struct receive_list_lock lock;
    struct receive_selector_not_empty_bits selector_not_empty_bits;
    struct receive_list_placement_configuration config;
    struct receive_list_placement_statistics_control stats_control;
    struct receive_list_placement_statistics_enable_mask stats_enable_mask;
    struct receive_list_placement_statistics_increment_mask stats_increment_mask;
    u32 unknown[56];

    struct {
        u32 list_head;
        u32 list_tail;
        u32 list_count;
        u32 unknown;
    } rx_selector[16];

    struct receive_list_local_statistics_counter stat_counter[23];
};

#endif
