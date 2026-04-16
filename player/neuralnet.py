from matrix import Matrix

class NeuralNet:
	def __init__(self, inputs, hidden, outputs):
		self.inodes = inputs
		self.hnodes = hidden
		self.onodes = outputs
		self.iweights = Matrix(self.hnodes, self.inodes + 1)
		self.hweights = Matrix(self.hnodes, self.hnodes + 1)
		self.oweights = Matrix(self.onodes, self.hnodes + 1)

		self.iweights.randomize()
		self.hweights.randomize()
		self.oweights.randomize()

	def mutate(self, mutation_rate):
		self.iweights.mutate(mutation_rate)
		self.hweights.mutate(mutation_rate)
		self.oweights.mutate(mutation_rate)

	# calculate output by feedforwarding the input through the network
	def feedforward(self, input_array):
		# convert input array to matrix
		inputs = self.oweights.single_column_matrix(input_array)
		# add bias to input matrix
		inputsbias = inputs.addbias()
		## calculate the guessed output
		# apply layer 1 weights to input
		hiddeninputs = self.iweights.dot_product(inputsbias)
		# apply activation function to hidden layer
		hiddenoutputs = hiddeninputs.activate()
		# add bias to hidden layer output
		hiddeninputsbias = hiddenoutputs.addbias()
		# apply layer 2 weights to hidden layer output
		hiddeninputs2 = self.hweights.dot_product(hiddeninputsbias)
		hiddenoutputs2 = hiddeninputs2.activate()
		hiddenoutputsbias2 = hiddenoutputs2.addbias()
		# apply layer 3 weights to hidden layer output
		outputinputs = self.oweights.dot_product(hiddenoutputsbias2)
		# apply activation function to output layer
		outputs = outputinputs.activate()
		# convert output matrix to array and return
		return outputs.to_array()
	
	#crossover function for genetic algorithm
	def crossover(self, partner):
		child = NeuralNet(self.inodes, self.hnodes, self.onodes)
		child.iweights = self.iweights.crossover(partner.iweights)
		child.hweights = self.hweights.crossover(partner.hweights)
		child.oweights = self.oweights.crossover(partner.oweights)
		return child
	
	# return a copy of this neural net
	def clone(self):
		clone = NeuralNet(self.inodes, self.hnodes, self.onodes)
		clone.iweights = self.iweights
		clone.hweights = self.hweights
		clone.oweights = self.oweights
		return clone
	
	# convert weights to a single array for saving and loading
	def net_to_array(self):
		array = {}
		array["iweights"] = self.iweights.to_array()
		array["hweights"] = self.hweights.to_array()
		array["oweights"] = self.oweights.to_array()
		return array
	
	def array_to_net(self, array):
		self.iweights.from_array(array["iweights"])
		self.hweights.from_array(array["hweights"])
		self.oweights.from_array(array["oweights"])