from tkinter import BOTH, Canvas

from constants import *
from grid import Grid

class Window:
	def __init__(self, root, width=625, height=625):
		self._root = root
		self._root.title("Snek")
		self._canvas = Canvas(self._root, bg="black", width=width, height=height)
		self._canvas.pack(fill=BOTH, expand=1)
		self.grid = Grid(MARGIN, MARGIN, NUM_CELL, NUM_CELL, CELL_SIZE_X, CELL_SIZE_Y, self)
		self.start_game()

	def draw_line(self, line, fill_color="white"):
		line.draw(self._canvas, fill_color)

	def draw_cell(self, cell, fill_color="white"):
		cell.draw(self._canvas, fill_color)
	
	def start_game(self):
		self.grid.snake.draw()