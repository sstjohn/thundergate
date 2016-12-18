.PHONY: all clean

include ../Make.common

CLIB_HEADERS=unistd.h sys/mman.h sys/types.h sys/stat.h fcntl.h stdlib.h malloc.h string.h sys/socket.h $(PROJ_ROOT)/misc/vfio.h sys/ioctl.h sys/eventfd.h errno.h linux/if.h

all: tglib.py clib.py tunlib.py

tglib.py: $(PROJ_ROOT)/include/*.h
	ctypesgen.py -I$(PROJ_ROOT)/include -o tglib.py --no-macros $(shell ls $(PROJ_ROOT)/include/*.h) 

clib.py: clib.xml
	xml2py clib.xml -l libc.so.6 -o clib.py > /dev/null

clib.xml: Makefile
	h2xml -q -c $(CLIB_HEADERS) -o clib.xml

tunlib.py: tunlibgen
	./tunlibgen > tunlib.py

clean:
	rm -f tglib.py tglib.xml clib.py clib.xml tunlib.py *.pyc
