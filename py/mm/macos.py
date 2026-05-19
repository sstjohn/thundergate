'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2026  Saul St. John

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# MacOSMemMgr -- DMA buffer manager for the macOS interface.
#
# It satisfies the _MemMgr contract (mm/mm.py) the way mm/win.py does:
# get_page() obtains one DMA-capable page from the dext and maps it into
# this process; get_paddr() returns the device-visible address.
#
# On Apple Silicon the page is mapped through the DART IOMMU, so the
# value the device must be programmed with is the IOVA the dext returns,
# not the host physical address. The dext (macos/TGDext) performs that
# mapping with an IODMACommand; this class just records the IOVA it hands
# back. (DART therefore also confines the NIC's DMA to these buffers --
# arbitrary host-memory introspection is not possible on Apple Silicon.)

from .mm import _MemMgr


class MacOSMemMgr(_MemMgr):
    def __init__(self, iface):
        super(MacOSMemMgr, self).__init__()
        # The dext exposes only kTGMaxDMABuffers (16) DMA slots, one taken
        # per get_page(). A large page keeps the whole driver's ring and
        # buffer footprint within a handful of dext allocations; the dext
        # AllocDMA takes an arbitrary size and DART maps it contiguously.
        self.page_sz = 0x100000
        self._iface = iface
        self._pages = {}        # page vaddr -> (dext DMA handle, IOVA)

    def get_page(self):
        handle, iova = self._iface._dma_alloc(self.page_sz)
        vaddr = self._iface._dma_map(handle)
        self._pages[vaddr] = (handle, iova)
        return (vaddr, self.page_sz)

    def get_paddr(self, vaddr):
        # The mapped page base is only OS-page-aligned, not page_sz-aligned,
        # so find the owning page by range rather than masking the vaddr.
        for page, (_handle, iova) in self._pages.items():
            if page <= vaddr < page + self.page_sz:
                return iova + (vaddr - page)
        raise KeyError(vaddr)

    def release(self):
        # Unmap and free every DMA page obtained from the dext.
        for vaddr, (handle, _iova) in list(self._pages.items()):
            try:
                self._iface._dma_unmap(handle, vaddr)
                self._iface._dma_free(handle)
            except Exception:
                pass
        self._pages.clear()
