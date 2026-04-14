import time
from tkinter import BOTH, Canvas

from constants import *
from grid import Grid

class Window:
	def __init__(self,
			  root,
			  width=constants.SCREEN_SIDE,
			  height=constants.SCREEN_SIDE
			  ):
		self._root = root
		self._root.title("Snek")
		self._canvas = Canvas(self._root, bg="black", width=width, height=height)
		self._canvas.pack(fill=BOTH, expand=1)
		self.grid = Grid(
			constants.MARGIN,
			constants.MARGIN,
			constants.NUM_CELL,
			constants.NUM_CELL,
			constants.CELL_SIZE_X,
			constants.CELL_SIZE_Y,
			self
			)
		self.start_game()

	def draw_line(self, line, fill_color="white"):
		line.draw(self._canvas, fill_color)

	def draw_cell(self, cell, fill_color="white"):
		cell.draw(self._canvas, fill_color)
	
	def start_game(self):
		self.grid.snake.draw()

	def update(self):
		self._root.update_idletasks()
		self._root.update()
		time.sleep(0.15)
