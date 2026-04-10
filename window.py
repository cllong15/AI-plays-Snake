from tkinter import Tk, BOTH, Canvas

class Window:
	def __init__(self, width=625, height=625):
		self.__root = Tk()
		self.__root.title("Snek")
		self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
		self.__canvas.pack(fill=BOTH, expand=1)

	def mainloop(self):
		self.__root.mainloop()

	def draw_line(self, line, fill_color="black"):
		line.draw(self.__canvas, fill_color)
