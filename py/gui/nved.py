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
 
import os
import wx
import wx.dataview
import threading

class NvFwProgress(wx.Dialog):
    def __init__(self, parent, total, title = "progress"):
        super(NvFwProgress, self).__init__(parent, title = title)
        self.total = total
        self.progress = wx.Gauge(self, range = total)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def updateProgress(self, val):
        wx.CallAfter(self._updateProgress, val)

    def _updateProgress(self, val):
        self.progress.SetValue(val)
        if val == self.total:
            self.EndModal(0)

class NvDirectoryListCtrl(wx.dataview.DataViewListCtrl):
    def __init__(self, parent, dev, *args, **kargs):
        self.dev = dev
        super(NvDirectoryListCtrl, self).__init__(parent, *args, **kargs)
        self.AppendTextColumn("idx")
        self.AppendTextColumn("type")
        self.AppendTextColumn("nv_ofs")
        self.AppendTextColumn("load_ofs")
        self.AppendTextColumn("size")
        self._populate()

    def _populate(self):
        self.DeleteAllItems()
        self.dev.nvram.acquire_lock()
        directory = self.dev.nvram.get_directory(force_reload = True)
        self.dev.nvram.relinquish_lock()

        hexify = lambda x: "%x" % x

        for i in directory:
            self.AppendItem(map(hexify, i))

def _nvsave(dev, path, updater):
        dev.nvram.acquire_lock()
        dev.nvram.dump_eeprom(path, updater=updater)
        dev.nvram.relinquish_lock()

class NvramEditor(wx.Panel):
    def __init__(self, parent, dev, *args, **kwargs):
        self.dev = dev
        self.dev.nvram.access_enable()
        super(NvramEditor, self).__init__(parent, *args, **kwargs)
        outer = wx.BoxSizer(wx.VERTICAL)
        image_sl_buttons = wx.BoxSizer(wx.HORIZONTAL)
        nvsave = wx.Button(self, label = "save nvram")
        self.Bind(wx.EVT_BUTTON, self.OnNvSave, nvsave)
        nvload = wx.Button(self, label = "load nvram")
        self.Bind(wx.EVT_BUTTON, self.OnNvLoad, nvload)
        image_sl_buttons.Add(nvsave, 0, wx.ALIGN_LEFT)
        image_sl_buttons.Add(nvload, 0, wx.ALIGN_RIGHT)
        outer.Add(
                item = image_sl_buttons, 
                proportion = 0, 
                flag = wx.ALIGN_TOP | wx.ALIGN_CENTER | wx.BOTTOM, 
                border=5)
        self.nved = NvDirectoryListCtrl(self, dev)
        outer.Add(
                item = self.nved, 
                proportion = 1, 
                flag = wx.ALIGN_CENTER | wx.EXPAND)
        esave = wx.Button(self, label = "save entry")
        eload = wx.Button(self, label = "load entry")
        erase = wx.Button(self, label = "erase entry")
        entry_sld_buttons = wx.BoxSizer(wx.HORIZONTAL)
        entry_sld_buttons.Add(esave, 0, wx.ALIGN_LEFT)
        entry_sld_buttons.Add(eload, 0, wx.ALIGN_CENTER)
        entry_sld_buttons.Add(erase, 0, wx.ALIGN_RIGHT)
        outer.Add(
                entry_sld_buttons,
                proportion = 0, 
                flag = wx.ALIGN_BOTTOM | wx.ALIGN_CENTER | wx.TOP,
                border = 5)
        self.SetSizer(outer)

    def OnNvSave(self, event):
        saveFileDialog = wx.FileDialog(
                self, "Save BIN file", "", "",
                "BIN files (*.bin)|*.bin", 
                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        
        path = saveFileDialog.GetPath()
        self.dev.nvram.acquire_lock()
        progress = NvFwProgress(
                self, 
                self.dev.nvram.eeprom_len, 
                title = "reading nvram")
        self.dev.nvram.relinquish_lock()
        t = threading.Thread(
                target=_nvsave, 
                args=(self.dev, path, progress.updateProgress))
        t.start()
        progress.ShowModal()

    def OnNvLoad(self, event):
        openFileDialog = wx.FileDialog(
                self, "Open BIN file", "", "",
                "BIN files (*.bin)|*.bin",
                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return

        path = openFileDialog.GetPath()
        size = os.path.getsize(path)
        progress = NvFwProgress(self, size, title = "writing nvram")
        t = threading.Thread(
                target=_nvload,
                args = (self.dev, path, progress.updateProgress))
        t.start()
        progress.ShowWindowModal()
        self.nved._populate()



def _nvload(dev, path, updater):
        dev.nvram.acquire_lock()
        dev.nvram.write_enable()
        dev.nvram.write_eeprom(path, updater=updater)
        dev.nvram.write_disable()
        dev.nvram.relinquish_lock()
