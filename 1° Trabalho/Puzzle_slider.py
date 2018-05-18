# -*- encoding:utf-8 -*-

class Puzzle_slider(object):

	matrix = None

	# Verificar se os dados passados são válidos(size. date)
	def __init__(self, size, date=None):
		if date is not None:
			self.create_matrix_with_date(size, date)
		else:
			self.create_matrix_without_date(size)

	def create_matrix(self, size):
		self.matrix = [0]*size

		for i in range(size):
			self.matrix[i] = [0] * size
		

	def create_matrix_without_date(self, size):
		aux = 1
		self.create_matrix(size)

		for i in range(size):
			for j in range(size):
				self.matrix[i][j] = aux+j
			aux = aux + 4

		self.matrix[size-1][size-1]=0

		print(self.matrix)

	def create_matrix_with_date(self, size, date):
		return None
	def matrix_reorder(self, amount):
		return None


juca = Puzzle_slider(4)


