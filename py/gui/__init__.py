import threading

def _run(dev, daemon = False):
    from app import App
    import wx
    _run.app = App(dev, daemon = daemon)
    _run.app.MainLoop()
    _run.app.Destroy()
    wx.Exit()

def run(dev):
    if hasattr(_run, "app"):
        _run.app.Invoke(_run.app.ShowMain)
    else:
        t = threading.Thread(target = _run, args = (dev, True))
        t.daemon = True
        t.start()
