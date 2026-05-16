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

#include "net/checksum.h"

/*
 * Accumulate the ones-complement sum of `len` bytes into `seed`, reading
 * the data as big-endian 16-bit words. Byte-wise, so it never needs an
 * unaligned load; an odd trailing byte is treated as the high byte of a
 * final 16-bit word, per RFC 1071.
 */
u32 net_cksum_partial(const u8 *data, u32 len, u32 seed)
{
    u32 i;

    for (i = 0; (i + 1) < len; i += 2)
        seed += ((u32)data[i] << 8) | data[i + 1];

    if (i < len)
        seed += (u32)data[i] << 8;

    return seed;
}

/* Fold the 32-bit accumulator down to a 16-bit ones-complement checksum. */
u16 net_cksum_fold(u32 sum)
{
    while (sum >> 16)
        sum = (sum & 0xffff) + (sum >> 16);

    return (u16)(~sum & 0xffff);
}

u16 net_cksum(const u8 *data, u32 len)
{
    return net_cksum_fold(net_cksum_partial(data, len, 0));
}

u16 net_cksum_seed(const u8 *data, u32 len, u32 seed)
{
    return net_cksum_fold(net_cksum_partial(data, len, seed));
}
