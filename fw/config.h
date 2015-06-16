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

#ifndef _CONFIG_H_
#define _CONFIG_H_

#define LOCAL_CTRL 	0x1
#define PEER_CTRL 	0x2
#define BEACON_EN	0x10
#define OPROM_EN	0x20
#define CLOAK_EN	0x40

#define DEFAULT_FLAGS	(LOCAL_CTRL | PEER_CTRL | BEACON_EN | \
			 OPROM_EN | CLOAK_EN)

#define DEFAULT_CTRL_ETYPE	0x88b5

#define DEFAULT_CLOAK_VID 	0x88b5
#define DEFAULT_CLOAK_DID	0x0000
#define DEFAULT_CLOAK_CC  	0x0880

struct gate_config {
	u32 flags;

	u16 ctrl_etype;

	u16 cloak_vid;
	u16 cloak_did;
	u16 cloak_cc;
};
	
#endif
