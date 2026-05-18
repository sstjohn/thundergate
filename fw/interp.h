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
 * Per-language backends behind the fw/interp.c dispatcher. Both interpreters
 * are linked into the one firmware image; interp.c's interp_eval_line()
 * routes a REPL line to whichever is active.
 */
#ifndef _INTERP_H_
#define _INTERP_H_

void zf_interp_init(void);
void zf_interp_eval(const char *line, unsigned len);
void ub_interp_init(void);
void ub_interp_eval(const char *line, unsigned len);

#endif
