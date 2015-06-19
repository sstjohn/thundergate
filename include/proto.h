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

#define CMD_REPLY		0x8000
#define ERR_REPLY		0x9000
#define UNKNOWN_CMD		0xffff

#define PING_CMD    		0x01
#define PING_REPLY  		PING_CMD | CMD_REPLY

#define READ_LOCAL_CMD    	0x02
#define READ_LOCAL_REPLY	READ_LOCAL_CMD | CMD_REPLY

#define WRITE_LOCAL_CMD		0x03
#define WRITE_LOCAL_ACK		WRITE_LOCAL_CMD | CMD_REPLY

#define READ_DMA_CMD		0x04
#define	READ_DMA_REPLY		READ_DMA_CMD | CMD_REPLY

#define SEND_MSI_CMD		0x05
#define SEND_MSI_ACK		SEND_MSI_CMD | CMD_REPLY

#define CAP_CTRL_CMD		0x06
#define CAP_CTRL_ACK		CAP_CTRL_CMD | CMD_REPLY
# define CAP_POWER_MANAGEMENT 		0x8
# define CAP_VPD			0x4
# define CAP_MSI			0x2
# define CAP_MSIX			0x1

#define HIDE_FUNC_CMD		0x07
#define HIDE_FUNC_ACK		HIDE_FUNC_CMD | CMD_REPLY

#define PME_ASSERT_CMD		0x08
#define PME_ASSERT_ACK		PME_ASSERT_CMD | CMD_REPLY

#define READ_NVRAM_CMD		0x09
#define READ_NVRAM_ACK		READ_NVRAM_CMD | CMD_REPLY

#define WRITE_NVRAM_CMD		0x0a
#define WRITE_NVRAM_ACK		WRITE_NVRAM_CMD | CMD_REPLY

#define PCIE_RETRY_BUFFER_DUMP_CMD 0x0b
#define PCIE_RETRY_BUFFER_DUMP_ACK PCIE_RETRY_BUFFER_DUMP_CMD | CMD_REPLY

#define CLOAK_EN_CMD		0x0c
#define CLOAK_EN_ACK		CLOAK_EN_CMD | CMD_REPLY

#define CLOAK_DIS_CMD 		0x0d
#define CLOAK_DIS_ACK		CLOAK_DIS_CMD | CMD_REPLY

#define TX_STD_ENQ_CMD		0x0e
#define TX_STD_ENQ_ACK		TX_STD_ENQ_CMD | CMD_REPLY
#define TX_STD_ENQ_ERR		TX_STD_ENQ_CMD | ERR_REPLY

#endif
