import random

direction_opposites = {
	"north": "south",
	"south": "north",
	"west": "east",
	"east": "west"
}

class Snake:
	def __init__(self, center, win):
		self.body = [center]  # List of Cell objects
		self.direction = "east"  # Initial direction: moving right
		self.grow = False  # Flag to indicate whether the snake should grow on the next move
		self._win = win

	def move(self):
		head_x, head_y = self.body[0].coords
		if self.direction == "north":
			new_coords = (head_x, head_y - 1)
		elif self.direction == "south":
			new_coords = (head_x, head_y + 1)
		elif self.direction == "west":
			new_coords = (head_x - 1, head_y)
		elif self.direction == "east":
			new_coords = (head_x + 1, head_y)
		
		# Find the new head cell from the grid
		new_head_cell = self._win.grid._cells[new_coords[0]][new_coords[1]]
		
		self.body.insert(0, new_head_cell)  # Add new head to the beginning of the body
		if not self.grow:
			self.body.pop()  # Remove the last segment of the body
		else:
			self.grow = False  # Reset grow flag after using it

	def change_direction(self, new_direction):
		# Prevent the snake from reversing onto itself
		if new_direction != direction_opposites[self.direction]:
			self.direction = new_direction

	def draw(self, fill_color="green"):
		for cell in self.body:
			self._win.draw_cell(cell, fill_color)
	