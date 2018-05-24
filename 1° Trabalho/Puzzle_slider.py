# -*- encoding:utf-8 -*-
#!/usr/bin/python


import random

class Puzzle_slider(object):

	matrix_origin = None
	matrix_compare = None

	size = None

	# Verificar se os dados passados são válidos(size. date)
	def __init__(self, size, date=None):
		self.size = size
		if date is not None:
			self.create_matrix_with_date(size, date)
		else:
			self.create_matrix_without_date(size)

	def get_matrix_origin(self):
		return self.matrix_origin

	def get_matrix_compare(self):
		return self.matrix_compare


	def create_matrix(self, size):
		self.matrix_origin = [0]*size
		self.matrix_compare = [0] * size

		for i in range(size):
			self.matrix_origin[i] = [0] * size
			self.matrix_compare[i] = [0] * size
		

	def create_matrix_without_date(self, size):
		aux = 1
		self.create_matrix(size)

		for i in range(size):
			for j in range(size):
				self.matrix_origin[i][j] = aux+j
				self.matrix_compare[i][j] = aux+j
			aux = aux + size

		#juca = self.matrix_origin

		self.matrix_origin[size-1][size-1]=0
		self.matrix_compare[size-1][size-1]=0
		#self.matrix_compare = self.ma

		return self.matrix_origin

		#print(self.matrix)

	def create_matrix_with_date(self, size, date):
		return None

	# Retorna a posição onde está o ZERO
	def position_free(self, matrix):
		for i in range(self.size):
			for j in range(self.size):
				if matrix[i][j] == 0:
					return i,j
			
		return None

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

	# Criar status matriz reordenada
	# Busca em profundidade
	# Adicionar uma fila de processos
	# Adicionar uma lista de nodos processados
	"""def Depth_First_Search(self, matrix):
		status_compare = self.compare_matrix(matrix)
		aux = 0
		print(status_compare)

		while not status_compare:
			i,j = self.position_free(matrix)
			list_moviment_free = self.move_free(i,j)

			moviment = random.choice(list_moviment_free)
			#print("Movimento", moviment)
			matrix = self.matrix_reorder(moviment, matrix, i,j)

			status_compare = self.compare_matrix(matrix)
			aux = aux +1
		print(aux)

		return matrix"""

	def Depth_First_Search(self, matrix):
		list_procs = []
		list_DFS = []
		depth = 0

		list_procs.append(matrix)
		matrix = list_procs.pop()

		status_compare = self.compare_matrix(matrix)

		while not status_compare:
			list_DFS.append(matrix)

			i,j = self.position_free(matrix)
			list_moviment_free = self.move_free(i,j)

			moviment = random.choice(list_moviment_free)
			matrix = self.matrix_reorder(moviment, matrix, i,j)

			list_procs.append(matrix)
			matrix = list_procs.pop()

			status_compare = self.compare_matrix(matrix)
			depth = depth +1
			#list_procs.append(matrix)
		#print(depth)

		return matrix

	def Breadth_First_Search(self, matrix):
		list_procs = []
		list_BFS = []
		depth = 0

		list_procs.append(matrix)
		matrix = list_procs.pop()

		status_compare = self.compare_matrix(matrix)

		print(matrix)
		print("")
		#while not status_compare:
		print("=====LOOP+++++")
		while depth != 2:

			list_BFS.append(matrix)
#----------------------------------------------------
			i,j = self.position_free(matrix)
			list_moviment_free = self.move_free(i,j)

			print("Movimentos: ",list_moviment_free)
			self.print_t(matrix)

			print("====================")
			for moviment in list_moviment_free:
				matrix_aux = self.matrix_reorder(moviment, matrix, i,j)
				list_procs.append(matrix_aux)
				print("")
				self.print_t(matrix_aux)
			print("====================")
			matrix = list_procs.pop(0)
			status_compare = self.compare_matrix(matrix)
			depth = depth +1
			#list_procs.append(matrix)

#----------------------------------------------------
		return matrix

Puzzle = Puzzle_slider(3)

matrix_reordered = Puzzle.matrix_reorder_all(100, Puzzle.get_matrix_origin())
#Puzzle.print_t(matrix_reordered)
print(matrix_reordered)
#juca = matrix_reordered

#matrix_DFS = Puzzle.Depth_First_Search(matrix_reordered)
#print("DFS:")
#Puzzle.print_t(matrix_DFS)

#print(juca)

matrix_BFS = Puzzle.Breadth_First_Search(matrix_reordered)
print("BSF:")
Puzzle.print_t(matrix_BFS)

	