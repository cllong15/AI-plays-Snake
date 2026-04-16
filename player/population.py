import random
from snake import Snake
class Population:
	def __init__(self, size):
		self.size = size
		self.individuals = []
		self.generation = 0
		self.global_best = 0
		self.global_best_fitness = 0
		self.current_best = 0
		self.current_best_snake = 0

		self.global_best_snake = self.individuals[0] if self.individuals else None

		self.popID = random.randint(0, 1000000)

	def create_population(self):
		for i in range(self.size):
			self.individuals.append(Snake())