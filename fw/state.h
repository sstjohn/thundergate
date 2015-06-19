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

#ifndef _STATE_H_
#define _STATE_H_

#define HANDSHAKE_MAGIC_SEEN	0x01
#define CLOAK_ENGAGED		0x02
#define TX_STD_SETUP		0x04
struct gate_state {
	u32 flags;
	u8 my_mac[6];
	u8 broadcast_mac[6];
	u8 remote_mac[6];
	u8 *dest_mac;
};
	
#endif
