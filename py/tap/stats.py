'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016  Saul St. John

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

_ctr_inc = lambda x, y: tuple(map(sum, zip(x, (1, y))))

class TapStatistics(object):
    def __init__(self):
        self.reset(True)

    def reset(self, quiet = False):
        self.inbound = (0, 0)
        self.outbound = (0, 0)
        if not quiet:
            print "[+] statistics reset"


    def pkt_in(self, length):
        self.inbound = _ctr_inc(self.inbound, length)

    def pkt_out(self, length):
        self.outbound = _ctr_inc(self.outbound, length)

    def display(self):
        print
        print "\t\t\t statistics "
        print "\t\t\t------------"
        print
        print "inbound:\t%8d pkts\t\t%8d bytes" % self.inbound
        print "outbound:\t%8d pkts\t\t%8d bytes" % self.outbound
        print
        print
