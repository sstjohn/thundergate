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

#ifndef _OTP_H_
#define _OTP_H_

#include "utypes.h"

struct otp_mode {
    u32 reserved :31;
    u32 mode :1;
};

struct otp_control {
    u32 bypass_otp_clk :1;
    u32 reserved :2;
    u32 cpu_debug_sel :4;
    u32 burst_stat_sel :1;
    u32 access_mode :2;
    u32 otp_prog_en :1;
    u32 otp_debug_mode :1;
    u32 wrp_continue_on_fail :1;
    u32 wrp_time_margin :3;
    u32 wrp_sadbyp :1;
    u32 unused :1;
    u32 wrp_pbyp :1;
    u32 wrp_pcount :3;
    u32 wrp_vsel :4;
    u32 wrp_prog_sel :1;
    u32 command :4;
    u32 start :1;
};

struct otp_status {
    u32 reserved :20;
    u32 control_error :1;
    u32 wrp_error :1;
    u32 invalid_command :1;
    u32 otp_stby_reg :1;
    u32 init_wait_done :1;
    u32 prog_blocked :1;
    u32 invalid_prog_req :1;
    u32 wrp_fail :1;
    u32 wrp_busy :1;
    u32 wrp_dout :1;
    u32 wrp_data_read :1;
    u32 command_done :1;
};

struct otp_addr {
    u32 reserved :16;
    u32 address :16;
};

struct otp_soft_reset {
    u32 reserved :31;
    u32 reset :1;
};

struct otp_regs {
    struct otp_mode mode;
    struct otp_control control;
    struct otp_status status;
    struct otp_addr address;

    u32 write_data;
    u32 read_data;
    struct otp_soft_reset soft_reset;
};

#endif
