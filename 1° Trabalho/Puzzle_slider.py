#!/usr/bin/python

# -*- encoding:utf-8 -*-
import random

class Puzzle_slider(object):

	matrix = None
	size = None

	# Verificar se os dados passados são válidos(size. date)
	def __init__(self, size, date=None):
		self.size = size
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

	# Retorna a posição onde está o ZERO
	def return_position_free(self):
		for i in range(self.size):
			for j in range(self.size):
				if self.matrix[i][j] == 0:
					return i,j
			
		return None

	#	1 = up_down; 	2 = down_up;	3 = left_right;		4 = right_left
	def move(self, i,j):
		#i,j = self.return_position_free()

		positions = []

		if i==0 and j==0:
			positions.append(1)
			positions.append(3)
			return positions
			#return 1,None,3,None
		elif i==0 and j!= self.size-1:
			positions.append(1)
			positions.append(3)
			positions.append(4)
			return positions
			#return 1, None, 3, 4
		elif i==0 and j== self.size-1:
			#return 1, None, None, 4
			positions.append(1)
			positions.append(4)
			return positions

		elif i!=self.size-1 and j==0:
			positions.append(1)
			positions.append(2)
			positions.append(3)
			return positions
			#return 1,2,3,None
		elif i==self.size-1 and j==0:
			positions.append(2)
			positions.append(3)
			return positions
			#return None,2,3,None

		elif i!=self.size-1 and j!=self.size-1:
			positions.append(1)
			positions.append(3)
			positions.append(2)
			positions.append(4)
			return positions
			#return 1,2,None,4

		elif i==self.size-1 and j!=self.size-1:
			positions.append(2)
			positions.append(3)
			positions.append(4)
			return positions
			#return None,2,3,4

		elif i==self.size-1 and j==self.size-1:
			positions.append(2)
			positions.append(4)
			return positions



		elif i!=self.size-1 and j==self.size-1:
			positions.append(1)
			positions.append(2)
			positions.append(4)
			return positions
			#return 1,None,None,4

		else:
			print("CASO DESCONHECIDO")


	def matrix_reorder(self, amount, p_free_i, p_free_j):

		if amount == 1:
			self.matrix[p_free_i][p_free_j] = self.matrix[p_free_i+1][p_free_j]
			self.matrix[p_free_i+1][p_free_j] = 0

		elif amount == 2:
			self.matrix[p_free_i][p_free_j] = self.matrix[p_free_i-1][p_free_j]
			self.matrix[p_free_i-1][p_free_j] = 0

		elif amount == 3:
			self.matrix[p_free_i][p_free_j] = self.matrix[p_free_i][p_free_j+1]
			self.matrix[p_free_i][p_free_j+1] = 0

		elif amount == 4:
			self.matrix[p_free_i][p_free_j] = self.matrix[p_free_i][p_free_j-1]
			self.matrix[p_free_i][p_free_j-1] = 0

		else:
			print("Movimento ilegal")


	def print(self):
		for i in range(self.size):
				print(self.matrix[i])

		#return self.matrix


juca = Puzzle_slider(4)

print()
juca.print()

for i in range(0,100):
	print("======Rodada {} ======".format(i))

	i,j = juca.return_position_free()
	list_j = juca.move(i,j)

	num = random.choice(list_j)
	print("Movimento", num)
	juca.matrix_reorder(num, i,j)
	juca.print()







