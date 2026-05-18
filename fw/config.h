/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015-2026  Saul St. John
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

/* Cloak is opt-in. cloak_engage() hides the NIC from the host by rewriting
   its PCI vendor ID to DEFAULT_CLOAK_VID -- which also makes the device
   unmanageable through the host driver/dext. Engage it deliberately via the
   0x88b5 CLOAK_EN_CMD when wanted; do not cloak by default. */
#define DEFAULT_FLAGS (LOCAL_CTRL | PEER_CTRL | OPROM_EN)

#define DEFAULT_CTRL_ETYPE	0x88b5

#define DEFAULT_CLOAK_VID 	0x88b5
#define DEFAULT_CLOAK_DID	0x0000
#define DEFAULT_CLOAK_CC  	0x0880

#define GATE_SHMEM_BASE		0xe00
#define GATE_SHMEM_SIZE		0x150

struct gate_config {
	u32 flags;

	u16 ctrl_etype;

	u16 cloak_vid;
	u16 cloak_did;
	u16 cloak_cc;

	/* on-core TCP/IP stack addressing (network byte order) */
	u8 ip_addr[4];
	u8 netmask[4];
	u8 gateway[4];
};

/* 10.0.0.0/8 -- kept clear of common 192.168.x home/Wi-Fi subnets so
   the host routes test traffic out the wired peer port, not Wi-Fi. */
#define DEFAULT_IP_ADDR	{ 10, 0, 0, 222 }
#define DEFAULT_NETMASK	{ 255, 0, 0, 0 }
#define DEFAULT_GATEWAY	{ 10, 0, 0, 1 }
	
#endif
