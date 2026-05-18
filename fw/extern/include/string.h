/*
 *  ThunderGate freestanding libc shim -- <string.h>
 *
 *  The mips-elf cross-toolchain is built without a C library, so the stock
 *  <string.h> does not exist. The vendored interpreters (zForth, uBASIC)
 *  expect it; these declarations let them compile unmodified. The matching
 *  definitions live in fw/libc_min.c.
 */
#ifndef _TG_STRING_H
#define _TG_STRING_H

#include <stddef.h>

void *memcpy(void *dst, const void *src, size_t n);
void *memmove(void *dst, const void *src, size_t n);
void *memset(void *dst, int c, size_t n);
int memcmp(const void *a, const void *b, size_t n);
size_t strlen(const char *s);
int strcmp(const char *a, const char *b);
int strncmp(const char *a, const char *b, size_t n);
char *strchr(const char *s, int c);

#endif
