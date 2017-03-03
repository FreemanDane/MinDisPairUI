#coding=utf-8
import wx
from randomPointFrame import randomPointFrame
from point import point
import random
import time
import platform

MAX_NUM = 2 ** 32

class mainFrame(wx.Frame):
	def __init__(self, parent, title):
		super(mainFrame, self).__init__(parent, title = title, size = (800, 600))
		self.InitUI()
		self.SetBackgroundColour("White")
		self.points = []

	def InitUI(self):
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Show(True)
		self.menuBar = wx.MenuBar()
		self.pointMenu = wx.Menu()
		self.clearItem = wx.MenuItem(self.pointMenu, 101, text = "&clear\tCtrl+C", kind = wx.ITEM_NORMAL)
		self.randomItem = wx.MenuItem(self.pointMenu, 102, text = "&random\tCtrl+R", kind = wx.ITEM_NORMAL)
		self.computeItem = wx.MenuItem(self.pointMenu, 103, text = "compute", kind = wx.ITEM_NORMAL)
		self.pointMenu.AppendItem(self.clearItem)
		self.pointMenu.AppendItem(self.randomItem)
		self.pointMenu.AppendItem(self.computeItem)
		self.randomFrame = randomPointFrame(self, "please input")
		self.menuBar.Append(self.pointMenu, "Point")
		self.SetMenuBar(self.menuBar)
		self.Bind(wx.EVT_MENU, self.MenuHandler)
		self.Bind(wx.EVT_LEFT_DOWN, self.AddPoint)
		self.Bind(wx.EVT_RIGHT_DOWN, self.DeletePoint)
		self.randomFrame.Show(False)
		self.randomFrame.OkButton.Bind(wx.EVT_BUTTON, self.RandomPoint)

	def OnPaint(self, e):
		self.DrawPoint()

	def DrawPoint(self):
		sysstr = platform.system()
		dc = None
		if sysstr == "Linux":
			dc = wx.PaintDC(self)
		elif sysstr == "Windows":
			dc = wx.ClientDC(self)
		brush = wx.Brush("White")
		dc.SetBackground(brush)
		dc.Clear()

		color = wx.Colour(0, 0, 0)
		b = wx.Brush(color)
		dc.SetBrush(b)
		for p in self.points:
			dc.DrawCircle(p.x, p.y, 2)

	def MenuHandler(self, e):
		ID = e.GetId()
		if ID == 101:
			while len(self.points) != 0:
				self.points.pop()
			self.DrawPoint()
		elif ID == 102:
			self.randomFrame.Show(True)
		else:
			result = self.FindMinDis()

	def AddPoint(self, e):
		x, y = e.GetPositionTuple()
		p = point(x, y)
		self.points.append(p)
		self.DrawPoint()

	def DeletePoint(self, e):
		x, y = e.GetPositionTuple()
		p = point(x, y)
		for pt in self.points:
			if (pt.dis(p) < 5):
				self.points.remove(pt)
		self.DrawPoint()
	def RandomPoint(self, e):
		pts = []
		num = int(self.randomFrame.NumberEdit.GetValue())
		for i in range(0, num):
			pts.append(point(random.randint(0, MAX_NUM - 1), random.randint(0, MAX_NUM - 1)))
		t1 = time.clock()
		self.ClosestPair(pts)
		t2 = time.clock()
		self.CommonMinDis(pts)
		t3 = time.clock()
		print "When the num of points up to", num
		print "Common method cost", t3 - t2, "s"
		print "Divide and Conquer method cost", t2 - t1, "s"

	def CommonMinDis(self, pts):
		dr = MAX_NUM - 1
		pr = None
		l = len(pts)
		for i in range(0, l):
			for j in range(i + 1, l):
				if pts[i].dis(pts[j]) < dr:
					dr = pts[i].dis(pts[j])
					pr = (pts[i], pts[j])
		return (dr, pr)

	def Merge(self, t, list1, list2):
		result = []
		list1.append(point(MAX_NUM, MAX_NUM))
		list2.append(point(MAX_NUM, MAX_NUM))
		i = 0
		j = 0
		if t is 0:
			while list1[i].x < MAX_NUM or list2[j].x < MAX_NUM:
				if list1[i].x < list2[j].x:
					result.append(list1[i])
					i += 1
				else:
					result.append(list2[j])
					j += 1
		else:
			while list1[i].y < MAX_NUM or list2[j].y < MAX_NUM:
				if list1[i].y < list2[j].y:
					result.append(list1[i])
					i += 1
				else:
					result.append(list2[j])
					j += 1
		return result
				

	def MergeSort(self, t, l):
		list1 = []
		list2 = []
		length = len(l)
		if length < 5:
			return self.InsertSort(t, l)
		for i in range(0, length / 2):
			list1.append(l[i])
		for i in range(length / 2, length):
			list2.append(l[i])
		list1 = self.MergeSort(t, list1)
		list2 = self.MergeSort(t, list2)
		return self.Merge(t, list1, list2)

	def InsertSort(self, t, l):
		minPoint = point(-MAX_NUM, -MAX_NUM)
		maxPoint = point(MAX_NUM, MAX_NUM)
		result = [minPoint, maxPoint]
		for p in l:
			length = len(result)
			for i in range(1, length):
				if t is 0:
					if result[i - 1].x <= p.x and result[i].x > p.x:
						result.insert(i, p)
						break
				else:
					if result[i - 1].y <= p.y and result[i].y > p.y:
						result.insert(i, p)
						break
		result.remove(minPoint)
		result.remove(maxPoint)
		return result
	def ClosestPair(self, l):
		sortX = self.MergeSort(0, l)
		sortY = self.MergeSort(1, l)
		return self.ClosestPairRec(sortX, sortY)

	def ClosestPairRec(self, sortX, sortY):
		length = len(sortX)
		if (length < 5):
			return self.CommonMinDis(sortX)
		middle = length / 2
		mid = sortX[middle]
		leftSortY = []
		rightSortY = []
		for p in sortY:
			if p.x < mid.x:
				leftSortY.append(p)
			else:
				rightSortY.append(p)
		leftSortX = []
		rightSortX = []
		for i in range(0, middle):
			leftSortX.append(sortX[i])
		for i in range(middle, length):
			rightSortX.append(sortX[i])
		leftResult = self.ClosestPairRec(leftSortX, leftSortY)
		rightResult = self.ClosestPairRec(rightSortX, rightSortY)
		minDis = MAX_NUM
		if leftResult[0] < rightResult[0]:
			minDis = leftResult
		else:
			minDis = rightResult
		s = []
		for p in sortY:
			if abs(p.x - mid.x) <= minDis[0]:
				s.append(p)
		length = len(s)
		for i in range(0, length):
			for j in range(i + 1, i + 8):
				if j == length:
					break
				if s[i].dis(s[j]) < minDis[0]:
					minDis = (s[i].dis(s[j]),(s[i], s[j]))
		return minDis
	def FindMinDis(self):
		r = self.ClosestPair(self.points)
		self.ShowMinDis(r)

	def ShowMinDis(self, result):
		sysstr = platform.system()
		dc = None
		if sysstr == "Linux":
			dc = wx.PaintDC(self)
		elif sysstr == "Windows":
			dc = wx.ClientDC(self)
		brush = wx.Brush("White")
		dc.SetBackground(brush)
		dc.Clear()
		color = wx.Colour(0, 0, 0)
		b = wx.Brush(color)
		dc.SetBrush(b)
		for p in self.points:
			if p not in result[1]:
				dc.DrawCircle(p.x, p.y, 2)
		color = wx.Colour(255, 0, 0)
		rb = wx.Brush(color)
		dc.SetBrush(rb)
		for p in result[1]:
			dc.DrawCircle(p.x, p.y, 2)
		dc.DrawLine(result[1][0].x, result[1][0].y, result[1][1].x, result[1][1].y)
		font = wx.Font(18, wx.ROMAN, wx.ITALIC, wx.NORMAL)
		dc.SetFont(font)
		dc.DrawText(str(result[0]), 0, 0)