ARCH            = $(shell uname -m | sed s,i[3456789]86,ia32,)

include ../Make.common

EFI_OBJS        = main.o splash.o werk.o
TARGET          = dmarf.efi dmarf.rom
EFIROM		= $(PROJ_ROOT)/py/efirom.py
TGINC		= -I$(PROJ_ROOT)/include
EFIINC          = $(PROJ_ROOT)/ext/gnu-efi/inc
EFIINCS         = -I$(EFIINC) -I$(EFIINC)/$(ARCH) -I$(EFIINC)/protocol
LIB_EFI         = $(PROJ_ROOT)/ext/gnu-efi/$(ARCH)/lib/libefi.a
LIB_GNUEFI	= $(PROJ_ROOT)/ext/gnu-efi/$(ARCH)/gnuefi/libgnuefi.a
EFI_CRT_OBJ     = $(PROJ_ROOT)/ext/gnu-efi/$(ARCH)/gnuefi/crt0-efi-$(ARCH).o
EFI_LDS         = $(PROJ_ROOT)/ext/gnu-efi/gnuefi/elf_$(ARCH)_efi.lds
LIB_GCC         = $(shell $(CC) -print-libgcc-file-name)
CFLAGS          = $(EFIINCS) $(TGINC) -mno-red-zone -mno-mmx -mno-sse \
		  -Os -fpic -fshort-wchar -fno-strict-aliasing \
		  -fno-merge-constants -ffreestanding -fno-stack-protector \
		  -fno-stack-check -DCONFIG_x86_64 -DGNU_EFI_USE_MS_ABI \
		  -maccumulate-outgoing-args --std=c11 -D__KERNEL__

LDFLAGS         = -nostdlib --warn-common --no-undefined --fatal-warnings \
		-shared -Bsymbolic -s

all: $(TARGET)

clean:
	-rm *.o
	-rm *.so
	-rm *.efi
	-rm *.rom

dmarf.so: $(EFI_OBJS) dmarf.h
	ld $(LDFLAGS) $(EFI_CRT_OBJ) $(EFI_OBJS) $(LIB_EFI) $(LIB_GNUEFI) $(LIB_GCC) -T $(EFI_LDS) -o $@

%.efi: %.so
	objcopy -j .text -j .sdata -j .data -j .dynamic \
		-j .dynsym  -j .rel -j .rela -j .rel.* -j .rela.* \
		-j .rel* -j .rela* -j .reloc \
		--target efi-bsdrv-$(ARCH) $^ $@

%.rom: %.efi
	$(EFIROM) -v 0x14e4 -d 0x1682 $^ $@
