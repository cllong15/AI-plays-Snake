from tkinter import Tk, BOTH, Canvas
from cell import Cell
import random
import time

class Grid:
	def __init__(
			self,
			x1,
			y1,
			num_rows,
			num_cols,
			cell_size_x,
			cell_size_y,
			win=None,
			seed=None
	):
		self._cells = []
		self._x1 = x1
		self._y1 = y1
		self._num_rows = num_rows
		self._num_cols = num_cols
		self._cell_size_x = cell_size_x
		self._cell_size_y = cell_size_y
		self._win = win
		if seed:
			random.seed(seed)

		self._create_cells()

	def _create_cells(self):
		for i in range(self._num_cols):
			col_cells = []
			for j in range(self._num_rows):
				col_cells.append(Cell(self._win, self))
			self._cells.append(col_cells)
		for i in range(self._num_cols):
			for j in range(self._num_rows):
				self._cells[i][j].coords = [i, j]
				self._cells[i][j].x1 = self._x1 + i * self._cell_size_x
				self._cells[i][j].y1 = self._y1 + j * self._cell_size_y
				self._cells[i][j].x2 = self._cells[i][j].x1 + self._cell_size_x
				self._cells[i][j].y2 = self._cells[i][j].y1 + self._cell_size_y
				if i > 0:
					self._cells[i][j].west = self._cells[i - 1][j]
				if i < self._num_cols - 1:
					self._cells[i][j].east = self._cells[i + 1][j]
				if j > 0:
					self._cells[i][j].north = self._cells[i][j - 1]
				if j < self._num_rows - 1:
					self._cells[i][j].south = self._cells[i][j + 1]
				self._draw_cell(i, j)

	def _draw_cell(self, i , j):
		if self._win is None:
			return
		if i == 0:
			self._cells[i][j].draw("west")
		if i == self._num_cols - 1:
			self._cells[i][j].draw("east")
		if j == 0:
			self._cells[i][j].draw("north")
		if j == self._num_rows - 1:
			self._cells[i][j].draw("south")
		
