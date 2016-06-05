.PHONY: all clean

include ../Make.common

CLIB_HEADERS=unistd.h sys/mman.h sys/types.h sys/stat.h fcntl.h stdlib.h malloc.h string.h sys/socket.h $(PROJ_ROOT)/misc/vfio.h sys/ioctl.h sys/eventfd.h errno.h linux/if.h

all: tglib.py clib.py tunlib.py

tglib.py: tglib.xml
	xml2py tglib.xml -o tglib.py

tglib.xml: $(PROJ_ROOT)/include/*.h
	h2xml -I$(PROJ_ROOT)/include -c $(shell ls $(PROJ_ROOT)/include) -o tglib.xml 

clib.py: clib.xml
	xml2py clib.xml -l libc.so.6 -o clib.py > /dev/null

clib.xml: Makefile
	h2xml -q -c $(CLIB_HEADERS) -o clib.xml

tunlib.py: tunlibgen
	./tunlibgen > tunlib.py

clean:
	rm -f tglib.py tglib.xml clib.py clib.xml tunlib.py *.pyc
