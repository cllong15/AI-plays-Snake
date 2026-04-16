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

	def draw_borders(self, direction):
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
# Canvas.create_rectangle
	def draw(self, canvas, fill_color="white"):
		canvas.create_rectangle(
			self.x1,
			self.y1,
			self.x2,
			self.y2,
			fill=fill_color
			)
		
	def next_cell(self, direction):
		match direction:
			case "north" | "no":
				return self.north
			case "south" | "so":
				return self.south
			case "east" | "ea":
				return self.east
			case "west" | "we":
				return self.west
			case "northwest" | "nw":
				return self.north.west if self.north and self.north.west else None
			case "northeast" | "ne":
				return self.north.east if self.north and self.north.east else None
			case "southwest" | "sw":
				return self.south.west if self.south and self.south.west else None
			case "southeast" | "se":
				return self.south.east if self.south and self.south.east else None
			case _:
				raise ValueError(f"Invalid direction: {direction}")
		
	def __repr__(self):
		return f"Cell({self.coords})"