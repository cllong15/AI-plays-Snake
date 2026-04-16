from player.population import Population

class world():
	def __init__(self, species_num=5, popsize=100):

		self.generation = 0
		self.species = Population(species_num)
		for i in range(self.species_number):
			self.species.individuals[i] = Population(popsize)
		self.top_brains = []
		self.world_best = 0
