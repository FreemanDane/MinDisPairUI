import mainFrame
import wx

app = wx.App()
frame = mainFrame.mainFrame(None, "main")
frame.Show()

app.MainLoop()