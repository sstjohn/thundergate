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
 * uBASIC payload glue: the interactive layer that stock uBASIC lacks.
 *
 * uBASIC (extern/ubasic/ubasic.c, tokenizer.c) runs one fixed program; it
 * has no line editor and no REPL. This file adds:
 *   - a numbered-line program store (enter a line to insert/replace/delete);
 *   - the meta-commands RUN, LIST, NEW;
 *   - a one-shot mode (a line with no number runs immediately);
 * and supplies the few libc functions uBASIC pulls in -- printf (to the
 * console), a reset-per-run bump allocator, and an exit() that unwinds
 * back here on a syntax error instead of halting the core.
 *
 * uBASIC keywords and variables are lowercase (this is stock uBASIC); the
 * RUN/LIST/NEW meta-commands are matched case-insensitively.
 */

#include <stddef.h>
#include <stdarg.h>

#include "console.h"
#include "interp.h"
#include "setjmp.h"
#include "ubasic.h"

/* ------------------------------------------------------------------ */
/* libc bits uBASIC needs                                             */
/* ------------------------------------------------------------------ */

/*
 * uBASIC mallocs one small node per program line for its line-number
 * index and frees them all at the start of each run. A bump allocator
 * that is reset before every run therefore never fragments and never
 * leaks; free() is a no-op.
 */
#define HEAP_SIZE 3072
static unsigned char heap[HEAP_SIZE] __attribute__((aligned(8)));
static unsigned heap_top;

void *malloc(size_t n)
{
	void *p;

	n = (n + 7u) & ~7u;
	if (heap_top + n > HEAP_SIZE)
		return (void *)0;
	p = &heap[heap_top];
	heap_top += n;
	return p;
}

void free(void *p) { (void)p; }

static void heap_reset(void) { heap_top = 0; }

/* Minimal printf -- uBASIC's PRINT uses %s and %d; output goes to the
 * console reply buffer. Width/precision are not supported (unused). */
int printf(const char *fmt, ...)
{
	va_list ap;

	va_start(ap, fmt);
	for (; *fmt; fmt++) {
		if (*fmt != '%') {
			con_putc(*fmt);
			continue;
		}
		switch (*++fmt) {
		case 'd': con_puti(va_arg(ap, int)); break;
		case 'u': con_putu(va_arg(ap, unsigned)); break;
		case 'c': con_putc((char)va_arg(ap, int)); break;
		case 's': con_puts(va_arg(ap, const char *)); break;
		case '%': con_putc('%'); break;
		case '\0': va_end(ap); return 0;
		default:  con_putc('%'); con_putc(*fmt); break;
		}
	}
	va_end(ap);
	return 0;
}

/* uBASIC calls exit() on a syntax error. Unwind back to run_program()
 * rather than halting the core. */
static jmp_buf exit_env;
static int exit_armed;

void exit(int code)
{
	(void)code;
	if (exit_armed)
		longjmp(exit_env, 1);
	for (;;)        /* unreachable: a run always arms exit_env first */
		;
}

/* ------------------------------------------------------------------ */
/* numbered-line program store                                        */
/* ------------------------------------------------------------------ */

#define PROG_MAX 2048

static char prog[PROG_MAX];
static unsigned prog_len;

/* Parse the leading line number of a stored line. */
static int line_num_at(const char *s)
{
	int n = 0;

	while (*s >= '0' && *s <= '9')
		n = n * 10 + (*s++ - '0');
	return n;
}

/* Offset of the first stored line whose number is >= n; *exact is set
 * when a line with exactly that number exists. */
static unsigned find_line(int n, int *exact)
{
	unsigned off = 0;

	*exact = 0;
	while (off < prog_len) {
		int ln = line_num_at(prog + off);

		if (ln >= n) {
			*exact = (ln == n);
			return off;
		}
		while (off < prog_len && prog[off] != '\n')
			off++;
		if (off < prog_len)
			off++;
	}
	return prog_len;
}

/* End offset (past the '\n') of the line that starts at off. */
static unsigned line_end(unsigned off)
{
	while (off < prog_len && prog[off] != '\n')
		off++;
	if (off < prog_len)
		off++;
	return off;
}

/*
 * Insert, replace or delete line n. text/tlen is the line as typed,
 * starting at the number; tlen == 0 deletes. Returns 0 if out of room.
 */
