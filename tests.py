import unittest
from unittest.mock import Mock, patch
import sys
import os
from tkinter import Tk

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from line import Point, Line
from cell import Cell
from grid import Grid
from window import Window
from snake import Snake
from constants import constants


class TestPoint(unittest.TestCase):
	"""Test cases for the Point class"""

	def test_point_creation(self):
		"""Test that Point objects are created with correct coordinates"""
		p = Point(10, 20)
		self.assertEqual(p.x, 10)
		self.assertEqual(p.y, 20)

	def test_point_attributes(self):
		"""Test that Point attributes can be accessed and modified"""
		p = Point(0, 0)
		p.x = 5
		p.y = 15
		self.assertEqual(p.x, 5)
		self.assertEqual(p.y, 15)


class TestLine(unittest.TestCase):
	"""Test cases for the Line class"""

	def test_line_creation(self):
		"""Test that Line objects are created with correct points"""
		p1 = Point(0, 0)
		p2 = Point(10, 10)
		line = Line(p1, p2)
		self.assertEqual(line.p1, p1)
		self.assertEqual(line.p2, p2)

	def test_line_draw(self):
		"""Test that Line.draw calls canvas.create_line with correct parameters"""
		p1 = Point(0, 0)
		p2 = Point(10, 10)
		line = Line(p1, p2)

		mock_canvas = Mock()
		line.draw(mock_canvas)

		mock_canvas.create_line.assert_called_once_with(
			0, 0, 10, 10, fill="black", width=2
		)

	def test_line_draw_custom_color(self):
		"""Test that Line.draw uses custom fill color"""
		p1 = Point(0, 0)
		p2 = Point(10, 10)
		line = Line(p1, p2)

		mock_canvas = Mock()
		line.draw(mock_canvas, fill_color="red")

		mock_canvas.create_line.assert_called_once_with(
			0, 0, 10, 10, fill="red", width=2
		)


class TestCell(unittest.TestCase):
	"""Test cases for the Cell class"""

	def setUp(self):
		"""Set up test fixtures"""
		self.mock_win = Mock()
		self.mock_grid = Mock()

	def test_cell_initialization(self):
		"""Test that Cell is initialized with correct default values"""
		cell = Cell(self.mock_win, self.mock_grid)

		self.assertIsNone(cell.coords)
		self.assertIsNone(cell.north)
		self.assertIsNone(cell.south)
		self.assertIsNone(cell.east)
		self.assertIsNone(cell.west)
		self.assertIsNone(cell.x1)
		self.assertIsNone(cell.y1)
		self.assertIsNone(cell.x2)
		self.assertIsNone(cell.y2)
		self.assertFalse(cell.food)
		self.assertEqual(cell._win, self.mock_win)
		self.assertEqual(cell._grid, self.mock_grid)

	def test_cell_initialization_no_win_grid(self):
		"""Test Cell initialization without win and grid"""
		cell = Cell()

		self.assertIsNone(cell._win)
		self.assertIsNone(cell._grid)

	def test_draw_north(self):
		"""Test drawing north wall"""
		cell = Cell(self.mock_win)
		cell.x1 = 0
		cell.y1 = 0
		cell.x2 = 10
		cell.y2 = 10

		cell.draw_borders("north")

		# Verify that win.draw_line was called with correct Line
		self.mock_win.draw_line.assert_called_once()
		line_arg = self.mock_win.draw_line.call_args[0][0]
		self.assertEqual(line_arg.p1.x, 0)
		self.assertEqual(line_arg.p1.y, 0)
		self.assertEqual(line_arg.p2.x, 10)
		self.assertEqual(line_arg.p2.y, 0)

	def test_draw_south(self):
		"""Test drawing south wall"""
		cell = Cell(self.mock_win)
		cell.x1 = 0
		cell.y1 = 0
		cell.x2 = 10
		cell.y2 = 10

		cell.draw_borders("south")

		self.mock_win.draw_line.assert_called_once()
		line_arg = self.mock_win.draw_line.call_args[0][0]
		self.assertEqual(line_arg.p1.x, 0)
		self.assertEqual(line_arg.p1.y, 10)
		self.assertEqual(line_arg.p2.x, 10)
		self.assertEqual(line_arg.p2.y, 10)

	def test_draw_east(self):
		"""Test drawing east wall"""
		cell = Cell(self.mock_win)
		cell.x1 = 0
		cell.y1 = 0
		cell.x2 = 10
		cell.y2 = 10

		cell.draw_borders("east")

		self.mock_win.draw_line.assert_called_once()
		line_arg = self.mock_win.draw_line.call_args[0][0]
		self.assertEqual(line_arg.p1.x, 10)
		self.assertEqual(line_arg.p1.y, 0)
		self.assertEqual(line_arg.p2.x, 10)
		self.assertEqual(line_arg.p2.y, 10)

	def test_draw_west(self):
		"""Test drawing west wall"""
		cell = Cell(self.mock_win)
		cell.x1 = 0
		cell.y1 = 0
		cell.x2 = 10
		cell.y2 = 10

		cell.draw_borders("west")

		self.mock_win.draw_line.assert_called_once()
		line_arg = self.mock_win.draw_line.call_args[0][0]
		self.assertEqual(line_arg.p1.x, 0)
		self.assertEqual(line_arg.p1.y, 0)
		self.assertEqual(line_arg.p2.x, 0)
		self.assertEqual(line_arg.p2.y, 10)

	def test_draw_invalid_direction(self):
		"""Test drawing with invalid direction does nothing"""
		cell = Cell(self.mock_win)
		cell.draw_borders("invalid")

		self.mock_win.draw_line.assert_not_called()

	def test_draw_no_win(self):
		"""Test that draw_borders does nothing when win is None"""
		cell = Cell()
		cell.x1 = 0
		cell.y1 = 0
		cell.x2 = 10
		cell.y2 = 10
	
		self.assertIsNone(cell.draw_borders("north"))
	
