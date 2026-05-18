/*
 *  ThunderGate freestanding libc shim -- <stdio.h>
 *
 *  uBASIC prints through printf(). fw/libc_min.c provides a minimal printf
 *  (%d, %u, %x, %c, %s) that writes into the console reply buffer instead
 *  of a real stdout.
 */
#ifndef _TG_STDIO_H
#define _TG_STDIO_H

int printf(const char *fmt, ...) __attribute__((format(printf, 1, 2)));

#endif
