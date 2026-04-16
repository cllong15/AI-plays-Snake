import random

class Matrix:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]

	def print_matrix(self):
		for row in self.matrix:
			print(row)
	
	def multiply_scalar(self, scalar):
		for i in range(self.rows):
			for j in range(self.cols):
				self.matrix[i][j] *= scalar

	def dot_product(self, other):
		if self.cols != other.rows:
			raise ValueError("Incompatible dimensions for dot product")
		result = Matrix(self.rows, other.cols)
		for i in range(result.rows):
			for j in range(result.cols):
				sum_product = 0
				for k in range(self.cols):
					sum_product += self.matrix[i][k] * other.matrix[k][j]
				result.matrix[i][j] = sum_product
		return result
	
	def randomize(self):
		for i in range(self.rows):
			for j in range(self.cols):
				self.matrix[i][j] = random.random()
	def scalar_add(self, scalar):
		for i in range(self.rows):
			for j in range(self.cols):
				self.matrix[i][j] += scalar
	
	def parameter_add(self, other):
		if self.rows != other.rows or self.cols != other.cols:
			raise ValueError("Matrices must have the same dimensions for parameter addition")
		newMatrix = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				newMatrix.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
		return newMatrix
	
	def parameter_sub(self, other):
		if self.rows != other.rows or self.cols != other.cols:
			raise ValueError("Matrices must have the same dimensions for parameter subtraction")
		newMatrix = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				newMatrix.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]
		return newMatrix
	
	def parameter_mult(self, other):
		if self.rows != other.rows or self.cols != other.cols:
			raise ValueError("Matrices must have the same dimensions for parameter multiplication")
		newMatrix = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				newMatrix.matrix[i][j] = self.matrix[i][j] * other.matrix[i][j]
		return newMatrix
	
	def transpose(self):
		newMatrix = Matrix(self.cols, self.rows)
		for i in range(self.rows):
			for j in range(self.cols):
				newMatrix.matrix[j][i] = self.matrix[i][j]
		return newMatrix
	
	# create single column matrix from parameter matrix
	def single_column_matrix(self, matrix):
		if self.cols != 1:
			raise ValueError("Matrix must have one column for to_array")
		newMatrix = Matrix(len(matrix), 1)
		for i in range(len(matrix)):
			newMatrix.matrix[i][0] = matrix[i]
		return newMatrix

	def from_array(self, array):
		if self.rows != len(array) or self.cols != 1:
			raise ValueError(f"Matrix must have dimensions {len(array)} for from_array")
		for i in range(self.rows):
			for j in range(self.cols):
				self.matrix[i][j] = array[j+i*self.cols]
	
	def to_array(self):
		if self.cols != 1:
			raise ValueError("Matrix must have one column for to_array")
		array = [0 for _ in range(self.rows*self.cols)]
		for i in range(self.rows):
			for j in range(self.cols):
				array[j+i*self.cols] = self.matrix[i][j]
		return array
	
	def addbias(self):
		newMatrix = Matrix(self.rows + 1, 1)
		for i in range(self.rows):
			newMatrix.matrix[i][0] = self.matrix[i][0]
		newMatrix.matrix[self.rows][0] = 1
		return newMatrix
	
	def removebias(self):
		if self.rows < 2:
			raise ValueError("Matrix must have at least 2 rows to remove bias")
		newMatrix = Matrix(self.rows - 1, self.cols)
		for i in range(self.rows - 1):
			for j in range(self.cols):
				newMatrix.matrix[i][j] = self.matrix[i][j]
		return newMatrix
	
	def activate(self):
		newMatrix = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				newMatrix.matrix[i][j] = 1 / (1 + pow(2.71828, -self.matrix[i][j]))
		return newMatrix
	
	def sigmoid_derived(self):
		newMatrix = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				# sigmoid_value = 1 / (1 + pow(2.71828, -self.matrix[i][j]))
				newMatrix.matrix[i][j] = (self.matrix[i][j]) * (1 - self.matrix[i][j])
		return newMatrix
	
	def mutate(self, mutation_rate):
		for i in range(self.rows):
			for j in range(self.cols):
				rand = random.random()
				if rand < mutation_rate: # if chosen to be mutated
					self.matrix[i][j] += random.gauss(0, 0.2)  # Add small random value from normal distribution

					if self.matrix[i][j] > 1:  # Clamp to 1
						self.matrix[i][j] = 1
					elif self.matrix[i][j] < -1:  # Clamp to -1
						self.matrix[i][j] = -1

	def crossover(self, partner):
		if self.rows != partner.rows or self.cols != partner.cols:
			raise ValueError("Matrices must have the same dimensions for crossover")
		child = Matrix(self.rows, self.cols)
		crossover_point = random.randint(0, self.rows * self.cols - 1)
		for i in range(self.rows):
			for j in range(self.cols):
				index = j + i * self.cols
				if index < crossover_point:
					child.matrix[i][j] = self.matrix[i][j]
				else:
					child.matrix[i][j] = partner.matrix[i][j]
		return child
	
	def clone(self):
		clone = Matrix(self.rows, self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				clone.matrix[i][j] = self.matrix[i][j]
		return clone