static int prog_set(int n, const char *text, unsigned tlen)
{
	int exact;
	unsigned off = find_line(n, &exact);
	unsigned oldlen = exact ? (line_end(off) - off) : 0;
	unsigned newlen = tlen ? (tlen + 1) : 0;  /* +1 for the '\n' */
	unsigned i;

	if (prog_len - oldlen + newlen > PROG_MAX - 1)
		return 0;

	/* Shift the tail so the [off, off+oldlen) slot becomes newlen. */
	if (off + oldlen < prog_len) {
		unsigned tail = prog_len - off - oldlen;

		if (newlen > oldlen) {
			for (i = tail; i > 0; i--)
				prog[off + newlen + i - 1] = prog[off + oldlen + i - 1];
		} else {
			for (i = 0; i < tail; i++)
				prog[off + newlen + i] = prog[off + oldlen + i];
		}
	}
	if (newlen) {
		for (i = 0; i < tlen; i++)
			prog[off + i] = text[i];
		prog[off + tlen] = '\n';
	}
	prog_len = prog_len - oldlen + newlen;
	prog[prog_len] = '\0';
	return 1;
}

/* ------------------------------------------------------------------ */
/* REPL                                                               */
/* ------------------------------------------------------------------ */

/* Whole-line case-insensitive match against a lowercase command. */
static int line_is(const char *s, unsigned len, const char *cmd)
{
	unsigned i = 0;

	while (cmd[i]) {
		char c = (i < len) ? s[i] : 0;

		if (c >= 'A' && c <= 'Z')
			c += 'a' - 'A';
		if (c != cmd[i])
			return 0;
		i++;
	}
	return i == len;
}

/* Run a uBASIC program string, guarding against a runaway loop (the core
 * has no preemption -- 10 goto 10 must not wedge it forever). */
static void run_program(const char *src)
{
	heap_reset();
	exit_armed = 1;
	if (setjmp(exit_env) == 0) {
		unsigned guard = 0;

		ubasic_init(src);
		while (!ubasic_finished()) {
			ubasic_run();
			if (++guard > 100000u) {
				con_puts("\n?runaway program halted\n");
				exit_armed = 0;
				return;
			}
		}
		con_puts("ok\n");
	} else {
		con_puts("?syntax error\n");
	}
	exit_armed = 0;
}

void ub_interp_init(void)
{
	prog_len = 0;
	prog[0] = '\0';
}

void ub_interp_eval(const char *line, unsigned len)
{
	unsigned i, j;

	/* Trim trailing newline/whitespace and leading whitespace. */
	while (len && (line[len - 1] == '\n' || line[len - 1] == '\r' ||
		       line[len - 1] == ' ' || line[len - 1] == '\t'))
		len--;
	i = 0;
	while (i < len && (line[i] == ' ' || line[i] == '\t'))
		i++;

	if (i == len) {
		con_puts("ok\n");
		return;
	}

	/* A line starting with a digit edits the stored program. */
	if (line[i] >= '0' && line[i] <= '9') {
		int n = 0;
		unsigned k;

		j = i;
		while (j < len && line[j] >= '0' && line[j] <= '9')
			n = n * 10 + (line[j++] - '0');
		k = j;
		while (k < len && (line[k] == ' ' || line[k] == '\t'))
			k++;
		/* bare number deletes; number + text inserts or replaces */
		if (prog_set(n, line + i, k == len ? 0 : len - i))
			con_puts("ok\n");
		else
			con_puts("?out of memory\n");
		return;
	}

	/* Meta-commands. */
	if (line_is(line + i, len - i, "run")) {
		run_program(prog);
		return;
	}
	if (line_is(line + i, len - i, "list")) {
		con_write(prog, prog_len);
		con_puts("ok\n");
		return;
	}
	if (line_is(line + i, len - i, "new")) {
		prog_len = 0;
		prog[0] = '\0';
		con_puts("ok\n");
		return;
	}

	/* Anything else runs immediately as a one-shot statement. */
	{
		static char oneshot[288];
		unsigned m = 0;

		oneshot[m++] = '1';
		oneshot[m++] = ' ';
		for (j = i; j < len && m < sizeof(oneshot) - 2; j++)
			oneshot[m++] = line[j];
		oneshot[m++] = '\n';
		oneshot[m] = '\0';
		run_program(oneshot);
	}
}
