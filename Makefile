.PHONY: all clean dmarf py fw

BUILD=dmarf py fw

all: $(BUILD)

dmarf:
	cd dmarf; make

fw:
	cd fw; make

py:
	cd py; make

clean:
	-cd dmarf; make clean
	-cd fw; make clean
	-cd py; make clean
