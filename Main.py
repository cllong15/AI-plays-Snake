from tkinter import Tk, BOTH, Canvas
from window import Window
from grid import Grid

def main():
	num_rows = 20
	num_cols = 20
	margin = 10
	screen_x = 550
	screen_y = 550
	cell_size_x = (screen_x - 2 * margin) / num_cols
	cell_size_y = (screen_y - 2 * margin) / num_rows
	win = Window(screen_x, screen_y)

	maze = Grid(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

	win.mainloop()


if __name__ == "__main__":
	main()