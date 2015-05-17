from ctypes import *

class _TEntry(Structure):
    _fields_ = [("addr_lo", c_uint32),
                ("addr_hi", c_uint32),
                ("data", c_uint32),
                ("ctrl", c_uint32)]

class Table(object):
    def __init__(self, bar, ofs, sz):
        self.bar = bar
        self.ofs = ofs
        self.sz = sz
        self._ptrs = []
        for i in range(sz):
            self._ptrs += [cast(bar + ofs, POINTER(_TEntry))[i]]

    def __len__(self):
        return self.sz

    def __getitem__(self, index):
        if index < 0 or index >= self.sz:
            raise IndexError()

        return self._ptrs[index]

class Pba(object):
    def __init__(self, bar, ofs, sz):
        self.bar = bar
        self.ofs = ofs
        self.sz = sz
