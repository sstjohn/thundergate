

import wx
import wx.dataview

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

class NvramEditor(wx.Panel):
    def __init__(self, parent, dev, *args, **kwargs):
        self.dev = dev
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

        self.dev.nvram.acquire_lock()
        self.dev.nvram.dump_eeprom(saveFileDialog.GetPath())
        self.dev.nvram.relinquish_lock()

    def OnNvLoad(self, event):
        openFileDialog = wx.FileDialog(
                self, "Open BIN file", "", "",
                "BIN files (*.bin)|*.bin",
                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return

        self.dev.nvram.acquire_lock()
        self.dev.nvram.write_enable()
        self.dev.nvram.write_eeprom(openFileDialog.GetPath())
        self.dev.nvram.write_disable()
        self.dev.nvram.relinquish_lock()
        self.nved._populate()
