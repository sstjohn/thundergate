/*
 *  zForth build configuration for the ThunderGate Tigon3 firmware.
 *
 *  This is the per-port zfconf.h that zForth expects (upstream ships one
 *  per target under src/<port>/). zforth.c and zforth.h are vendored
 *  unmodified; all target-specific choices live here.
 */
#ifndef zfconf
#define zfconf

#include <stdint.h>

/* Tracing pulls in printf-style formatting and is dropped to save space. */
#define ZF_ENABLE_TRACE 0

/* Stack boundary checks: ~100 bytes, and they turn a stack slip into a
 * clean abort instead of dictionary corruption -- worth keeping. */
#define ZF_ENABLE_BOUNDARY_CHECKS 1

/* The dictionary is bootstrapped at start-up (primitives + core.zf). */
#define ZF_ENABLE_BOOTSTRAP 1

/* Typed (8/16/32-bit) memory access is unused by core.zf -- drop it. */
#define ZF_ENABLE_TYPED_MEM_ACCESS 0

/* The Tigon3 core has no FPU, so the cell is a 32-bit integer. */
typedef int32_t zf_cell;
#define ZF_CELL_FMT "%d"

/* zf_int is used for bit operations; match the cell width. */
typedef int32_t zf_int;

/* Dictionary addresses. */
typedef unsigned int zf_addr;
#define ZF_ADDR_FMT "%04x"

/* Dictionary size in bytes; stack sizes in cells. The whole zf_ctx
 * (~4.5 KB) lands in .bss -- see the 32 KB scratch-pad budget. */
#define ZF_DICT_SIZE 4096
#define ZF_DSTACK_SIZE 32
#define ZF_RSTACK_SIZE 32

#endif
