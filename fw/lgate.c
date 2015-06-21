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

#include "fw.h"

u8 *lgate_base;


void lgate_post(void *_src, u32 _len, u16 cmd)
{
	int i;
	int len = _len * 4;
	if (len > GATE_SHMEM_SIZE - 4)
		len = GATE_SHMEM_SIZE - 4;

	u8 *src = (u8 *)_src;
	for (i = 0; i < len; i++)
		lgate_base[4 + i] = *src++;

	*((u16 *)(lgate_base + 2)) = (cmd | 0x8000);
}

void lgate_reply()
{
	if (state.flags & LGATE_SETUP) {
		u32 tmp = *((u32 *)lgate_base);
		if ((tmp >> 16) == config.ctrl_etype) {
			if (!(tmp & 0x8000)) {
				u16 cmd = tmp & 0x7fff;
				u32 arg1 = *((u32 *)(lgate_base + 4));
				u32 arg2 = *((u32 *)(lgate_base + 8));
				u32 arg3 = *((u32 *)(lgate_base + 0xc));
				handle(lgate_post, cmd, arg1, arg2, arg3);
			}
		} else {
			*((u32 *)lgate_base) = (u32)config.ctrl_etype << 16;
		}
	}
	grc.rxcpu_event.sw_event_0 = 0;
}

void lgate_setup()
{
	if (!(config.flags & LOCAL_CTRL))
		return;

	lgate_base = (u8 *)(GATE_SHMEM_BASE);
	*((u32 *)lgate_base) = (u32)config.ctrl_etype << 16;

	state.flags |= LGATE_SETUP;
}
