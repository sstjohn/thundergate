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

u32 read_nvram(u32 ofs)
{
	u32 r;

	nvram.sw_arb.req_set0 = 1;
	while (!nvram.sw_arb.arb_won0);
	nvram.access.enable = 1;

	nvram.data_address = ofs;

	nvram.command.last = 1;
	nvram.command.first = 1;
	nvram.command.erase = 0;
	nvram.command.wr = 0;
	nvram.command.doit = 1;

	while (!nvram.command.done);
	r = nvram.read_data;

	nvram.access.enable = 0;
	nvram.sw_arb.req_clr0 = 1;

	return r;
}

void write_nvram(u32 ofs, u32 val)
{
	nvram.sw_arb.req_set0 = 1;
	while (!nvram.sw_arb.arb_won0);
	
	nvram.access.enable = 1;
	nvram.access.write_enable = 1;
	
	nvram.data_address = ofs;
	nvram.write_data = val;

	nvram.command.last = 1;
	nvram.command.first = 1;
	nvram.command.erase = 0;
	nvram.command.wr = 1;
	nvram.command.doit = 1;

	while (!nvram.command.done);

	nvram.access.write_enable = 1;
	nvram.access.enable = 0;
	nvram.sw_arb.req_clr0 = 1;
}

void nv_load_mac(u8 *mac)
{
    u64 tmp;

    nvram.sw_arb.req_set0 = 1;
    while (!nvram.sw_arb.arb_won0);
    nvram.access.enable = 1;

    nvram.command.wr = 0;
    nvram.command.erase = 0;
    nvram.command.first = 1;
    nvram.command.last = 1;

    nvram.data_address = 0x7c;
    nvram.command.doit = 1;
    while (!nvram.command.done);

    tmp = nvram.read_data;
    tmp <<= 32;

    nvram.command.done = 1;

    nvram.data_address = 0x80;
    nvram.command.doit = 1;
    while (!nvram.command.done);
    tmp |= nvram.read_data;

    nvram.access.enable = 0;
    nvram.sw_arb.req_clr0 = 1;

    for (int i = 5; i >= 0; i--) {
	mac[i] = tmp & 0xff;
	tmp >>= 8;
    }
}
