# ThunderGate -- dmarf, the UEFI PCI option-ROM driver.
#
# Builds dmarf.rom for x86_64 and aarch64. (Apple Silicon firmware will
# not load a PCI option ROM, but other ARM UEFI platforms will.)
#
# Toolchain: clang + ld.lld cross-compile every EFI arch from one host;
# GNU objcopy does the ELF->PE conversion (its efi-bsdrv-* output
# targets are not implemented by llvm-objcopy). Every tool variable is
# overridable on the command line.
#   Linux:  install  clang lld binutils   -- all used straight off PATH
#   macOS:  brew install llvm lld binutils -- Apple's toolchain is
#           Mach-O only; the Homebrew kegs are keg-only, hence the paths
# The .rom step needs eficompressor in the project virtualenv:
#   .venv/bin/pip install ext/python-eficompressor
# gnu-efi is built automatically from the ext/gnu-efi submodule.

include ../Make.common

ARCHES  := x86_64 aarch64
GNUEFI  := $(PROJ_ROOT)/ext/gnu-efi
EFIROM  := $(PROJ_ROOT)/.venv/bin/python3 $(PROJ_ROOT)/py/efirom.py
SRCS    := main.c splash.c werk.c iort.c

# --- toolchain (override any of these on the command line) ----------
ifeq ($(shell uname -s),Darwin)
  CLANG   ?= /opt/homebrew/opt/llvm/bin/clang
  LLD     ?= /opt/homebrew/opt/lld/bin/ld.lld
  AR      ?= /opt/homebrew/opt/llvm/bin/llvm-ar
  RANLIB  ?= /opt/homebrew/opt/llvm/bin/llvm-ranlib
  OBJCOPY ?= /opt/homebrew/opt/binutils/bin/objcopy
else
  CLANG   ?= clang
  LLD     ?= ld.lld
  AR      ?= llvm-ar
  RANLIB  ?= llvm-ranlib
  OBJCOPY ?= objcopy
endif

ifeq ($(ARCH),)
# ==== top level: build the option ROM for every arch ================
all: $(foreach a,$(ARCHES),dmarf-$(a).rom)

dmarf-%.rom: gnuefi-%
	$(MAKE) ARCH=$* dmarf-$*.rom

# Build gnu-efi's support libraries for one arch, once. elf-shim
# supplies a minimal <elf.h> (macOS has none) for gnu-efi's relocator.
gnuefi-%:
	@test -f $(GNUEFI)/$*/gnuefi/libgnuefi.a || \
	  CPATH=$(CURDIR)/elf-shim $(MAKE) -C $(GNUEFI) ARCH=$* \
	    CC="$(CLANG) --target=$*-pc-linux-gnu" \
	    AS="$(CLANG) --target=$*-pc-linux-gnu" \
	    LD="$(LLD)" AR="$(AR)" RANLIB="$(RANLIB)" OBJCOPY="$(OBJCOPY)" \
	    HOSTCC="$(CLANG)" lib gnuefi

clean:
	-rm -rf $(ARCHES) dmarf-*.so dmarf-*.efi dmarf-*.rom

distclean: clean
	-for a in $(ARCHES); do \
	  $(MAKE) -C $(GNUEFI) ARCH=$$a clean 2>/dev/null || true; done

.PHONY: all clean distclean $(foreach a,$(ARCHES),gnuefi-$(a))

else
# ==== per-arch build (recursive invocation, ARCH set) ===============
TRIPLE  := $(ARCH)-pc-linux-gnu
OBJS    := $(addprefix $(ARCH)/,$(SRCS:.c=.o))
EFIINC  := $(GNUEFI)/inc

CFLAGS  := --target=$(TRIPLE) \
           -I$(EFIINC) -I$(EFIINC)/$(ARCH) -I$(EFIINC)/protocol \
           -I$(PROJ_ROOT)/include \
           -Os -fpic -fshort-wchar -fno-strict-aliasing -ffreestanding \
           -fno-stack-protector -fno-stack-check -std=c11 -D__KERNEL__ \
           -DCONFIG_$(ARCH)
ifeq ($(ARCH),x86_64)
  CFLAGS += -mno-red-zone -mno-mmx -mno-sse -DGNU_EFI_USE_MS_ABI
endif

LDFLAGS := -nostdlib --warn-common --no-undefined --fatal-warnings \
           -shared -Bsymbolic -s --defsym=EFI_SUBSYSTEM=0xb

CRT     := $(GNUEFI)/$(ARCH)/gnuefi/crt0-efi-$(ARCH).o
LDS     := $(GNUEFI)/gnuefi/elf_$(ARCH)_efi.lds
LIBS    := $(GNUEFI)/$(ARCH)/lib/libefi.a \
           $(GNUEFI)/$(ARCH)/gnuefi/libgnuefi.a

MACHINE_x86_64  := 0x8664
MACHINE_aarch64 := 0xaa64

dmarf-$(ARCH).rom: dmarf-$(ARCH).efi
	$(EFIROM) -v 0x14e4 -d 0x1682 -m $(MACHINE_$(ARCH)) $< $@

# ELF -> PE/COFF. objcopy's efi-bsdrv-* target synthesises the PE
# header and marks the image a boot-service driver.
dmarf-$(ARCH).efi: dmarf-$(ARCH).so
	$(OBJCOPY) -j .text -j .sdata -j .data -j .dynamic -j .rodata \
	  -j .rel -j .rela -j .rel.* -j .rela.* -j .rel* -j .rela* \
	  -j .areloc -j .reloc --output-target efi-bsdrv-$(ARCH) $< $@

dmarf-$(ARCH).so: $(OBJS) $(CRT) $(LDS) $(LIBS)
	$(LLD) $(LDFLAGS) $(CRT) $(OBJS) $(LIBS) -T $(LDS) -o $@

$(ARCH)/%.o: %.c dmarf.h | $(ARCH)
	$(CLANG) $(CFLAGS) -c $< -o $@

$(ARCH):
	mkdir -p $(ARCH)

endif
