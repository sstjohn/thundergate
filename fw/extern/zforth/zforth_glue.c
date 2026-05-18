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
 * zForth payload glue: binds the vendored, unmodified zForth VM
 * (extern/zforth/zforth.c) to the firmware console. zforth.c and zforth.h
 * are upstream verbatim; all target-specific code lives here and in
 * zfconf.h.
 */

#include <stddef.h>

#include "console.h"
#include "interp.h"
#include "zforth.h"
#include "forth_core.h"

/* The whole VM state -- stacks, dictionary, ~4.5 KB -- lands in .bss. */
static zf_ctx ctx;

/*
 * Host system call. zForth's core.zf maps `emit`/`.`/`tell` onto syscalls
 * 0/1/2; everything above that (quit, sin, include, save, user calls) has
 * no meaning on a bare NIC core and is quietly ignored.
 */
zf_input_state zf_host_sys(zf_ctx *c, zf_syscall_id id, const char *input)
{
	(void)input;

	switch ((int)id) {
	case ZF_SYSCALL_EMIT:
		con_putc((char)zf_pop(c));
		break;

	case ZF_SYSCALL_PRINT:
		con_puti((int)zf_pop(c));
		con_putc(' ');
		break;

	case ZF_SYSCALL_TELL: {
		zf_cell len = zf_pop(c);
		zf_cell addr = zf_pop(c);
		const char *dict = (const char *)zf_dump(c, NULL);
		con_write(dict + (int)addr, (unsigned)len);
		break;
	}

	default:
		break;
	}

	return ZF_INPUT_INTERPRET;
}

/*
 * Parse a token that was not found in the dictionary as an integer
 * literal: optional sign, decimal, or 0x-prefixed hex. zForth's upstream
 * host uses sscanf("%f"); the core is integer-only, so this replaces it.
 */
zf_cell zf_host_parse_num(zf_ctx *c, const char *buf)
{
	const char *s = buf;
	zf_cell v = 0;
	int neg = 0, digits = 0;

	if (*s == '-') {
		neg = 1;
		s++;
	} else if (*s == '+') {
		s++;
	}

	if (s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
		s += 2;
		for (; *s; s++) {
			int d;
			if (*s >= '0' && *s <= '9')
				d = *s - '0';
			else if (*s >= 'a' && *s <= 'f')
				d = *s - 'a' + 10;
			else if (*s >= 'A' && *s <= 'F')
				d = *s - 'A' + 10;
			else
				break;
			v = v * 16 + d;
			digits++;
		}
	} else {
		for (; *s >= '0' && *s <= '9'; s++) {
			v = v * 10 + (*s - '0');
			digits++;
		}
	}

	if (!digits || *s != '\0')
		zf_abort(c, ZF_ABORT_NOT_A_WORD);

	return neg ? -v : v;
}

static const char *abort_msg(zf_result r)
{
	switch (r) {
	case ZF_ABORT_INTERNAL_ERROR:    return "internal error";
	case ZF_ABORT_OUTSIDE_MEM:       return "out of bounds";
	case ZF_ABORT_DSTACK_UNDERRUN:   return "stack underrun";
	case ZF_ABORT_DSTACK_OVERRUN:    return "stack overrun";
	case ZF_ABORT_RSTACK_UNDERRUN:   return "return stack underrun";
	case ZF_ABORT_RSTACK_OVERRUN:    return "return stack overrun";
	case ZF_ABORT_NOT_A_WORD:        return "not a word";
	case ZF_ABORT_COMPILE_ONLY_WORD: return "compile-only word";
	case ZF_ABORT_INVALID_SIZE:      return "invalid size";
	case ZF_ABORT_DIVISION_BY_ZERO:  return "division by zero";
	case ZF_ABORT_INVALID_USERVAR:   return "invalid variable";
	default:                         return "error";
	}
}

void zf_interp_init(void)
{
	zf_init(&ctx, 0);          /* tracing off */
	zf_bootstrap(&ctx);        /* primitives + user variables */
	zf_eval(&ctx, forth_core); /* compile the Forth bootstrap */
}

void zf_interp_eval(const char *line, unsigned len)
{
	static char buf[256];
	unsigned i;
	zf_result r;

	/* zf_eval() wants a NUL-terminated string; the trailing NUL also
	 * flushes the final word. Over-long lines are clamped. */
	if (len > sizeof(buf) - 1)
		len = sizeof(buf) - 1;
	for (i = 0; i < len; i++)
		buf[i] = line[i];
	buf[len] = '\0';

	r = zf_eval(&ctx, buf);
	if (r == ZF_OK) {
		con_puts(" ok\n");
	} else {
		con_puts(" error: ");
		con_puts(abort_msg(r));
		con_putc('\n');
	}
}
