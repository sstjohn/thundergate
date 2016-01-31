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

class DeviceModel(object):
    def __init__(self, name = None, parent = None):
        self.parent = parent
        self.name = name
        self.children = []

is_struct = lambda c: Structure in c.__bases__
is_union = lambda c: Union in c.__bases__
is_bf = lambda o: len(o._fields_[0]) == 3

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
    model = DeviceModel()
    for name, cl, bitlen in o._fields_:
        sm = DeviceModel(name = name, parent = model)
        sm.val_type = cl.__name__
        model.children.append(sm)
    return model

def _model(o):
    if is_bf(o):
        return _model_bf(o)

    model = DeviceModel()
    fields = getattr(o, "_fields_")
    for name, cl in fields:
        if is_struct(cl) or is_union(cl):
            so = getattr(o, name)
            sm = _model(so)
            sm.name = name
            sm.parent = model
            am = getattr(o, "_anonymous_", None)
            model.children.append(_collapse_anon(sm, am))
        else:
            sm = DeviceModel(name = name, parent = model)
            sm.val_type = cl.__name__
            model.children.append(sm)

    return model

def model_device(device):
    model = DeviceModel(name = "device")
    for block in device.blocks:
        block_name = block.__class__.__name__
        anonymous_members = getattr(block, "_anonymous_", None)
        if block_name[-2:] == "_x":
            block_name = block_name[:-2]
        if block_name[-5:] == "_regs":
            block_name = block_name[:-5]
        block_model = _collapse_anon(_model(block), anonymous_members)
        block_model.name = block_name
        block_model.parent = model
        model.children.append(block_model)
    return model
