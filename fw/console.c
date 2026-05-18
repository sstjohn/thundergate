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

#include "console.h"

/*
 * One REPL reply is one UDP datagram. net_tx() carries at most NET_TX_MAX
 * (320) bytes, of which the Ethernet/IP/UDP headers take ~62; 256 leaves
 * comfortable headroom and is the hard cap on a single reply.
 */
#define CON_OUT_MAX 256

static char con_buf[CON_OUT_MAX];
static unsigned con_len;
static int con_trunc;

void con_out_reset(void)
{
	con_len = 0;
	con_trunc = 0;
}

const char *con_out_buf(void) { return con_buf; }
unsigned con_out_len(void)    { return con_len; }
int con_truncated(void)       { return con_trunc; }

void con_putc(char c)
{
	if (con_len < CON_OUT_MAX - 3) {
		con_buf[con_len++] = c;
	} else if (!con_trunc) {
		/* Reserve the last three bytes for a truncation marker. */
		con_trunc = 1;
		con_buf[con_len++] = '.';
		con_buf[con_len++] = '.';
		con_buf[con_len++] = '.';
	}
}

void con_puts(const char *s)
{
	while (*s)
		con_putc(*s++);
}

void con_write(const char *p, unsigned n)
{
	while (n--)
		con_putc(*p++);
}

void con_putu(unsigned v)
{
	char tmp[10];
	int i = 0;

	if (v == 0) {
		con_putc('0');
		return;
	}
	while (v) {
		tmp[i++] = '0' + (v % 10);
		v /= 10;
	}
	while (i)
		con_putc(tmp[--i]);
}

void con_puti(int v)
{
	if (v < 0) {
		con_putc('-');
		con_putu(-(unsigned)v);
	} else {
		con_putu((unsigned)v);
	}
}
