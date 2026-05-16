# Host-side test of the on-core TCP/IP stack.
#
# The protocol code in fw/net/ builds unchanged with the host compiler;
# harness.c supplies mac_cpy()/net_tx() and exercises it with no NIC.
#
# Run:  make -C fw/net/test run

CC     ?= cc
ROOT   := ../../..
CFLAGS := -I$(ROOT)/include -Wall -g -O1

STACK := $(ROOT)/fw/net/checksum.c \
         $(ROOT)/fw/net/ether.c \
         $(ROOT)/fw/net/arp.c \
         $(ROOT)/fw/net/ip.c \
         $(ROOT)/fw/net/icmp.c \
         $(ROOT)/fw/net/udp.c

.PHONY: run clean

run: nettest
	./nettest

nettest: harness.c $(STACK)
	$(CC) $(CFLAGS) -o $@ harness.c $(STACK)

clean:
	rm -f nettest
