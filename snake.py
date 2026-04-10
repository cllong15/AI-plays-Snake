

direction_opposites = {
	"north": "south",
	"south": "north",
	"west": "east",
	"east": "west"
}

class Snake:
	def __init__(self, center):
		self.body = [center]  # List of (x, y) tuples representing the snake's body segments
		self.direction = "east"  # Initial direction: moving right
		self.grow = False  # Flag to indicate whether the snake should grow on the next move

	def move(self):
		head_x, head_y = self.body[0]
		if self.direction == "north":
			new_head = (head_x, head_y - 1)
		elif self.direction == "south":
			new_head = (head_x, head_y + 1)
		elif self.direction == "west":
			new_head = (head_x - 1, head_y)
		elif self.direction == "east":
			new_head = (head_x + 1, head_y)
		self.body.insert(0, new_head)  # Add new head to the beginning of the body
		if not self.grow:
			self.body.pop()  # Remove the last segment of the body
		else:
			self.grow = False  # Reset grow flag after using it

	def change_direction(self, new_direction):
		# Prevent the snake from reversing onto itself
		if new_direction != direction_opposites[self.direction]:
			self.direction = new_direction
