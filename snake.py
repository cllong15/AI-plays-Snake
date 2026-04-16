from constants import constants
from player.neuralnet import NeuralNet

class Snake:
	def __init__(self, win):
		self._win = win
		self.grid = win.grid

		# The snake starts in the center of the grid, so we initialize its body with the center cell and the tail extending to the north
		self.head_pos = self.grid._center.coords  # center cell of the grid
		self.length = 4  # Initial length of the snake
		body = []
		for i in range(self.length):
			body.append((self.head_pos[0] - i, self.head_pos[1]))  # Extend the body to the north
			# This creates a vertical snake starting from the center and extending upwards
			# For example, if the head is at (5, 5), the body will be [(5, 5), (4, 5), (3, 5), (2, 5)]
		self.body = body  # List of Cell objects
		self.direction = self.grid.get_cell(
			self.head_pos[0] + 1,
			self.head_pos[1]
			).south  # Initial direction: moving down

		self.brain = NeuralNet(24, 18, 4)  # Placeholder for AI brain
		self.vision = 24  # Placeholder for AI vision
		self.decision = None  # Placeholder for AI decision
		self.food = None # Placeholder for food position (can be set to the grid's food position when needed)

		self.lifetime = 0  # Number of moves made
		self.score = 0  # Score based on food eaten
		self.fitness = 0  # Fitness score for AI training
		self.moves_left = 200  # Moves left before the snake dies (can be adjusted based on game rules)

		self.alive = True  # Flag to indicate if the snake is alive
		self.tested = False  # Flag to indicate if the snake is being tested rather than trained

	def mutate(self):
		self.brain.mutate(0.1)  # Mutate the neural net

	def move(self):
		self.lifetime += 1  # Increment lifetime with each move
		self.moves_left -= 1  # Decrement moves left with each move
		if self.moves_left <= 0:
			self.alive = False  # Snake dies if it runs out of moves
		
		if self.collision():
			self.alive = False  # Snake dies if it collides
		
		if self.head_pos.food:
			self.head_pos.food = False  # Remove food from the current cell
			self.score += 1  # Increment score for eating food
			self.moves_left += 100  # Reset moves left after eating food
			self.grid.food = None  # Remove the food from the grid
			self.grid.make_food()  # Create new food on the grid
			# The snake grows by not removing the tail segment when it eats food
		else:
			old = self.body.pop()  # Remove the last segment of the body
			self._win.draw_cell(old, "black")  # Clear the old tail cell

		# Find the new head cell from the grid based on the current direction
		new_head_cell = self.grid.get_cell(self.direction.coords)
		self.body.insert(0, new_head_cell)  # Add new head to the beginning of the body
		self.head_pos = new_head_cell  # Update head position to the new cell

		self.draw()  # Redraw the snake in its new position

	def change_direction(self, new_direction):
		self.decision = self.brain.output(self.vision)  # Get the AI's decision based on its vision
		index = self.decision.index(max(self.decision))  # Get the index of the highest output value
		match self.decision:
			case index if index == 0:
				self.direction = (self.head_pos[0], self.head_pos[1] - 1)  # Move north
			case index if index == 1:
				self.direction = (self.head_pos[0], self.head_pos[1] + 1)  # Move south
			case index if index == 2:
				self.direction = (self.head_pos[0] - 1, self.head_pos[1])  # Move west
			case index if index == 3:
				self.direction = (self.head_pos[0] + 1, self.head_pos[1])  # Move east

	def draw(self, fill_color="green"):
		for cell in self.body:
			self._win.draw_cell(cell, fill_color)
		
	def collision(self):
		# Check for collision with walls
		if 0 > self.head_pos.coords[0] >= self._win.grid._num_cols or 0 > self.head_pos.coords[1] >= self._win.grid._num_rows:
			return True
		# Check for collision with itself
		if self.head_pos in self.body[1:]:
			return True
		return False
	
	def calculate_fitness(self):
		# Fitness can be based on score and lifetime, with a bonus for surviving longer
		if self.score < 10:
			self.fitness = self.score * self.lifetime * pow(2, (self.length))
		else:
			self.fitness = self.score * self.lifetime * pow(2, 10)  * (self.length - 9)  # Cap the length bonus at 10 for fitness calculation

	def crossover(self, partner):
		child = Snake(self._win)  # Create a new snake for the child
		child.brain = self.brain.crossover(partner.brain)  # Crossover the neural nets
		return child
	
	def clone(self):
		clone = Snake(self._win)  # Create a new snake for the clone
		clone.brain = self.brain.clone()  # Clone the neural net
		clone.alive = True  # Ensure the clone starts alive
		return clone
	
	def save_snake(self, snakeID, score, popID):
		pass # TODO save to database
		# Save the snake's brain and relevant data to a database for later analysis or reuse
	
	def load_snake(self, snakeID):
		pass # TODO load from database
		# Load a snake's brain and relevant data from a database using its ID for testing or further training

	def look(self):
		self.vision = []  # Reset vision array
		# look west
		self.vision.extend(self.look_in_direction("west"))
		# look northwest
		self.vision.extend(self.look_in_direction("northwest"))
		# look north
		self.vision.extend(self.look_in_direction("north"))
		# look northeast
		self.vision.extend(self.look_in_direction("northeast"))
		# look east
		self.vision.extend(self.look_in_direction("east"))
		# look southeast
		self.vision.extend(self.look_in_direction("southeast"))
		# look south
		self.vision.extend(self.look_in_direction("south"))
		# look southwest
		self.vision.extend(self.look_in_direction("southwest"))
		
	def look_in_direction(self, direction):
		# look in the specified direction and return the distance to the nearest food, wall, and body segment
		vision_in_direction = [0, 0, 0]  # [food_distance, wall_distance, body_distance]
		position = self.head_pos.next_cell(direction)  # Start looking from the cell adjacent to the head in the specified direction
		found_food = False
		found_tail = False
		distance = 1
		while position.coords[0] < self.grid.num_cols and position.coords[0] >= 0 and position.coords[1] < self.grid.num_rows and position.coords[1] >= 0:
			if not found_food and position.food:
				vision_in_direction[0] = 1 / distance  # Inverse of distance to food
				found_food = True
			if not found_tail and position in self.body:
				vision_in_direction[2] = 1 / distance  # Inverse of distance to body segment
				found_tail = True
			position = position.next_cell(direction)  # Move to the next cell in the same direction
			distance += 1
		
		vision_in_direction[1] = 1 / distance  # Inverse of distance to wall (when we go out of bounds)
		return vision_in_direction