/*
 *  ThunderGate freestanding libc shim -- <setjmp.h>
 *
 *  zForth uses setjmp()/longjmp() to unwind out of an aborted evaluation.
 *  There is no C library, so this is built on GCC's __builtin_setjmp /
 *  __builtin_longjmp (a 5-word buffer, no headers needed).
 *
 *  __builtin_longjmp always makes __builtin_setjmp return 1, so it cannot
 *  carry a value itself. longjmp() stashes the caller's value in the global
 *  tg_longjmp_val and the setjmp() macro reads it back -- giving ordinary
 *  value-passing semantics. zForth runs one evaluation at a time, so a
 *  single global is sufficient. Definitions live in fw/libc_min.c.
 */
#ifndef _TG_SETJMP_H
#define _TG_SETJMP_H

typedef void *jmp_buf[5];

extern int tg_longjmp_val;
void longjmp(jmp_buf env, int val) __attribute__((noreturn));

#define setjmp(env) (__builtin_setjmp(env) ? tg_longjmp_val : 0)

#endif
