/*
 * Minimal <elf.h> for building gnu-efi on hosts that lack one (macOS).
 *
 * gnu-efi's position-independent relocator (gnuefi/reloc_<arch>.c) is the
 * only part of the build that includes <elf.h>, and it touches just the
 * ELF64 dynamic / relocation definitions below. These are fixed by the
 * ELF specification, so a tiny self-contained header is sufficient and
 * avoids depending on a Linux/glibc sysroot for the cross build.
 *
 * Put on the compiler's include path (CPATH) only while building gnu-efi.
 */
#ifndef _ELF_H
#define _ELF_H

#include <stdint.h>

typedef uint64_t Elf64_Addr;
typedef uint64_t Elf64_Xword;
typedef int64_t  Elf64_Sxword;

typedef struct {
	Elf64_Sxword d_tag;
	union {
		Elf64_Xword d_val;
		Elf64_Addr  d_ptr;
	} d_un;
} Elf64_Dyn;

typedef struct {
	Elf64_Addr  r_offset;
	Elf64_Xword r_info;
} Elf64_Rel;

typedef struct {
	Elf64_Addr   r_offset;
	Elf64_Xword  r_info;
	Elf64_Sxword r_addend;
} Elf64_Rela;

/* relocation type is the low 32 bits of r_info */
#define ELF64_R_TYPE(i)  ((i) & 0xffffffffUL)

/* dynamic-section tags */
#define DT_NULL     0
#define DT_RELA     7
#define DT_RELASZ   8
#define DT_RELAENT  9

/* relocation types applied by the gnu-efi relocator */
#define R_X86_64_NONE       0
#define R_X86_64_RELATIVE   8
#define R_AARCH64_NONE      0
#define R_AARCH64_RELATIVE  1027

#endif /* _ELF_H */
