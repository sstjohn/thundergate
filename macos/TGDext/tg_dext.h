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

/*
 * The ABI between the ThunderGate dext and its user-space client.
 *
 * The dext (this directory) and py/interfaces/macos.py must agree on
 * these selectors and memory-type values; the Python side mirrors them.
 */

#ifndef TG_DEXT_H
#define TG_DEXT_H

/* IOUserClient external-method selectors. */
enum {
    kTGConfigRead  = 0,   /* scalar in: (offset);        scalar out: (value) */
    kTGConfigWrite = 1,   /* scalar in: (offset, value); scalar out: ()      */
    kTGGetBar0Info = 2,   /* scalar in: ();              scalar out: (size)  */
    kTGMethodCount = 3,
};

/* IOConnectMapMemory memory types. */
enum {
    kTGMemoryBar0 = 0,    /* maps PCI BAR 0 into the caller */
};

#endif /* TG_DEXT_H */
