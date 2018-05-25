# -*- encoding:utf-8 -*-
#!/usr/bin/python

from Tree import No
import copy
import random

class Puzzle_slider(object):

	matrix_origin = None
	matrix_compare = None
	size = None

	father_of_all = None		# Serve para algo

	list_DFS = []
	list_BFS = []


	# Verificar se os dados passados são válidos(size. date)
	def __init__(self, size, date=None):
		self.size = size
		if date is not None:
			self.create_matrix_with_date(date)
		else:
			self.create_matrix_without_date()

	#def get_matrix_origin(self):
	#	return self.matrix_origin

	#def get_matrix_compare(self):
	#	return self.matrix_compare

	def get_father_of_all(self):
		return self.father_of_all


	def create_matrix(self):
		self.matrix_origin = [0]*self.size

		for i in range(self.size):
			self.matrix_origin[i] = [0] * self.size
		

	def create_matrix_without_date(self):
		aux = 1
		self.create_matrix()

		for i in range(self.size):
			for j in range(self.size):
				self.matrix_origin[i][j] = aux+j
			aux = aux + self.size

		self.matrix_origin[self.size-1][self.size-1]=0
		self.matrix_compare = copy.deepcopy(self.matrix_origin)

		self.father_of_all = copy.deepcopy(No(self.matrix_compare, level=0)) # Verificar a utilização do DEEP



	def create_matrix_with_date(self, date):
		return None

	# Retorna a posição onde está o ZERO
	def position_free(self, matrix):
		#print("=======", matrix)
		for i in range(self.size):
			for j in range(self.size):
				if matrix[i][j] == 0:
					return i,j
			
		#return None

	#	1 = up_down; 	2 = down_up;	3 = left_right;		4 = right_left
	def move_free(self, i,j):
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
			positions.append(2)
			positions.append(3)
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


	# Arrumar
	def matrix_reorder(self, amount, matrix, p_free_i, p_free_j):

		if amount == 1:
			matrix[p_free_i][p_free_j] = matrix[p_free_i+1][p_free_j]
			matrix[p_free_i+1][p_free_j] = 0

		elif amount == 2:
			matrix[p_free_i][p_free_j] = matrix[p_free_i-1][p_free_j]
			matrix[p_free_i-1][p_free_j] = 0

		elif amount == 3:
			matrix[p_free_i][p_free_j] = matrix[p_free_i][p_free_j+1]
			matrix[p_free_i][p_free_j+1] = 0

		elif amount == 4:
			matrix[p_free_i][p_free_j] = matrix[p_free_i][p_free_j-1]
			matrix[p_free_i][p_free_j-1] = 0

		else:
			print("Movimento ilegal")

		return matrix


	def print_t(self, matrix):
		for i in range(self.size):
			print(matrix[i])

		#return self.matrix

	def matrix_reorder_all(self, amount, matrix):

		for iterations in range(amount):
			#print("======Rodada {} ======".format(iterations))
			i,j = self.position_free(matrix)
			list_moviment_free = self.move_free(i,j)

			moviment = random.choice(list_moviment_free)
			#print("Movimento", moviment)
			self.matrix_reorder(moviment, matrix, i,j)

		return matrix

	# Criar a matriz generica p/ comparar

	def compare_matrix(self, matrix_process):
		#matrix_compare = [[1,2,3,4,],[5,6,7,8,],[9,10,11,0,]]
		status = False
		if self.matrix_compare == matrix_process:
			status = True

		return status
		

	# Recebe o objeto NO
	def Depth_First_Search(self, no):
		list_procs = []
		depth = 0	# Verificar

		list_procs.append(no.get_data())
		matrix = list_procs.pop()

		#print(matrix)

		status_compare = self.compare_matrix(matrix)

		while not status_compare:
			self.list_DFS.append(matrix)

			i,j = self.position_free(matrix)
			list_moviment_free = self.move_free(i,j)

			moviment = random.choice(list_moviment_free)
			matrix = self.matrix_reorder(moviment, matrix, i,j)

			# Criar o novo nó e atribuir a um filho

			depth = depth+1

			son = No(matrix, level=depth)
			no.set_leaf_one(son)

			son.set_father(no)

			#depth = depth+1
			list_procs.append(matrix)
			matrix = list_procs.pop()
			status_compare = self.compare_matrix(matrix)

		#print(depth)
		return son



	def Breadth_First_Search(self, matrix):
		list_procs = []
		list_BFS = []
		depth = 0

		list_procs.append(matrix)
		matrix = list_procs.pop()

		status_compare = self.compare_matrix(matrix)

		list_BFS.append(matrix)

		while not status_compare:
		#while depth != 3:

			#list_BFS.append(matrix)

			i,j = self.position_free(matrix)
			list_moviment_free = self.move_free(i,j)

			for moviment in list_moviment_free:
				matrix_aux = self.matrix_reorder(moviment, copy.deepcopy(matrix), i,j)
				list_procs.append(matrix_aux)

			matrix = list_procs.pop(0)
			status_compare = self.compare_matrix(matrix)
			list_BFS.append(matrix)

			depth = depth +1

		for ju in list_BFS:
			print(ju)
		#print(list_BFS)

		return matrix

Puzzle = Puzzle_slider(3)

Puzzle_2 = copy.deepcopy(Puzzle)

matrix_reordered = Puzzle.matrix_reorder_all(100, Puzzle.get_father_of_all().get_data())
print(matrix_reordered)

print("DFS:")
# Envia o objeto pai da árvore, p os filhos acessarem
matrix_DFS = Puzzle.Depth_First_Search(Puzzle.get_father_of_all())#copy.deepcopy(matrix_reordered))
print(matrix_DFS.get_data())
print(matrix_DFS.get_level())


#Resolver esse problema
print(Puzzle_2.get_father_of_all().get_data())

#Puzzle.print_t(matrix_DFS)

#print("BSF:")
#matrix_BFS = Puzzle.Breadth_First_Search(copy.deepcopy(matrix_reordered))
#Puzzle.print_t(matrix_BFS)

