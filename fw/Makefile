CC=mips-linux-gnu-gcc
LD=mips-linux-gnu-ld
OBJCOPY=mips-linux-gnu-objcopy

include ../Make.common

INCLUDE=-I$(PROJ_ROOT)/include
CFLAGS=-mtune=r6000 -mips2 -G 0 -fno-pic -fno-builtin -fverbose-asm  -mno-shared -mno-abicalls -mno-llsc -s -O0 -mno-split-addresses -mtigon -ggdb -std=gnu11
LDFLAGS=-nostdlib --build-id=none -Timage.x -static -Rfixed.sym

IMAGE=nvimage

CSOURCE=app.c
CHEADERS=$(shell ls $(PROJ_ROOT)/include)

ASOURCE=main.S

ASFLAGS=$(CFLAGS)
CPPFLAGS=$(INCLUDE)

OBJECTS=$(CSOURCE:.c=.o) $(ASOURCE:.S=.o)

all: fw.elf $(IMAGE)

fw.elf: image.x fixed.sym $(OBJECTS)
	$(LD) $(LDFLAGS) $(OBJECTS) -o fw.elf

fixed.sym: $(PROJ_ROOT)/py/symgen.py
	sh -c "cd $(PROJ_ROOT); py/symgen.py > fw/fixed.sym"

$(IMAGE): fw.elf
	$(OBJCOPY) -j .text -j .data -j .rodata -j .bss -O binary fw.elf $(IMAGE)
	crc32 $(IMAGE) | tr -d '\n' >> $(IMAGE)

clean:
	rm -f $(OBJECTS) fw.elf nvimage .depend fixed.sym

depend: .depend

.depend: $(CSOURCE)
	rm -f ./.depend
	$(CC) $(CFLAGS) $(CPPFLAGS) -MM $^ -MF ./.depend;

include .depend
