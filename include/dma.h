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

#ifndef _DMA_H_
#define _DMA_H_

struct dma_desc {
	u32 addr_hi;
	u32 addr_lo;
	u32 nic_mbuf;
	struct {
		u32 length :16;
		u32 cqid_sqid :16;
	};
	u32 flags;
	u32 opaque1;
	u32 opaque2;
	u32 opaque3;
};

#endif
