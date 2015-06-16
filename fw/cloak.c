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

#include "fw.h"

u32 old_id = 0;
u32 old_class = 0;

void cloak_engage()
{
	u32 new_id;

	if (state.flags & CLOAK_ENGAGED)
		return;

	old_id = cfg_port.pci_id.word;
	new_id = old_id;
	if (config.cloak_vid) {
		new_id &= 0xffff0000;
		new_id |= config.cloak_vid;
	}
	if (config.cloak_did) {
		new_id &= 0xffff;
		new_id |= (config.cloak_vid << 16);
	}
	cfg_port.pci_id.word = new_id;

	old_class = cfg_port.pci_class.word;
	if (config.cloak_cc)
		cfg_port.pci_class.word = config.cloak_cc << 8;

	state.flags |= CLOAK_ENGAGED;
}

void cloak_disengage()
{
	if (!(state.flags & CLOAK_ENGAGED))
		return;

	cfg_port.pci_id.word = old_id;
	cfg_port.pci_class.word = old_class;

	state.flags &= ~CLOAK_ENGAGED;
}
