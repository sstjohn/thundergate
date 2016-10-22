CC=mips-elf-gcc
#CC=clang-3.8
LD=mips-elf-ld
OBJCOPY=mips-elf-objcopy

include ../Make.common

INCLUDE=-I$(PROJ_ROOT)/include
CFLAGS=-mips2 -march=r6000 -mfix-r4000 -G 0 -fno-pic -fno-builtin -fverbose-asm  -mno-shared -mno-abicalls -mno-llsc -s -mno-split-addresses -mtigon -msoft-float -g3 -std=gnu11 -Wall -Wno-main -gdwarf-4 -fvar-tracking -fno-dwarf2-cfi-asm -fno-omit-frame-pointer
#CFLAGS=-fintegrated-as -ffreestanding -fno-builtin -fno-pic -msoft-float -gstrict-dwarf -gdwarf-2 -nostdlib -nostdinc -target mips-none-elf -march=mips2
LDFLAGS=-nostdlib --build-id=none -Timage.x -static -Rfixed.sym
LIBGCC=$(shell $(CC) -print-libgcc-file-name)

IMAGE=fw.img

CSOURCE=test.c #main.c init.c handlers.c nvram.c phy.c util.c beacon.c cloak.c rx.c tx.c lgate.c
CHEADERS=$(shell ls $(PROJ_ROOT)/include)

ASOURCE=entry.S

ASFLAGS=$(CFLAGS)
CPPFLAGS=$(INCLUDE)

OBJECTS=$(ASOURCE:.S=.o) $(CSOURCE:.c=.o) 

all: fw.elf $(IMAGE)

fw.elf: image.x fixed.sym $(OBJECTS)
	$(LD) $(LDFLAGS) $(OBJECTS) $(LIBGCC) -o fw.elf

fixed.sym: $(PROJ_ROOT)/py/symgen.py $(PROJ_ROOT)/py/device.py map.h
	sh -c "cd $(PROJ_ROOT); py/symgen.py > fw/fixed.sym"

$(IMAGE): fw.elf
	$(OBJCOPY) -j .text -j .data -j .rodata -j .bss -O binary fw.elf $(IMAGE)

clean:
	-rm -f $(OBJECTS) fw.elf fw.img .depend fixed.sym

depend: .depend

.depend: $(CSOURCE)
	rm -f ./.depend
	$(CC) $(CFLAGS) $(CPPFLAGS) -MM $^ -MF ./.depend;

include .depend
