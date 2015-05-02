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

#ifndef _HC_H_
#define _HC_H_

#include "utypes.h"

struct hc_mode {
	u32 during_int_frame_cntr_fix_disable :1;
	u32 end_of_rx_stream_detector_fires_all_msix :1;
	u32 end_of_rx_stream_int :1;
	u32 enable_attn_int_fix :1;
	u32 reserved :10;
	u32 coalesce_now_1_5 :5;
	u32 no_int_on_force_update :1;
	u32 no_int_on_dmad_force :1;
	u32 reserved2 :1;
	u32 clear_ticks_mode_on_rx :1;
	u32 status_block_size :2;
	u32 msi_bits :3;
	u32 coalesce_now :1;
	u32 attn_enable :1;
	u32 enable :1;
	u32 reset :1;
};

struct hc_status {
    u32 reserved :29;
    u32 error :1;
    u32 reserved2 :2;
};

struct hc_flow_attention {
    u32 sbdi :1;
    u32 sbdc :1;
    u32 sbdrs :1;
    u32 sdi :1;
    u32 sdc :1;
    u32 reserved :3;
    u32 rbdi :1;
    u32 rbdc :1;
    u32 rlp :1;
    u32 rls :1;
    u32 rdi :1;
    u32 rdc :1;
    u32 rcb_incorrect :1;
    u32 dmac_discard :1;
    u32 hc :1;
    u32 reserved2 :7;
    u32 ma :1;
    u32 mbuf_low_water :1;
    u32 reserved3 :6;
};

struct hc_regs {
	struct hc_mode mode;
	struct hc_status status;
	u32 rx_coal_ticks;
	u32 tx_coal_ticks;

	u32 rx_max_coal_bds;
	u32 tx_max_coal_bds;
        u32 ofs_18;
        u32 ofs_1c;

	u32 rx_max_coal_bds_in_int;
	u32 tx_max_coal_bds_in_int;
        u32 ofs_28;
        u32 ofs_2c;

        u32 ofs_30;
        u32 ofs_34;
	u32 status_block_host_addr_hi;
	u32 status_block_host_addr_low;

        u32 ofs_40;
        u32 status_block_nic_addr;
	struct hc_flow_attention flow_attention;
        u32 ofs_4c;
 
	u32 nic_jumbo_rbd_ci;
	u32 nic_std_rbd_ci;
	u32 nic_mini_rbd_ci;
        u32 ofs_5c;

        u32 ofs_60;
        u32 ofs_64;
        u32 ofs_68;
        u32 ofs_6c;

        u32 ofs_70;
        u32 ofs_74;
        u32 ofs_78;
        u32 ofs_7c;

	u32 nic_diag_rr_pi[16];
	u32 nic_diag_sbd_ci[16];
};

#endif
