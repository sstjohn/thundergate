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

#ifndef _NET_CHECKSUM_H_
#define _NET_CHECKSUM_H_

#include "utypes.h"

/*
 * The 16-bit ones-complement Internet checksum (RFC 1071).
 *
 * net_cksum() is the standalone checksum of a buffer (IP header, ICMP
 * message). net_cksum_seed() continues a sum from a partial total -- used
 * for the UDP checksum, which prepends an IPv4 pseudo-header.
 *
 * Implemented byte-wise with only add and shift: alignment-safe on a core
 * with no lwl/lwr, and free of the mult/div the core also lacks.
 */

u32 net_cksum_partial(const u8 *data, u32 len, u32 seed);
u16 net_cksum_fold(u32 sum);
u16 net_cksum(const u8 *data, u32 len);
u16 net_cksum_seed(const u8 *data, u32 len, u32 seed);

#endif
