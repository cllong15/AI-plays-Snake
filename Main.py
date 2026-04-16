import random
from tkinter import Tk
from window import Window
from constants import constants


def main():
    if constants.NUM_CELL % 2 == 0:
        raise ValueError("NUM_CELL must be odd to have a center cell.")

    root = Tk()

    win = Window(root, constants.SCREEN_SIDE, constants.SCREEN_SIDE)

    while constants.exit is False:
        try:
            if not root.winfo_exists():
                break
        except Tk.tclerror:
            break  # Window has been destroyed
        win.grid.snake.change_direction(
            random.choice(["north", "south", "east", "west"])
        )  # Example: change direction to east
        win.grid.snake.move()
        win.update()


# main()
if __name__ == "__main__":
	main()
