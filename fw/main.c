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

/* #include "fw.h" */

int global_var = 0;

int function(int local, int global) 
{
	static int static_var = 0;
	int function_local_var = static_var++;
	global_var = 0;
	return function_local_var;
}

void main() 
{
	int local_var = 0;

    while (1) {
		if (++local_var == 128) {
			if (++global_var == 128) {
				function(local_var, global_var);
			}
			local_var = 0;			
		}
	}
	/*
	if (grc.rxcpu_event.emac) {
		check_link();
	}
        if (grc.rxcpu_event.timer) {
		beacon();
        }
	if (grc.rxcpu_event.rdiq) {
		rx();
	}
	if (grc.rxcpu_event.sw_event_0) {
		lgate_reply();
	}
	*/
} 