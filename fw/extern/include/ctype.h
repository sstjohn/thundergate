/*
 *  ThunderGate freestanding libc shim -- <ctype.h>
 *
 *  Defined inline: these are tiny and avoid pulling in another object.
 *  Only the classifiers the vendored interpreters use are provided.
 */
#ifndef _TG_CTYPE_H
#define _TG_CTYPE_H

static inline int isspace(int c)
{
	return c == ' ' || c == '\t' || c == '\n' ||
	       c == '\r' || c == '\v' || c == '\f';
}

static inline int isdigit(int c) { return c >= '0' && c <= '9'; }
static inline int isupper(int c) { return c >= 'A' && c <= 'Z'; }
static inline int islower(int c) { return c >= 'a' && c <= 'z'; }
static inline int isalpha(int c) { return isupper(c) || islower(c); }

#endif
