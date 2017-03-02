import math

class point:
	def __init__(self, a = 0, b = 0):
		self.x = a
		self.y = b

	def show(self):
		print self.x,',',self.y
		
	def dis(self, other):
		return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)