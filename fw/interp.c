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
 * Interpreter dispatcher. The firmware can carry zForth, uBASIC, both, or
 * neither (the Makefile's ZFORTH/UBASIC switches define TG_ZFORTH/TG_UBASIC).
 * This routes each console line to the active interpreter; a line that is
 * just "forth" or "basic" switches languages, "help" prints a hint.
 */

#include "console.h"
#include "interp.h"

static int active;          /* 0 = zForth, 1 = uBASIC */

/* Case-insensitive match of the s[0..n) span against a lowercase command. */
static int eq_ci(const char *s, unsigned n, const char *cmd)
{
	unsigned i;

	for (i = 0; i < n; i++) {
		char c = s[i];

		if (c >= 'A' && c <= 'Z')
			c += 'a' - 'A';
		if (cmd[i] == '\0' || c != cmd[i])
			return 0;
	}
	return cmd[n] == '\0';
}

void interp_init(void)
{
#ifdef TG_ZFORTH
	zf_interp_init();
#endif
#ifdef TG_UBASIC
	ub_interp_init();
#endif
	/* default to zForth when both are present */
#ifdef TG_UBASIC
	active = 1;
#endif
#ifdef TG_ZFORTH
	active = 0;
#endif
}

void interp_eval_line(const char *line, unsigned len)
{
	const char *s;
	unsigned i = 0, n;

	/* Trim surrounding whitespace just to recognise the meta-commands;
	 * the interpreter gets the original, untrimmed line. */
	while (len && (line[len - 1] == '\n' || line[len - 1] == '\r' ||
		       line[len - 1] == ' ' || line[len - 1] == '\t'))
		len--;
	while (i < len && (line[i] == ' ' || line[i] == '\t'))
		i++;
	s = line + i;
	n = len - i;

	if (eq_ci(s, n, "forth") || eq_ci(s, n, "zforth")) {
#ifdef TG_ZFORTH
		active = 0;
		con_puts("[zForth]\n");
#else
		con_puts("zForth not built into this image\n");
#endif
		return;
	}
	if (eq_ci(s, n, "basic") || eq_ci(s, n, "ubasic")) {
#ifdef TG_UBASIC
		active = 1;
		con_puts("[uBASIC]\n");
#else
		con_puts("uBASIC not built into this image\n");
#endif
		return;
	}
	if (eq_ci(s, n, "help") || eq_ci(s, n, "?")) {
		con_puts("an interpreter running on the Tigon3 RX CPU.\n");
		con_puts("type 'forth' or 'basic' to switch language.\n");
		return;
	}

#ifdef TG_ZFORTH
	if (active == 0) {
		zf_interp_eval(line, len);
		return;
	}
#endif
#ifdef TG_UBASIC
	if (active == 1) {
		ub_interp_eval(line, len);
		return;
	}
#endif
	con_puts("no interpreter built into this image\n");
}
