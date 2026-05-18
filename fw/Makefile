CC=mips-elf-gcc
LD=mips-elf-ld
OBJCOPY=mips-elf-objcopy

include ../Make.common

# fw/extern/include holds the freestanding libc shim headers the vendored
# interpreters need; harmless on the substrate's include path.
INCLUDE=-I$(PROJ_ROOT)/include -I$(PROJ_ROOT)/fw -I$(PROJ_ROOT)/fw/extern/include

# ---- module selection -------------------------------------------------------
# Each switch compiles a module entirely out when set to 0. Override on the
# command line, e.g.   make UBASIC=0   |   make GATE=0 BEACON=0
#
# Always built (the substrate): boot, hardware init, the on-core TCP/IP
# stack, the UDP console transport and the interpreter dispatcher.
#   ZFORTH  the zForth interpreter
#   UBASIC  the uBASIC interpreter
#   GATE    the control surface: 0x88b5 protocol, DMA, cloak, lgate
#   BEACON  the link beacon
ZFORTH ?= 1
UBASIC ?= 1
GATE   ?= 1
BEACON ?= 1

# -fcommon: map.h declares the register-block globals as tentative
# definitions and relies on the linker merging them. GCC 10+ defaults to
# -fno-common, which turns those into multiple definitions; restore the
# pre-GCC-10 behaviour the firmware was written against.
CFLAGS=-mips2 -march=r6000 -mfix-r4000 -fcommon -G 0 -fno-pic -fno-builtin -fverbose-asm  -mno-shared -mno-abicalls -mno-llsc -s -mno-split-addresses -mtigon -msoft-float -g3 -std=gnu11 -Wall -Wno-main -gdwarf-4 -fvar-tracking -fno-dwarf2-cfi-asm -fno-omit-frame-pointer -funwind-tables
LDFLAGS=-nostdlib --build-id=none -Timage.x -static -Rfixed.sym
# libgcc supplies the soft multiply/divide routines a -mtigon build calls
# (__mulsi3/__divsi3/...); misc/build-toolchain.sh builds it for this target.
# -nostdlib drops the standard libraries, so libgcc is named explicitly on
# the link line below.
LIBGCC := $(shell $(CC) -print-libgcc-file-name)

# Substrate -- always linked.
COMMON=entry.o main.o init.o nvram.o phy.o util.o rx.o console.o interp.o \
	net/checksum.o net/ether.o net/coretx.o net/arp.o net/ip.o \
	net/icmp.o net/udp.o
OBJECTS=$(COMMON)
MODDEFS=

ifeq ($(ZFORTH),1)
  OBJECTS += extern/zforth/zforth.o extern/zforth/zforth_glue.o
  MODDEFS += -DTG_ZFORTH
endif
ifeq ($(UBASIC),1)
  OBJECTS += extern/ubasic/ubasic.o extern/ubasic/tokenizer.o extern/ubasic/repl.o
  MODDEFS += -DTG_UBASIC
endif
# The freestanding libc shim is pulled in only by the interpreters.
ifneq ($(ZFORTH)$(UBASIC),00)
  OBJECTS += libc_min.o
endif
ifeq ($(GATE),1)
  OBJECTS += handlers.o cloak.o lgate.o
  MODDEFS += -DTG_GATE
endif
ifeq ($(BEACON),1)
  OBJECTS += beacon.o
  MODDEFS += -DTG_BEACON
endif
# tx.c (crafted-frame TX) is shared by the GATE handlers and the beacon.
ifneq ($(GATE)$(BEACON),00)
  OBJECTS += tx.o
endif

CFLAGS += $(MODDEFS)

# The vendored interpreters (extern/) build with the same target flags but
# freestanding, with the shim include paths, -Os, and warnings off.
EXTERN_INC=-I$(PROJ_ROOT)/fw -I$(PROJ_ROOT)/fw/extern/include \
	-I$(PROJ_ROOT)/fw/extern/zforth -I$(PROJ_ROOT)/fw/extern/ubasic
EXTERN_CFLAGS=$(CFLAGS) -ffreestanding -Os -w

CPPFLAGS=$(INCLUDE)
ASFLAGS=$(CFLAGS)

IMAGE=fw.img

# Sources that are always built -- used to generate .depend.
DEPSRC=main.c init.c nvram.c phy.c util.c rx.c console.c interp.c \
	net/checksum.c net/ether.c net/coretx.c net/arp.c net/ip.c \
	net/icmp.c net/udp.c

.PHONY: all clean rebuild depend

# One firmware image. Loads at 0x08000000 (see image.x); load with
# py/blocks/cpu.py. Module set is whatever the switches above select.
all: $(IMAGE)

fw.elf: image.x fixed.sym $(OBJECTS)
	$(LD) $(LDFLAGS) $(OBJECTS) $(LIBGCC) -o fw.elf

$(IMAGE): fw.elf
	$(OBJCOPY) -j .text -j .data -j .rodata -j .bss -O binary fw.elf $(IMAGE)

# Vendored interpreter objects: freestanding, shim includes, -Os, no warnings.
extern/%.o: extern/%.c
	$(CC) $(EXTERN_CFLAGS) $(EXTERN_INC) -c -o $@ $<

# zForth's Forth bootstrap (core.zf) is compiled in as a C string. The
# generated header is committed, so a plain checkout builds without Python;
# this rule only refreshes it when core.zf changes.
extern/zforth/forth_core.h: extern/zforth/core.zf extern/zforth/embed-core.py
	python3 extern/zforth/embed-core.py
extern/zforth/zforth_glue.o: extern/zforth/forth_core.h

fixed.sym: $(PROJ_ROOT)/py/symgen.py $(PROJ_ROOT)/py/device.py map.h
	sh -c "cd $(PROJ_ROOT); .venv/bin/python3 py/symgen.py > fw/fixed.sym"

clean:
	-rm -f *.o net/*.o extern/zforth/*.o extern/ubasic/*.o \
		fw.elf fw.img .depend fixed.sym

rebuild:
	$(MAKE) clean && $(MAKE)

depend: .depend

.depend: $(DEPSRC)
	rm -f ./.depend
	for s in $(DEPSRC); do $(CC) $(CFLAGS) $(CPPFLAGS) -MM -MT $${s%.c}.o $$s >> ./.depend; done

include .depend
