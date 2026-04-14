from tkinter import Tk, BOTH, Canvas
from cell import Cell
from snake import Snake
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
			win
	):
		self._cells = []
		self._x1 = x1
		self._y1 = y1
		self._num_rows = num_rows
		self._num_cols = num_cols
		self._cell_size_x = cell_size_x
		self._cell_size_y = cell_size_y
		self._win = win
		self._center = None

		self._create_cells()
		self.snake = Snake(self._center, self._win)
		self.food = None
		self.make_food()

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
				self._draw_borders(i, j)
		self._center = self._cells[(self._num_cols - 1) // 2][(self._num_rows - 1) // 2]

	def _draw_borders(self, i , j):
		if self._win is None:
			return
		if i == 0:
			self._cells[i][j].draw_borders("west")
		if i == self._num_cols - 1:
			self._cells[i][j].draw_borders("east")
		if j == 0:
			self._cells[i][j].draw_borders("north")
		if j == self._num_rows - 1:
			self._cells[i][j].draw_borders("south")

	def make_food(self):
		empty_cells = [cell for col in self._cells for cell in col if not cell.food and cell not in self.snake.body]
		if not empty_cells:
			return None
		food_cell = random.choice(empty_cells)
		self.food = food_cell
		food_cell.food = True
		if self._win is not None:
			self._win.draw_cell(food_cell, "red")