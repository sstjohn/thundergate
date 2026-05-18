# leechcore_device_thundergate -- LeechCore device plugin for ThunderGate.
# Drop this directory into a LeechCore-plugins checkout (alongside
# leechcore_device_skeleton) and run `make`.

CC ?= cc
UNAME := $(shell uname)

CFLAGS  += -I. -I../includes -fPIC -fvisibility=hidden -g -Wall -Wno-unused-variable
OBJ = leechcore_device_thundergate.o

ifeq ($(UNAME), Darwin)
  OUT = leechcore_device_thundergate.dylib
  LDFLAGS += -dynamiclib -L. -lleechcore -Wl,-rpath,@loader_path
else
  CFLAGS  += -D LINUX
  OUT = leechcore_device_thundergate.so
  LDFLAGS += -shared -L. -l:leechcore.so -Wl,-rpath,'$$ORIGIN' -ldl
endif

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

all: $(OBJ)
	cp ../files/leechcore.* . 2>/dev/null || true
	$(CC) -o $(OUT) $(OBJ) $(CFLAGS) $(LDFLAGS)
	mkdir -p ../files
	mv $(OUT) ../files/
	rm -f *.o *.so *.dylib 2>/dev/null || true

clean:
	rm -f *.o *.so *.dylib
