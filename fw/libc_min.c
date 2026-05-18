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
 * Minimal freestanding string/mem helpers for the vendored interpreters.
 * The mips-elf toolchain ships no C library; these are the few <string.h>
 * and <stdlib.h> functions zForth and uBASIC reference. They are plain
 * byte loops -- not soft-math; runtime multiply/divide come from libgcc.
 *
 * setjmp()/longjmp() are built on GCC's __builtin_* primitives (see
 * fw/extern/include/setjmp.h); longjmp() stashes the result value here.
 */

#include <stddef.h>
#include "string.h"
#include "stdlib.h"
#include "setjmp.h"

void *memcpy(void *dst, const void *src, size_t n)
{
	unsigned char *d = dst;
	const unsigned char *s = src;
	while (n--)
		*d++ = *s++;
	return dst;
}

void *memmove(void *dst, const void *src, size_t n)
{
	unsigned char *d = dst;
	const unsigned char *s = src;

	if (d < s) {
		while (n--)
			*d++ = *s++;
	} else {
		d += n;
		s += n;
		while (n--)
			*--d = *--s;
	}
	return dst;
}

void *memset(void *dst, int c, size_t n)
{
	unsigned char *d = dst;
	while (n--)
		*d++ = (unsigned char)c;
	return dst;
}

int memcmp(const void *a, const void *b, size_t n)
{
	const unsigned char *p = a, *q = b;
	while (n--) {
		if (*p != *q)
			return *p - *q;
		p++;
		q++;
	}
	return 0;
}

size_t strlen(const char *s)
{
	const char *p = s;
	while (*p)
		p++;
	return p - s;
}

int strcmp(const char *a, const char *b)
{
	while (*a && *a == *b) {
		a++;
		b++;
	}
	return (unsigned char)*a - (unsigned char)*b;
}

int strncmp(const char *a, const char *b, size_t n)
{
	while (n && *a && *a == *b) {
		a++;
		b++;
		n--;
	}
	if (n == 0)
		return 0;
	return (unsigned char)*a - (unsigned char)*b;
}

char *strchr(const char *s, int c)
{
	for (; *s; s++)
		if (*s == (char)c)
			return (char *)s;
	return (c == 0) ? (char *)s : (char *)0;
}

int atoi(const char *s)
{
	int sign = 1, v = 0;

	while (*s == ' ' || *s == '\t' || *s == '\n' || *s == '\r')
		s++;
	if (*s == '-') {
		sign = -1;
		s++;
	} else if (*s == '+') {
		s++;
	}
	while (*s >= '0' && *s <= '9')
		v = v * 10 + (*s++ - '0');
	return sign * v;
}

/*
 * setjmp() (a macro in <setjmp.h>) yields tg_longjmp_val after a longjmp.
 * __builtin_longjmp cannot carry a value, so longjmp() stashes it here.
 */
int tg_longjmp_val;

void longjmp(jmp_buf env, int val)
{
	tg_longjmp_val = val ? val : 1;
	__builtin_longjmp(env, 1);
}
