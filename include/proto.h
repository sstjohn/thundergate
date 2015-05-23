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

#ifndef _PROTO_H_
#define _PROTO_H_

#define PROTO_VER		1

#define PING_CMD    		0x01
#define PING_REPLY  		0x02

#define READ_LOCAL_CMD    	0x03
#define READ_LOCAL_REPLY	0x04

#define WRITE_LOCAL_CMD		0x05
#define WRITE_LOCAL_ACK		0x06

#define READ_DMA_CMD		0x07
#define	READ_DMA_REPLY		0x08

#define SEND_MSI_CMD		0x09
#define SEND_MSI_ACK		0x0a

#define CAP_CTRL_CMD		0x0b
#define CAP_CTRL_ACK		0x0c
# define CAP_POWER_MANAGEMENT 		0x8
# define CAP_VPD			0x4
# define CAP_MSI			0x2
# define CAP_MSIX			0x1

#endif
