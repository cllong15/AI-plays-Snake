from tkinter import Tk, BOTH, Canvas
from window import Window
from grid import Grid
from constants import *

def main():
	if SIDE % 2 == 0:
		raise ValueError("Side length must be odd to have a center cell.")
	win = Window(SCREEN_SIDE, SCREEN_SIDE)

	maze = Grid(MARGIN, MARGIN, SIDE, SIDE, CELL_SIZE_X, CELL_SIZE_Y, win)

	win.mainloop()


if __name__ == "__main__":
	main()