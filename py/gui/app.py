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

import wx
import wx.py
import threading
import functools
from tree import GenTree
from nved import NvramEditor
from datamodel import model_registers, model_memory

class ThunderSplash(wx.SplashScreen):
    def __init__(self, parent):
        img = wx.Image("misc/thunderlogo.png", wx.BITMAP_TYPE_PNG)
        bitmap = img.ConvertToBitmap()
        super(ThunderSplash, self).__init__(
                bitmap = bitmap,
                milliseconds = 0,
                splashStyle = wx.SPLASH_CENTER_ON_SCREEN | wx.SPLASH_NO_TIMEOUT,
                parent = parent)
        self.GetSplashWindow().SetBitmap(bitmap)

class App(wx.App):
    def __init__(self, dev, nosplash = False, daemon = False):
        self.dev = dev
        self.nosplash = nosplash
        self.daemon = daemon
        super(App, self).__init__()

    def OnInit(self):
        if self.daemon:
            self.toplevel = wx.Frame(None, -1)
        else:
            self.toplevel = None
        if self.nosplash:
            self.PrepareMain()
        else:
            self.ShowSplash()
        return True

    def ShowSplash(self):
        img = wx.Image('misc/thunderlogo.png', wx.BITMAP_TYPE_PNG)
        self.splash = ThunderSplash(self.toplevel)
        self.splash.Refresh()
        wx.Yield()
	wx.CallAfter(self.PrepareMain)

    def PrepareMain(self):
        self.main_frame = wx.Frame(self.toplevel, -1, 'thundergate')
        self.nb = wx.Notebook(self.main_frame)
	page = wx.NotebookPage(self.nb)
	wx.py.shell.Shell(page, locals = {"dev": self.dev})
	self.nb.AddPage(page, text = "console")
        self.bgthreads = []
        t = threading.Thread(
                target = self._collect_model,
                args = ("registers", model_registers))
        wx.CallAfter(t.start)
        self.bgthreads += [t]
        t = threading.Thread(
                target = self._collect_model,
                args = ("memory", model_memory))
        wx.CallAfter(t.start)
        self.bgthreads += [t]
        t = threading.Thread(target = self._wait_for_models)
        wx.CallAfter(t.start)

    def Invoke(self, fun):
        wx.CallAfter(fun)

    def _collect_model(self, name, modeler):
        res = modeler(self.dev)
        setattr(self, "%s_model" % name, res)
        notify = functools.partial(self._add_regtree, name)
        wx.CallAfter(notify)

    def _add_regtree(self, name):
        model = getattr(self, "%s_model" % name)
        page = GenTree(self.nb, model)
        self.nb.AddPage(page, text=name)

    def _wait_for_models(self):
        for t in self.bgthreads:
            t.join()
        wx.CallAfter(self._bgwork_done)

    def _bgwork_done(self):
        page = NvramEditor(self.nb, self.dev)
        self.nb.AddPage(page, text="nvram")
        self.main_frame.Show()

        if not self.nosplash:
            self.splash.Destroy()
