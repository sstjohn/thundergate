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

#define PING_CMD    		1
#define PING_REPLY  		2

#define READ_LOCAL_CMD    	3
#define READ_LOCAL_REPLY	4

#define WRITE_LOCAL_CMD		5
#define WRITE_LOCAL_ACK		6

#define READ_DMA_CMD		7
#define	READ_DMA_REPLY		8

#endif