class TestGrid(unittest.TestCase):
	"""Test cases for the Grid class"""

	def setUp(self):
		"""Set up test fixtures"""
		self.mock_win = Mock()

	def test_grid_initialization(self):
		"""Test Grid initialization with basic parameters"""
		grid = Grid(10, 10, 5, 5, 20, 20, self.mock_win)

		self.assertEqual(grid._x1, 10)
		self.assertEqual(grid._y1, 10)
		self.assertEqual(grid._num_rows, 5)
		self.assertEqual(grid._num_cols, 5)
		self.assertEqual(grid._cell_size_x, 20)
		self.assertEqual(grid._cell_size_y, 20)
		self.assertEqual(grid._win, self.mock_win)
		self.assertIsInstance(grid._cells, list)

	def test_create_cells_structure(self):
		"""Test that _create_cells creates correct 2D structure"""
		grid = Grid(0, 0, 3, 4, 10, 10, self.mock_win)

		self.assertEqual(len(grid._cells), 4)  # num_cols
		for col in grid._cells:
			self.assertEqual(len(col), 3)  # num_rows

		# Check that all cells are Cell instances
		for col in grid._cells:
			for cell in col:
				self.assertIsInstance(cell, Cell)

	def test_cell_coordinates_assignment(self):
		"""Test that cells get correct coordinates assigned"""
		grid = Grid(0, 0, 2, 3, 10, 10, self.mock_win)

		# Check coordinates for each cell
		for i in range(3):	# cols
			for j in range(2):	# rows
				cell = grid._cells[i][j]
				self.assertEqual(cell.coords, [i, j])

	def test_cell_position_calculation(self):
		"""Test that cell positions are calculated correctly"""
		grid = Grid(5, 5, 2, 2, 15, 20, self.mock_win)

		# Cell at (0,0)
		cell_00 = grid._cells[0][0]
		self.assertEqual(cell_00.x1, 5)
		self.assertEqual(cell_00.y1, 5)
		self.assertEqual(cell_00.x2, 20)  # 5 + 15
		self.assertEqual(cell_00.y2, 25)  # 5 + 20

		# Cell at (1,1)
		cell_11 = grid._cells[1][1]
		self.assertEqual(cell_11.x1, 20)  # 5 + 1*15
		self.assertEqual(cell_11.y1, 25)  # 5 + 1*20
		self.assertEqual(cell_11.x2, 35)  # 20 + 15
		self.assertEqual(cell_11.y2, 45)  # 25 + 20

	def test_cell_neighbor_assignment(self):
		"""Test that cell neighbors are assigned correctly"""
		grid = Grid(0, 0, 3, 3, 10, 10, self.mock_win)

		# Test corner cells
		cell_00 = grid._cells[0][0]
		self.assertIsNone(cell_00.west)
		self.assertIsNone(cell_00.north)
		self.assertEqual(cell_00.east, grid._cells[1][0])
		self.assertEqual(cell_00.south, grid._cells[0][1])

		# Test center cell
		cell_11 = grid._cells[1][1]
		self.assertEqual(cell_11.west, grid._cells[0][1])
		self.assertEqual(cell_11.east, grid._cells[2][1])
		self.assertEqual(cell_11.north, grid._cells[1][0])
		self.assertEqual(cell_11.south, grid._cells[1][2])

		# Test bottom-right corner
		cell_22 = grid._cells[2][2]
		self.assertEqual(cell_22.west, grid._cells[1][2])
		self.assertEqual(cell_22.north, grid._cells[2][1])
		self.assertIsNone(cell_22.east)
		self.assertIsNone(cell_22.south)

	def test_grid_initialization_contains_snake(self):
		"""Test Grid initialization creates a centered Snake"""
		grid = Grid(0, 0, 3, 3, 10, 10, self.mock_win)

		expected_center_coords = [1, 1]	 # Center of 3x3 grid
		self.assertIsInstance(grid._center, Cell)
		self.assertIsNotNone(grid.snake)
		self.assertEqual(grid.snake.body[0].coords, expected_center_coords)
		self.assertEqual(grid._center.coords, expected_center_coords)

	def test_make_food_returns_none_when_no_empty_cells(self):
		"""Test that make_food returns None if there are no empty cells"""
		grid = Grid(0, 0, 2, 2, 10, 10, self.mock_win)

		self.assertIsNone(grid.make_food())

	def test_make_food_creates_food_on_empty_cell(self):
		"""Test that make_food places food on an empty cell"""
		grid = Grid(0, 0, 2, 2, 10, 10, self.mock_win)
		# All cells are empty except one in snake body
		grid.snake.body = [grid._cells[0][0]]  # Snake occupies one cell
		grid._cells[0][0].food = False	# Ensure it's not food
		grid._cells[0][1].food = False
		grid._cells[1][0].food = False
		grid._cells[1][1].food = False

		grid.make_food()
		# make_food doesn't return, it sets grid.food
		self.assertIsNotNone(grid.food)
		self.assertTrue(grid.food.food)
		# Check that exactly one cell has food
		food_cells = [cell for col in grid._cells for cell in col if cell.food]
		self.assertEqual(len(food_cells), 1)
		self.assertEqual(grid.food, food_cells[0])

	def test_grid_makes_food_on_init(self):
		"""Test that grid creates food during initialization"""
		grid = Grid(0, 0, 3, 3, 10, 10, self.mock_win)
		# Food should be created during init
		self.assertIsNotNone(grid.food)
		self.assertTrue(grid.food.food)
		# Verify draw_cell was called for food
		self.mock_win.draw_cell.assert_called_with(grid.food, "red")

