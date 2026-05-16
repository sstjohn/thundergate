.PHONY: all clean

include ../Make.common

# tglib.py - ctypes bindings for the Tigon3 register and structure headers,
# generated from include/*.h with ctypesgen (Python 3).
#
# The old clib.py / clib.xml (built by the long-dead h2xml/xml2py) are gone;
# the libc and VFIO ABI is now the hand-written cabi.py. tunlib.py (built by
# tunlibgen) is likewise gone; the TAP driver uses fcntl.ioctl directly.

all: tglib.py

tglib.py: $(PROJ_ROOT)/include/*.h
	ctypesgen -I $(PROJ_ROOT)/include --no-macro-warnings -o tglib.py $(PROJ_ROOT)/include/*.h

clean:
	rm -f tglib.py *.pyc
	rm -rf __pycache__
