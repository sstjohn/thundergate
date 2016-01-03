/*
*  ThunderGate - an open source toolkit for PCI bus exploration
*  Copyright (C) 2015-2016  Saul St. John
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

DEFINE_GUID (GUID_DEVINTERFACE_tgwink,
    0x77dce17a,0x78bd,0x4b27,0x84,0x09,0x8f,0x5d,0x20,0x96,0x3c,0x39);
// {77dce17a-78bd-4b27-8409-8f5d20963c39}

#define IOCTL_TGWINK_SAY_HELLO CTL_CODE(0x8000, 0x8000, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)
#define IOCTL_TGWINK_MAP_BAR_0 CTL_CODE(0x8000, 0x8001, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)
#define IOCTL_TGWINK_READ_PHYS CTL_CODE(0x8000, 0x8002, METHOD_BUFFERED, FILE_ANY_ACCESS)
#define IOCTL_TGWINK_GET_IRQFD CTL_CODE(0x8000, 0x8003, METHOD_OUT_DIRECT, FILE_ANY_ACCESS)
