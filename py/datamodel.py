'''
    ThunderGate - an open source toolkit for PCI bus exploration
    Copyright (C) 2015-2016 Saul St. John

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

from ctypes import Structure, Union
from device import tg3_blocks, tg3_mem

class GenericModel(object):
    def __init__(self, name = None, parent = None):
        self.parent = parent
        self.name = name
        self.children = []

class MemoryModel(GenericModel):
    pass

class RegisterModel(GenericModel):
    pass

is_struct = lambda c: Structure in c.__bases__
is_union = lambda c: Union in c.__bases__
is_parray = lambda o: hasattr(o, "__iter__")
is_bf = lambda o: hasattr(o, "_fields_") and (len(o._fields_[0]) == 3)

def _collapse_anon(o, anon):
    if anon is not None:
        to_remove = []
        for child in o.children:
            if child.name in anon:
                to_remove.append(child)
                for sc in child.children:
                    sc.parent = o
                    o.children.append(sc)

        for ac in to_remove:
            o.children.remove(ac)
    return o
            
def _model_bf(o):
    model = GenericModel()
    for name, cl, bitlen in o._fields_:
        sm = GenericModel(name = name, parent = model)
        sm.val_type = cl.__name__
        model.children.append(sm)
    return model

def _model_parray(o):
    model = GenericModel()
    for i in o:
        sm = GenericModel(name = "[%d]")
        sm = _model(i)
        sm.parent = model
        model.children.append(sm)
    return model

def _model(o):
    if is_parray(o):
        return _model_parray(o)
    if is_bf(o):
        return _model_bf(o)

    model = GenericModel()
    fields = getattr(o, "_fields_", None)
    if fields is None:
        fields = [(n, type(getattr(o, n))) for n in filter(lambda x: x[0] != "_", o.__dict__)]
    for name, cl in fields:
        if is_struct(cl) or is_union(cl):
            so = getattr(o, name)
            sm = _model(so)
            sm.name = name
            sm.parent = model
            am = getattr(o, "_anonymous_", None)
            model.children.append(_collapse_anon(sm, am))
        else:
            sm = GenericModel(name = name, parent = model)
            sm.val_type = cl.__name__
            model.children.append(sm)

    return model

def model_registers(device):
    model = RegisterModel(name = "registers")
    for block_name, _, block_type in tg3_blocks:
        block = getattr(device, block_name)
        anonymous_members = getattr(block, "_anonymous_", None)
        block_model = _collapse_anon(_model(block), anonymous_members)
        block_model.name = block_name
        block_model.parent = model
        model.children.append(block_model)
    return model

def model_memory(device):
    model = MemoryModel(name = "memory")
    for seg_name, seg_type, _, count in tg3_mem:
        seg = getattr(device.mem, seg_name)
        anonymous_members = getattr(seg, "_anonymous_", None)
        seg_model = _collapse_anon(_model(seg), anonymous_members)
        seg_model.name = seg_name
        seg_model.parent = model
        model.children.append(seg_model)
    return model
