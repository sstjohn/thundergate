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
    pass

is_struct = lambda c: Structure in c.__bases__
is_union = lambda c: Union in c.__bases__
is_bf = lambda o: len(o._fields_[0]) == 3

def _collapse_anon(o, anon):
    if anon is not None:
        keys = o.__dict__.keys()
        for k in keys:
            if k in anon:
                ao = getattr(o, k)
                for sk in ao.__dict__:
                    so = getattr(ao, sk)
                    setattr(o, sk, so)
                delattr(o, k)
    return o
            
def _model_bf(o):
    model = DeviceModel()
    for name, cl, bitlen in o._fields_:
        setattr(model, name, cl)
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
            am = getattr(o, "_anonymous_", None)
            setattr(model, name, _collapse_anon(sm, am))
        else:
            setattr(model, name, cl)
    return model

def model_device(device):
    model = DeviceModel()
    for block in device.blocks:
        block_name = block.__class__.__name__
        anonymous_members = getattr(block, "_anonymous_", None)
        if block_name[-2:] == "_x":
            block_name = block_name[:-2]
        if block_name[-5:] == "_regs":
            block_name = block_name[:-5]
        block_model = _collapse_anon(_model(block), anonymous_members)
        setattr(model, block_name, block_model)
    return model
