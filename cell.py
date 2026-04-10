from tkinter import Tk, BOTH, Canvas
from line import Line, Point

class Cell():
	def __init__(self, win=None, grid=None):
		self.coords = None
		self.north = None
		self.south = None
		self.east = None
		self.west = None
		self.x1 = None
		self.y1 = None
		self.x2 = None
		self.y2 = None
		self.food = False
		self._win = win
		self._grid = grid

	def draw(self, direction):
		if self._win is None:
			return
		match direction:
			case "north":
				self._win.draw_line(Line(Point(self.x1, self.y1), Point(self.x2, self.y1)))
			case "south":
				self._win.draw_line(Line(Point(self.x1, self.y2), Point(self.x2, self.y2)))
			case "east":
				self._win.draw_line(Line(Point(self.x2, self.y1), Point(self.x2, self.y2)))
			case "west":
				self._win.draw_line(Line(Point(self.x1, self.y1), Point(self.x1, self.y2)))