class TestWindow(unittest.TestCase):
	"""Test cases for the Window class"""

	def test_window_initialization(self):
		"""Test Window initialization"""
		# Note: Testing GUI components is tricky, so we'll just test basic setup
		root = Tk()
		try:
			with patch('window.constants') as mock_constants:
				mock_constants.MARGIN = 10
				mock_constants.NUM_CELL = 11
				mock_constants.CELL_SIZE_X = 10
				mock_constants.CELL_SIZE_Y = 10
				mock_constants.SCREEN_SIDE = 550
				window = Window(root, 400, 300)
				self.assertIsNotNone(window)
				self.assertEqual(window._root, root)
		finally:
			root.destroy()

	def test_window_initialization_default_size(self):
		"""Test Window initialization with default size"""
		root = Tk()
		try:
			with patch('window.constants') as mock_constants:
				mock_constants.MARGIN = 10
				mock_constants.NUM_CELL = 11
				mock_constants.CELL_SIZE_X = 10
				mock_constants.CELL_SIZE_Y = 10
				mock_constants.SCREEN_SIDE = 550
				window = Window(root)
				self.assertIsNotNone(window)
		finally:
			root.destroy()

	def test_window_draw_cell(self):
		"""Test Window.draw_cell calls cell.draw with canvas and color"""
		root = Tk()
		try:
			with patch('window.constants') as mock_constants:
				mock_constants.MARGIN = 10
				mock_constants.NUM_CELL = 11
				mock_constants.CELL_SIZE_X = 10
				mock_constants.CELL_SIZE_Y = 10
				mock_constants.SCREEN_SIDE = 550
				with patch.object(Window, 'start_game'):
					window = Window(root)
					mock_cell = Mock()
					window.draw_cell(mock_cell, "red")
					mock_cell.draw.assert_called_once_with(window._canvas, "red")
		finally:
			root.destroy()


