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

char *beacon_buf = 
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"aabbccddeeffgghhiijjkkllmmnnooppqqrrssttuuvvwwxxyyzz"
	"0123456789012345678901234567890123456789012$";

void reset_beacon_timer()
{
    grc.rxcpu_event.timer = 0;
    if (config.flags & BEACON_EN) {
    	grc.rxcpu_timer_reference = grc.timer + 1000000;
    	grc.rxcpu_event_enable.timer = 1;
    }
}

void beacon()
{
    	tx_asf(beacon_buf, 76, 0);
	reset_beacon_timer();
}
