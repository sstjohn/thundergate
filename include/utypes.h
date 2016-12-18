/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015-2016 Saul St. John
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

#ifndef _UTYPES_H_
#define _UTYPES_H_

#if defined(_MSC_VER)
#define uint8_t unsigned __int8
#define uint16_t unsigned __int16
#define uint32_t unsigned __int32
#define uint64_t unsigned __int64
#elif defined(__clang__)
#define uint8_t __UINT8_TYPE__
#define uint16_t __UINT16_TYPE__
#define uint32_t __UINT32_TYPE__
#define uint64_t __UINT64_TYPE__
#elif defined(__GNUC__) || defined(CTYPESGEN)
#include <stdint-gcc.h>
#endif

typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef uint64_t u64;

#endif

