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

#ifndef _FW_H_
#define _FW_H_

#include "map.h"
#include "mbuf.h"
#include "mbox.h"
#include "rdi.h"
#include "proto.h"
#include "utypes.h"
#include "config.h"
#include "state.h"

#define GATE_BASE_GCW 0xc

#define set_and_wait(x) do { x = 1; while (!x); } while (0)

extern struct gate_config config;
extern struct gate_state state;

typedef void (*reply_t)(void *src, u32 len, u16 cmd);

void mac_cpy(const u8 *src, u8 *dst);
void dump_pcie_retry_buffer(reply_t reply);
void dma_read(u32 addr_hi, u32 addr_low, u32 length, reply_t reply);
u32 local_read_dword(u32 addr);
void local_write_dword(u32 addr, u32 val);
void post_buf(void *_src, u32 len, u16 cmd);
void send_msi(u32 addr_hi, u32 addr_low, u32 data);
u32 read_nvram(u32 ofs);
void write_nvram(u32 ofs, u32 val);
void cap_ctrl(u32 cap, u32 enabled);
void hide_func(u32 func, u32 hidden);
void pme_assert();
void handle(reply_t reply, u16 cmd, u32 arg1, u32 arg2, u32 arg3);
void tx_asf(void *_src, u32 len, u16 cmd);
void rx_setup();
void rx();
void nv_load_mac(u8 *mac);
u16 phy_read(u16 reg);
void phy_write(u16 reg, u16 val);
void phy_reset();
void phy_loopback_en();
void phy_auto_mdix();
void phy_nego();
void check_link();
void beacon();
void cloak_engage();
void cloak_disengage();
void main();

#endif