class TestSnake(unittest.TestCase):
	"""Test cases for the Snake class"""

	def _create_mock_cell(self, coords):
		"""Helper to create a mock cell with coords"""
		cell = Mock()
		cell.coords = coords
		return cell

	def test_snake_initialization(self):
		"""Test that Snake is initialized with correct default values"""
		mock_win = Mock()
		center_cell = self._create_mock_cell([5, 5])
		snake = Snake(center_cell, mock_win)

		self.assertEqual(snake.body, [center_cell])
		self.assertEqual(snake.direction, "east")
		self.assertEqual(snake._win, mock_win)

	def test_move_east(self):
		"""Test moving snake east (default direction)"""
		mock_win = Mock()
		mock_grid = Mock()
		mock_win.grid = mock_grid
		# Create mock cells for positions (5,5) and (6,5)
		start_cell = self._create_mock_cell([5, 5])
		end_cell = self._create_mock_cell([6, 5])
		start_cell.food = False
		end_cell.food = False
		# Mock a larger grid
		mock_grid._cells = [[None] * 10 for _ in range(10)]
		mock_grid._num_cols = 10
		mock_grid._num_rows = 10
		mock_grid._cells[5][5] = start_cell
		mock_grid._cells[6][5] = end_cell
		
		snake = Snake(start_cell, mock_win)
		snake.move()

		expected_body = [end_cell]	# Moved right by 1
		self.assertEqual(snake.body, expected_body)
		self.assertEqual(len(snake.body), 1)  # Should not grow by default
		# Verify draw_cell was called to clear old tail and draw new snake
		self.assertTrue(mock_win.draw_cell.called)

	def test_move_west(self):
		"""Test moving snake west"""
		mock_win = Mock()
		mock_grid = Mock()
		mock_win.grid = mock_grid
		# Create mock cells for positions (5,5) and (4,5)
		start_cell = self._create_mock_cell([5, 5])
		end_cell = self._create_mock_cell([4, 5])
		start_cell.food = False
		end_cell.food = False
		mock_grid._cells = [[None] * 10 for _ in range(10)]
		mock_grid._num_cols = 10
		mock_grid._num_rows = 10
		mock_grid._cells[5][5] = start_cell
		mock_grid._cells[4][5] = end_cell
		
		snake = Snake(start_cell, mock_win)
		snake.direction = "west"
		snake.move()

		expected_body = [end_cell]	# Moved left by 1
		self.assertEqual(snake.body, expected_body)

	def test_move_north(self):
		"""Test moving snake north"""
		mock_win = Mock()
		mock_grid = Mock()
		mock_win.grid = mock_grid
		# Create mock cells for positions (5,5) and (5,4)
		start_cell = self._create_mock_cell([5, 5])
		end_cell = self._create_mock_cell([5, 4])
		start_cell.food = False
		end_cell.food = False
		mock_grid._cells = [[None] * 10 for _ in range(10)]
		mock_grid._num_cols = 10
		mock_grid._num_rows = 10
		mock_grid._cells[5][5] = start_cell
		mock_grid._cells[5][4] = end_cell
		
		snake = Snake(start_cell, mock_win)
		snake.direction = "north"
		snake.move()

		expected_body = [end_cell]	# Moved up by 1
		self.assertEqual(snake.body, expected_body)

	def test_move_south(self):
		"""Test moving snake south"""
		mock_win = Mock()
		mock_grid = Mock()
		mock_win.grid = mock_grid
		# Create mock cells for positions (5,5) and (5,6)
		start_cell = self._create_mock_cell([5, 5])
		end_cell = self._create_mock_cell([5, 6])
		start_cell.food = False
		end_cell.food = False
		mock_grid._cells = [[None] * 10 for _ in range(10)]
		mock_grid._num_cols = 10
		mock_grid._num_rows = 10
		mock_grid._cells[5][5] = start_cell
		mock_grid._cells[5][6] = end_cell
		
		snake = Snake(start_cell, mock_win)
		snake.direction = "south"
		snake.move()

		expected_body = [end_cell]	# Moved down by 1
		self.assertEqual(snake.body, expected_body)

	def test_move_with_multiple_segments(self):
		"""Test moving snake with multiple body segments"""
		mock_win = Mock()
		mock_grid = Mock()
		mock_win.grid = mock_grid
		# Create mock cells for positions (5,5), (4,5), (3,5), (6,5)
		cell_55 = self._create_mock_cell([5, 5])
		cell_45 = self._create_mock_cell([4, 5])
		cell_35 = self._create_mock_cell([3, 5])
		cell_65 = self._create_mock_cell([6, 5])
		cell_55.food = False
		cell_45.food = False
		cell_35.food = False
		cell_65.food = False
		mock_grid._cells = [[None] * 10 for _ in range(10)]
		mock_grid._num_cols = 10
		mock_grid._num_rows = 10
		mock_grid._cells[6][5] = cell_65
		mock_grid._cells[5][5] = cell_55
		mock_grid._cells[4][5] = cell_45
		mock_grid._cells[3][5] = cell_35
		
		snake = Snake(cell_55, mock_win)
		# Manually add segments to simulate growth
		snake.body = [cell_55, cell_45, cell_35]
		snake.move()

		expected_body = [cell_65, cell_55, cell_45]	 # Head moves, tail follows
		self.assertEqual(snake.body, expected_body)

	def test_grow_when_food_eaten(self):
		"""Test that snake grows when food is eaten"""
		mock_win = Mock()
		mock_grid = Mock()
		mock_win.grid = mock_grid
		# Create mock cells for positions (5,5) and (6,5)
		start_cell = self._create_mock_cell([5, 5])
		end_cell = self._create_mock_cell([6, 5])
		start_cell.food = False
		end_cell.food = True  # Food on the new cell
		mock_grid._cells = [[None] * 10 for _ in range(10)]
		mock_grid._num_cols = 10
		mock_grid._num_rows = 10
		mock_grid._cells[5][5] = start_cell
		mock_grid._cells[6][5] = end_cell
		mock_grid.food = end_cell
		mock_grid.make_food = Mock()  # Mock make_food to avoid creating real food
		
		snake = Snake(start_cell, mock_win)
		snake.move()

		expected_body = [end_cell, start_cell]	# Head moves AND body grows
		self.assertEqual(snake.body, expected_body)
		# Verify food respawn was called
		mock_grid.make_food.assert_called_once()

	def test_grow_flag_false(self):
		"""Test that snake doesn't grow when no food"""
		mock_win = Mock()
		mock_grid = Mock()
		mock_win.grid = mock_grid
		# Create mock cells for positions (5,5) and (6,5)
		start_cell = self._create_mock_cell([5, 5])
		end_cell = self._create_mock_cell([6, 5])
		start_cell.food = False
		end_cell.food = False
		mock_grid._cells = [[None] * 10 for _ in range(10)]
		mock_grid._num_cols = 10
		mock_grid._num_rows = 10
		mock_grid._cells[5][5] = start_cell
		mock_grid._cells[6][5] = end_cell
		
		snake = Snake(start_cell, mock_win)
		snake.move()

		expected_body = [end_cell]	# Only head moves, no growth
		self.assertEqual(snake.body, expected_body)

	def test_change_direction_valid(self):
		"""Test changing direction to a valid new direction"""
		mock_win = Mock()
		center_cell = self._create_mock_cell([5, 5])
		snake = Snake(center_cell, mock_win)
		snake.direction = "east"

		snake.change_direction("north")
		self.assertEqual(snake.direction, "north")

		snake.change_direction("west")
		self.assertEqual(snake.direction, "west")

	def test_change_direction_all_opposites(self):
		"""Test preventing reversal in all directions"""
		test_cases = [
			("east", "west"),
			("west", "east"),
			("north", "south"),
			("south", "north")
		]

		for current_dir, opposite_dir in test_cases:
			with self.subTest(current=current_dir, opposite=opposite_dir):
				mock_win = Mock()
				center_cell = self._create_mock_cell([5, 5])
				snake = Snake(center_cell, mock_win)
				snake.direction = current_dir
				snake.change_direction(opposite_dir)
				self.assertEqual(snake.direction, current_dir,
							   f"Should not allow reversing from {current_dir} to {opposite_dir}")

	def test_change_direction_same_direction(self):
		"""Test changing to the same direction (should be allowed)"""
		mock_win = Mock()
		center_cell = self._create_mock_cell([5, 5])
		snake = Snake(center_cell, mock_win)
		snake.direction = "east"
		snake.change_direction("east")
		self.assertEqual(snake.direction, "east")

	def test_multiple_moves_with_growth(self):
		"""Test multiple moves with intermittent growth"""
		mock_win = Mock()
		mock_grid = Mock()
		mock_win.grid = mock_grid
		# Create mock cells for positions (5,5), (6,5), (7,5), (8,5)
		cell_55 = self._create_mock_cell([5, 5])
		cell_65 = self._create_mock_cell([6, 5])
		cell_75 = self._create_mock_cell([7, 5])
		cell_85 = self._create_mock_cell([8, 5])
		cell_55.food = False
		cell_65.food = False
		cell_75.food = True	 # Food on this cell
		cell_85.food = False
		mock_grid._cells = [[None] * 10 for _ in range(10)]
		mock_grid._num_cols = 10
		mock_grid._num_rows = 10
		mock_grid._cells[5][5] = cell_55
		mock_grid._cells[6][5] = cell_65
		mock_grid._cells[7][5] = cell_75
		mock_grid._cells[8][5] = cell_85
		mock_grid.food = cell_75
		mock_grid.make_food = Mock()  # Mock make_food
		
		snake = Snake(cell_55, mock_win)

		# Move 1: normal move
		snake.move()
		self.assertEqual(snake.body, [cell_65])

		# Move 2: with growth (food eaten)
		snake.move()
		self.assertEqual(snake.body, [cell_75, cell_65])
		# Verify make_food was called
		mock_grid.make_food.assert_called_once()

		# Move 3: normal move
		# Reset make_food mock for this move
		mock_grid.make_food.reset_mock()
		snake.move()
		self.assertEqual(snake.body, [cell_85, cell_75])
		# make_food should not be called this move
		mock_grid.make_food.assert_not_called()

	def test_draw_method(self):
		"""Test that draw method calls window.draw_cell for each body segment"""
		mock_win = Mock()
		# Mock the grid structure
		mock_grid = Mock()
		mock_win.grid = mock_grid
		mock_cell1 = Mock()
		mock_cell2 = Mock()
		mock_grid._cells = [[mock_cell1, mock_cell2], [mock_cell1, mock_cell2]]	 # Mock 2x2 grid structure
		
		center_cell = self._create_mock_cell([0, 0])
		snake = Snake(center_cell, mock_win)
		snake.body = [mock_cell1, mock_cell2]  # Cell objects

		snake.draw("green")

		# Should call draw_cell twice, once for each body segment
		self.assertEqual(mock_win.draw_cell.call_count, 2)
		mock_win.draw_cell.assert_any_call(mock_cell1, "green")
		mock_win.draw_cell.assert_any_call(mock_cell2, "green")

	def test_collision_with_self(self):
		"""Test that snake detects collision with its own body"""
		mock_win = Mock()
		mock_grid = Mock()
		mock_win.grid = mock_grid
		# Create mock cells: head at (5,5), body at (6,5), tail at (7,5)
		# Next move east would go to (6,5), which is occupied by body
		cell_55 = self._create_mock_cell([5, 5])  # head
		cell_65 = self._create_mock_cell([6, 5])  # body
		cell_75 = self._create_mock_cell([7, 5])  # tail
		cell_55.food = False
		cell_65.food = False
		cell_75.food = False
		mock_grid._cells = [[None] * 10 for _ in range(10)]
		mock_grid._num_cols = 10
		mock_grid._num_rows = 10
		mock_grid._cells[5][5] = cell_55
		mock_grid._cells[6][5] = cell_65
		mock_grid._cells[7][5] = cell_75
		
		snake = Snake(cell_55, mock_win)
		snake.body = [cell_55, cell_65, cell_75]  # Snake occupies these cells
		snake.direction = "east"  # Next move to (6,5), which is cell_65 in body
		
		# Move should detect collision
		snake.move()
		
		# Check that collision was detected (constants.exit should be True)
		self.assertTrue(constants.exit)


if __name__ == '__main__':
	unittest.main()