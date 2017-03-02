#coding=utf-8
import point
import wx

class randomPointFrame(wx.Frame):
	def __init__(self, parent, title):
		super(randomPointFrame, self).__init__(parent, title = title, size = (200, 200))
		bkg = wx.Panel(self)
		self.NumberEdit = wx.TextCtrl(bkg)
		self.OkButton = wx.Button(bkg, label = 'Ok')
		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.NumberEdit, 0, flag = wx.EXPAND | wx.ALL, border = 5)
		vbox.Add(self.OkButton, 1, flag = wx.EXPAND | wx.ALL, border = 5)
		bkg.SetSizer(vbox)