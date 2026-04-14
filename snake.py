from constants import *

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
		self._win = win

	def move(self):
		head_x, head_y = self.body[0].coords
		if self.direction == "north":
			new_coords = (head_x, head_y - 1)
			if new_coords[1] < 0:  # Check for collision with top wall
				constants.exit = True
				return
		elif self.direction == "south":
			new_coords = (head_x, head_y + 1)
			if new_coords[1] >= self._win.grid._num_rows:  # Check for collision with bottom wall
				constants.exit = True
				return
		elif self.direction == "west":
			new_coords = (head_x - 1, head_y)
			if new_coords[0] < 0:  # Check for collision with left wall
				constants.exit = True
				return
		elif self.direction == "east":
			new_coords = (head_x + 1, head_y)
			if new_coords[0] >= self._win.grid._num_cols:  # Check for collision with right wall
				constants.exit = True
				return
		# Find the new head cell from the grid
		new_head_cell = self._win.grid._cells[new_coords[0]][new_coords[1]]
		
		self.body.insert(0, new_head_cell)  # Add new head to the beginning of the body

		if not new_head_cell.food:
			old = self.body.pop()  # Remove the last segment of the body
			self._win.draw_cell(old, "black")  # Clear the old tail cell
		else:
			self._win.grid.food = None  # Remove the food from the grid
			self._win.grid.make_food()  # Create new food
		
		if self.collision():
			constants.exit = True  # End the game if there's a collision
		
		self.draw()  # Redraw the snake in its new position

	def change_direction(self, new_direction):
		# Prevent the snake from reversing onto itself
		if new_direction != direction_opposites[self.direction]:
			self.direction = new_direction

	def draw(self, fill_color="green"):
		for cell in self.body:
			self._win.draw_cell(cell, fill_color)
		
	def collision(self):
		head = self.body[0]
		# Check for collision with walls
		if 0 > head.coords[0] >= self._win.grid._num_cols or 0 > head.coords[1] >= self._win.grid._num_rows:
			constants.exit = True
			return True
		# Check for collision with itself
		if head in self.body[1:]:
			constants.exit = True
			return True
		return False
	