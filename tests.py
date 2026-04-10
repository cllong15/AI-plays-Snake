import unittest
from unittest.mock import Mock
import sys
import os

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from line import Point, Line
from cell import Cell
from grid import Grid
from window import Window


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

        cell.draw("north")

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

        cell.draw("south")

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

        cell.draw("east")

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

        cell.draw("west")

        self.mock_win.draw_line.assert_called_once()
        line_arg = self.mock_win.draw_line.call_args[0][0]
        self.assertEqual(line_arg.p1.x, 0)
        self.assertEqual(line_arg.p1.y, 0)
        self.assertEqual(line_arg.p2.x, 0)
        self.assertEqual(line_arg.p2.y, 10)

    def test_draw_invalid_direction(self):
        """Test drawing with invalid direction does nothing"""
        cell = Cell(self.mock_win)
        cell.draw("invalid")

        self.mock_win.draw_line.assert_not_called()

    def test_draw_no_win(self):
        """Test that draw does nothing when win is None"""
        cell = Cell()
        cell.draw("north")

        # Should not raise an exception


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

    def test_grid_initialization_with_seed(self):
        """Test Grid initialization with seed"""
        grid = Grid(0, 0, 2, 2, 10, 10, seed=42)
        # Just verify it doesn't crash
        self.assertEqual(len(grid._cells), 2)
        self.assertEqual(len(grid._cells[0]), 2)

    def test_create_cells_structure(self):
        """Test that _create_cells creates correct 2D structure"""
        grid = Grid(0, 0, 3, 4, 10, 10)

        self.assertEqual(len(grid._cells), 4)  # num_cols
        for col in grid._cells:
            self.assertEqual(len(col), 3)  # num_rows

        # Check that all cells are Cell instances
        for col in grid._cells:
            for cell in col:
                self.assertIsInstance(cell, Cell)

    def test_cell_coordinates_assignment(self):
        """Test that cells get correct coordinates assigned"""
        grid = Grid(0, 0, 2, 3, 10, 10)

        # Check coordinates for each cell
        for i in range(3):  # cols
            for j in range(2):  # rows
                cell = grid._cells[i][j]
                self.assertEqual(cell.coords, [i, j])

    def test_cell_position_calculation(self):
        """Test that cell positions are calculated correctly"""
        grid = Grid(5, 5, 2, 2, 15, 20)

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
        grid = Grid(0, 0, 3, 3, 10, 10)

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

    def test_draw_cell_no_win(self):
        """Test that _draw_cell does nothing when win is None"""
        grid = Grid(0, 0, 2, 2, 10, 10)

        # Should not raise an exception
        grid._draw_cell(0, 0)

    def test_draw_cell_with_win(self):
        """Test that _draw_cell calls draw on appropriate walls"""
        grid = Grid(0, 0, 3, 3, 10, 10, self.mock_win)

        # Reset mock to clear calls from grid initialization
        self.mock_win.reset_mock()

        # Top-left corner (0,0) - should draw north and west
        grid._draw_cell(0, 0)
        self.assertEqual(self.mock_win.draw_line.call_count, 2)

        # Reset mock
        self.mock_win.reset_mock()

        # Bottom-right corner (2,2) - should draw south and east
        grid._draw_cell(2, 2)
        self.assertEqual(self.mock_win.draw_line.call_count, 2)


class TestWindow(unittest.TestCase):
    """Test cases for the Window class"""

    def test_window_initialization(self):
        """Test Window initialization"""
        # Note: Testing GUI components is tricky, so we'll just test basic setup
        window = Window(400, 300)

        # We can't easily test Tkinter components without a display
        # But we can verify the object was created
        self.assertIsNotNone(window)

    def test_window_initialization_default_size(self):
        """Test Window initialization with default size"""
        window = Window()
        self.assertIsNotNone(window)


if __name__ == '__main__':
    unittest.main()