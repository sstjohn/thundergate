ARCH            = $(shell uname -m | sed s,i[3456789]86,ia32,)

include ../Make.common

EFI_OBJS        = main.o
TARGET          = dmarf.efi dmarf.rom
EFIROM		= $(PROJ_ROOT)/py/efirom.py
TGINC		= -I$(PROJ_ROOT)/include
EFIINC          = /usr/include/efi
EFIINCS         = -I$(EFIINC) -I$(EFIINC)/$(ARCH) -I$(EFIINC)/protocol
EFILIB          = /usr/lib
EFI_CRT_OBJS    = $(EFILIB)/crt0-efi-$(ARCH).o
EFI_LDS         = $(EFILIB)/elf_$(ARCH)_efi.lds
LIB_GCC         = $(shell $(CC) -print-libgcc-file-name)
CFLAGS          = $(EFIINCS) $(TGINC) -mno-red-zone -mno-mmx -mno-sse \
		  -Os -fpic -fshort-wchar -fno-strict-aliasing \
		  -fno-merge-constants -ffreestanding -fno-stack-protector \
		  -fno-stack-check -DCONFIG_x86_64 -DGNU_EFI_USE_MS_ABI \
		  -maccumulate-outgoing-args --std=c11 -D__KERNEL__

LDFLAGS         = -nostdlib --warn-common --no-undefined --fatal-warnings \
		-shared -Bsymbolic -s -L$(EFILIB) $(EFI_CRT_OBJS)

all: $(TARGET)

clean:
	-rm *.o
	-rm *.so
	-rm *.efi
	-rm *.rom

dmarf.so: $(EFI_OBJS)
	ld $(LDFLAGS) $(EFI_OBJS) -o $@ -lefi -lgnuefi $(LIB_GCC) -T $(EFI_LDS)

%.efi: %.so
	objcopy -j .text -j .sdata -j .data -j .dynamic \
		-j .dynsym  -j .rel -j .rela -j .rel.* -j .rela.* \
		-j .rel* -j .rela* -j .reloc \
		--target efi-bsdrv-$(ARCH) $^ $@

%.rom: %.efi
	$(EFIROM) -v 0x14e4 -d 0x1682 $^ $@
