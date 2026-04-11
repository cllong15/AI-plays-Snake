from tkinter import Tk
from window import Window
from constants import *

def main():
	if NUM_CELL % 2 == 0:
		raise ValueError("NUM_CELL must be odd to have a center cell.")

	root = Tk()

	win = Window(root, SCREEN_SIDE, SCREEN_SIDE)

	root.mainloop()


if __name__ == "__main__":
	main()