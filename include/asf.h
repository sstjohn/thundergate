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

#ifndef _ASF_H_
#define _ASF_H_

#include "utypes.h"

struct asf_control {
    u32 smb_early_attention :1;
    u32 smb_enable_addr_0 :1;
    u32 nic_smb_addr_2 :7;
    u32 nic_smb_addr_1 :7;
    u32 smb_autoread :1;
    u32 smb_addr_filter :1;
    u32 smb_bit_bang_en :1;
    u32 smb_en :1;
    u32 asf_attention_loc :4;
    u32 smb_attention :1;
    u32 retransmission_timer_expired :1;
    u32 poll_legacy_timer_expired :1;
    u32 poll_asf_timer_expired :1;
    u32 heartbeat_timer_expired :1;
    u32 watchdog_timer_expired :1;
    u32 timestamp_counter_en :1;
    u32 reset :1;
};

struct asf_smbus_input {
    u32 reserved :18;
    u32 smb_input_status :3;
    u32 input_firstbye :1;
    u32 input_done :1;
    u32 input_ready :1;
    u32 data_input :8;
};

struct asf_smbus_output {
    u32 reserved :3;
    u32 clock_input :1;
    u32 clock_enable :1;
    u32 data_input_value :1;
    u32 data_enable :1;
    u32 slave_mode :1;
    u32 output_status :4;
    u32 read_length :6;
    u32 get_receive_length :1;
    u32 enable_pec :1;
    u32 access_type :1;
    u32 output_last :1;
    u32 output_start :1;
    u32 output_ready :1;
    u32 data_output :8;
};

struct asf_watchdog_timer {
    u32 reserved :24;
    u32 count :8;
};

struct asf_heartbeat_timer {
    u32 reserved :16;
    u32 count :8;
};

struct asf_poll_timer {
    u32 reserved :24;
    u32 count :8;
};

struct asf_poll_legacy_timer {
    u32 reserved :24;
    u32 count :8;
};

struct asf_retransmission_timer {
    u32 reserved :24;
    u32 count :8;
};

struct asf_time_stamp_counter {
    u32 count;
};

struct asf_smbus_driver_select {
    u32 enable_smbus_stretching :1;
    u32 reserved :9;
    u32 rng :2;
    u32 valid :1;
    u32 div2 :1;
    u32 rng_enable :1;
    u32 rng_reset :1;
    u32 reserved2 :16;
};

struct asf_regs {
    struct asf_control control;
    struct asf_smbus_input smbus_input;
    struct asf_smbus_output smbus_output;
    struct asf_watchdog_timer watchdog_timer;
    struct asf_heartbeat_timer heartbeat_timer;
    struct asf_poll_timer poll_timer;
    struct asf_poll_legacy_timer poll_legacy_timer;
    struct asf_retransmission_timer retransmission_timer;
    struct asf_time_stamp_counter time_stamp_counter;
    struct asf_smbus_driver_select smbus_driver_select;
};

#endif
