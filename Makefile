.PHONY: all clean efi py fw

BUILD=efi py fw

all: $(BUILD)

efi:
	cd efi; make

fw:
	cd fw; make

py:
	cd py; make

clean:
	-cd efi; make clean
	-cd fw; make clean
	-cd py; make clean
