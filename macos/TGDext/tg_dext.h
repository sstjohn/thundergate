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
 *
 * Selectors 0-2 (config space + BAR0) are the flash path (Phase 4a).
 * Selectors 3-5 (DMA buffers + interrupts) back the TAP driver and the
 * py/mm/macos.py memory manager (Phase 4b).
 */

#ifndef TG_DEXT_H
#define TG_DEXT_H

/* IOUserClient external-method selectors. */
enum {
    kTGConfigRead    = 0,  /* scalar in: (offset);        out: (value)         */
    kTGConfigWrite   = 1,  /* scalar in: (offset, value); out: ()              */
    kTGGetBar0Info   = 2,  /* scalar in: ();              out: (size)          */
    kTGAllocDMA      = 3,  /* scalar in: (size);          out: (handle, iova)  */
    kTGFreeDMA       = 4,  /* scalar in: (handle);        out: ()              */
    kTGWaitInterrupt = 5,  /* async: completion fires on the next interrupt    */
    kTGMethodCount   = 6,
};

/*
 * IOConnectMapMemory memory types.
 *   kTGMemoryBar0            -- PCI BAR 0
 *   kTGMemoryDMA + <handle>  -- the DMA buffer with that kTGAllocDMA handle
 */
enum {
    kTGMemoryBar0 = 0,
    kTGMemoryDMA  = 0x100,
};

/* Maximum number of concurrently-allocated DMA buffers. */
#define kTGMaxDMABuffers  16

#endif /* TG_DEXT_H */
