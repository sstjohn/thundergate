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

u16 phy_read(u16 reg)
{
	emac.mii_communication.read_command = 1;
	emac.mii_communication.write_command = 0;
	emac.mii_communication.phy_addr = 1;
	emac.mii_communication.reg_addr = reg;
	emac.mii_communication.start_busy = 1;

	while (emac.mii_communication.start_busy);

	return emac.mii_communication.data;
}

void phy_write(u16 reg, u16 val)
{
	emac.mii_communication.read_command = 0;
	emac.mii_communication.write_command = 1;
	emac.mii_communication.phy_addr = 1;
	emac.mii_communication.reg_addr = reg;
	emac.mii_communication.data = val;
	emac.mii_communication.start_busy = 1;

	while (emac.mii_communication.start_busy);
}

void phy_reset()
{
	phy_write(0, 0x8000);

	while (phy_read(0) & 0x8000);
}

void phy_loopback_en()
{
	phy_write(0, 1 << 14);

	while(phy_read(1) & (1 << 4));
}

void phy_auto_mdix()
{
	u16 val;
	phy_write(0x18, 0x7007);
	
	val = phy_read(0x18);
	val |= (1 << 9) | (1 << 15);
	phy_write(0x18, val);

	val = phy_read(0x10);
	val &= ~(1 << 14);
	phy_write(0x10, val);
}

void phy_nego()
{
	u16 val = (1 << 11) | (1 << 10) | (1 << 8) | (1 << 7);
	val |= (1 << 6) | (1 << 5) | 1;
	phy_write(0x4, val);

	phy_write(0x9, 1 << 9);

	val = (1 << 12) | (1 << 9);
	phy_write(0, val);
	
	while (!(phy_read(1) & (1 << 5)));
}

void check_link()
{
	u16 res;

	if (state.flags & HANDSHAKE_MAGIC_SEEN)
		return;

	if (!emac.tx_mac_status.link_up) {
		emac.status.link_state_changed = 1;
		return;
	}

	phy_reset();
	phy_auto_mdix();
	phy_loopback_en();
	phy_nego();

	res = (phy_read(0x19) & 0x703);
	emac.rx_mac_mode.enable_flow_control = !!(res & 2);
	emac.tx_mac_mode.enable_flow_control = !!(res & 1);
	res >>= 8;
	if ((res & 6) == 6) {
		emac.mode.port_mode = 2;

		if (res & 1)
			emac.mode.half_duplex = 0;
		else
			emac.mode.half_duplex = 1;
		
	} else {
		emac.mode.port_mode = 1;

		if ((res == 3) || (res == 1))
			emac.mode.half_duplex = 1;
		else
			emac.mode.half_duplex = 0;
	}

	emac.status.link_state_changed = 1;
}
