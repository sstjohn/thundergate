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
 * Console: the seam between the firmware substrate and whichever language
 * interpreter is linked in. A REPL exchange is request/response -- one
 * inbound line in, one buffer of output back -- so the interpreter writes
 * its output through con_*() into a single reply buffer that the UDP
 * console service (fw/net/udp.c) then drains into one datagram.
 *
 * The buffer is capped at one datagram's worth; output past the cap is
 * dropped and the buffer is finished with a "..." marker.
 */
#ifndef _CONSOLE_H_
#define _CONSOLE_H_

/* Output sink -- the interpreter calls these. */
void con_putc(char c);
void con_puts(const char *s);              /* NUL-terminated */
void con_write(const char *p, unsigned n); /* counted */
void con_puti(int v);                      /* signed decimal */
void con_putu(unsigned v);                 /* unsigned decimal */

/* Reply-buffer access -- the transport (udp.c) calls these. */
void con_out_reset(void);
const char *con_out_buf(void);
unsigned con_out_len(void);
int con_truncated(void);                   /* 1 if output hit the cap */

/*
 * Interpreter payload -- defined by the language object linked into the
 * image (fw/extern/zforth/zforth_glue.c or fw/extern/ubasic/repl.c).
 * interp_init() runs once at start-up; interp_eval_line() evaluates one
 * REPL line, leaving all output in the console buffer.
 */
void interp_init(void);
void interp_eval_line(const char *line, unsigned len);

#endif
