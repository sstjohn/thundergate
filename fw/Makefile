CC=mips-elf-gcc
LD=mips-elf-ld
OBJCOPY=mips-elf-objcopy

include ../Make.common

INCLUDE=-I$(PROJ_ROOT)/include -I$(PROJ_ROOT)/fw
# -fcommon: map.h declares the register-block globals as tentative
# definitions and relies on the linker merging them. GCC 10+ defaults to
# -fno-common, which turns those into multiple definitions; restore the
# pre-GCC-10 behaviour the firmware was written against.
CFLAGS=-mips2 -march=r6000 -mfix-r4000 -fcommon -G 0 -fno-pic -fno-builtin -fverbose-asm  -mno-shared -mno-abicalls -mno-llsc -s -mno-split-addresses -mtigon -msoft-float -g3 -std=gnu11 -Wall -Wno-main -gdwarf-4 -fvar-tracking -fno-dwarf2-cfi-asm -fno-omit-frame-pointer -funwind-tables
LDFLAGS=-nostdlib --build-id=none -Timage.x -static -Rfixed.sym
# The cross-toolchain is built without libgcc (GCC 14's libgcc2.c will
# not compile under -mtigon); the firmware supplies any soft-math it
# needs itself, so nothing extra is linked.

IMAGE=fw.img

CSOURCE=main.c init.c handlers.c nvram.c phy.c util.c beacon.c cloak.c rx.c tx.c lgate.c \
	net/checksum.c net/ether.c net/coretx.c net/arp.c net/ip.c \
	net/icmp.c net/udp.c #test.c
CHEADERS=$(shell ls $(PROJ_ROOT)/include)

ASOURCE=entry.S

ASFLAGS=$(CFLAGS)
CPPFLAGS=$(INCLUDE)

OBJECTS=$(ASOURCE:.S=.o) $(CSOURCE:.c=.o) 

all: fw.elf $(IMAGE)

fw.elf: image.x fixed.sym $(OBJECTS)
	$(LD) $(LDFLAGS) $(OBJECTS) -o fw.elf

fixed.sym: $(PROJ_ROOT)/py/symgen.py $(PROJ_ROOT)/py/device.py map.h
	sh -c "cd $(PROJ_ROOT); .venv/bin/python3 py/symgen.py > fw/fixed.sym"

$(IMAGE): fw.elf
	$(OBJCOPY) -j .text -j .data -j .rodata -j .bss -O binary fw.elf $(IMAGE)

clean:
	-rm -f *.o net/*.o fw.elf fw.img .depend fixed.sym

rebuild:
	$(MAKE) clean && $(MAKE)

depend: .depend

.depend: $(CSOURCE)
	rm -f ./.depend
	for s in $(CSOURCE); do $(CC) $(CFLAGS) $(CPPFLAGS) -MM -MT $${s%.c}.o $$s >> ./.depend; done

include .depend
