/*
 *  ThunderGate freestanding libc shim -- <stdlib.h>
 *
 *  uBASIC uses malloc()/free() for its line-number index and exit() on a
 *  syntax error; its tokenizer uses atoi(). fw/libc_min.c provides minimal
 *  versions: a small fixed-pool allocator, and an exit() that longjmp()s
 *  back to the uBASIC REPL driver rather than halting the core.
 */
#ifndef _TG_STDLIB_H
#define _TG_STDLIB_H

#include <stddef.h>

void *malloc(size_t n);
void free(void *p);
void exit(int code) __attribute__((noreturn));
int atoi(const char *s);

#endif
