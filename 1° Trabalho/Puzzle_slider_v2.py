# -*- encoding:utf-8 -*-
#!/usr/bin/python

from Tree import No
from memory_profiler import memory_usage
import copy
import random
import time

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

    def set_father_of_all(self, matrix):
        self.father_of_all.set_data(matrix)# = matrix


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

       # self.matrix_origin = [[0, 6, 2,], [1, 3, 8,], [4, 7, 5,]]
        self.matrix_compare = copy.deepcopy(self.matrix_origin)

        self.father_of_all = copy.deepcopy(No(self.matrix_compare, level=0))



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

        return copy.deepcopy(matrix)

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

        list_procs.append(no)
        matrix = list_procs.pop().get_data()

        status_compare = self.compare_matrix(matrix)

        while not status_compare:
            self.list_DFS.append(matrix)

            i,j = self.position_free(matrix)
            list_moviment_free = self.move_free(i,j)

            moviment = random.choice(list_moviment_free)
            matrix = self.matrix_reorder(moviment, matrix, i,j)

            
            depth = depth+1		# Utilizado p/ salvar a profundidade do nó
            # Cria o novo nó e atribui pai a um filho
            son = No(matrix, level=depth)
            no.set_leaf(son)
            son.set_father(no)
            #-----------------------------------------

            list_procs.append(son)
            no = list_procs.pop()
            matrix = no.get_data()
            status_compare = self.compare_matrix(matrix)

        return son



    def Breadth_First_Search(self, no):
        list_procs = []		# Lista dos nós a serem processados
        list_BFS = []		# Lista dos nós visitados
        depth = 0			# Utiliza

        list_procs.append(no)	# Adiciona na lista o nó a ser processado
        matrix = list_procs.pop().get_data()

        status_compare = self.compare_matrix(matrix)
        list_BFS.append(matrix)		# Adiciona na lista o matrix processada

        while not status_compare:
            depth = depth +1
            i,j = self.position_free(matrix)
            list_moviment_free = self.move_free(i,j)

            for moviment in list_moviment_free:		# Realiza tds os movimentos possíveis
                matrix_aux = self.matrix_reorder(moviment, copy.deepcopy(matrix), i,j)
                
                son = No(copy.deepcopy(matrix_aux), level=depth)
                no.set_leaf(son)
                son.set_father(no)

                list_procs.append(son)

            no = list_procs.pop(0)

            depth = no.get_level()
            matrix = no.get_data()
            status_compare = self.compare_matrix(matrix)
            
            list_BFS.append(no.get_data())

        return no


    def Iterative_Depth_Search(self, no, level):
        list_procs = []
        list_IDS = []
        list_IDS_aux = []
        list_IDS_level = []
        depth = 0

        list_procs.append(no)	# Adiciona na lista o nó a ser processado
        matrix = list_procs.pop().get_data()
        print("MATRIIXXX: ", matrix)

        status_compare = self.compare_matrix(matrix)
        list_IDS.append(matrix)
        #print("Matrix: ",matrix)

        while not status_compare:
            aux=0
            #print("Entrou")
            if depth == level:			
                if list_procs != None:
                    list_IDS_aux.append(no)

                    no = list_procs.pop()
                    matrix = no.get_data()
                    depth = no.get_level()
                else:
                    print("Lista vazia")

            depth = depth +1
            i,j = self.position_free(matrix)
            list_moviment_free = self.move_free(i,j)	

            
            if depth != level and depth < level-1:
                for moviment in list_moviment_free:
                        
                    matrix_aux = self.matrix_reorder(moviment, copy.deepcopy(matrix), i,j)
                    if aux != 0:
                        son = No(copy.deepcopy(matrix_aux), level=depth)	
                        list_procs.append(son)
                        no.set_leaf(son)
                        son.set_father(no)
                        
                    else:		# Faz a busca em profundidade
                        son_aux = No(copy.deepcopy(matrix_aux), level=depth)
                        no.set_leaf(son_aux)
                        son_aux.set_father(no)

                    aux = aux+1

                no = son_aux

            matrix = no.get_data()
            print("Matrix: "+str(matrix)+"Depth: "+str(depth))
            list_IDS.append(matrix)
            status_compare = self.compare_matrix(matrix)
            #depth = depth +1

        #print(depth)
        return no


        
Puzzle = Puzzle_slider(3)

#Puzzle_2 = copy.deepcopy(Puzzle)


matrix_reordered = Puzzle.matrix_reorder_all(10, Puzzle.get_father_of_all().get_data())
print("Matriz entrada: ")
print(matrix_reordered)
print("")

# print("DFS:")
# # Envia o objeto pai da árvore, p os filhos acessarem
# t0 = time.time()
# matrix_DFS = Puzzle.Depth_First_Search(copy.deepcopy(Puzzle.get_father_of_all()))#copy.deepcopy(matrix_reordered))
# t1 = time.time()


# print(matrix_DFS.get_data())
# print(matrix_DFS.get_level())
# print ("Total time running: %s seconds" %(str(t1-t0)))

#Resolver esse problema


#print(matrix_reordered)

#print(Puzzle.get_father_of_all().get_data())
# print("BSF:")
# t0 = time.time()
# matrix_BFS = Puzzle.Breadth_First_Search(copy.deepcopy(Puzzle.get_father_of_all()))
# t1 = time.time()

# print(matrix_BFS.get_data())
# print(matrix_BFS.get_level())

# print("Total time running: %s seconds" %(str(t1-t0)))

#juca = [[0, 6, 2,], [1, 3, 8,], [4, 7, 5,]]
juca = [[1, 2, 3,], [4, 5, 6,], [0, 7, 8,]]

Puzzle.set_father_of_all(juca)

print("IDS:")
t0 = time.time()
matrix_IDS = Puzzle.Iterative_Depth_Search(copy.deepcopy(Puzzle.get_father_of_all()), 13)
print(matrix_IDS.get_data())
print(matrix_IDS.get_level())
#matrix_IDS = Puzzle.Iterative_Depth_Search(copy.deepcopy(Puzzle.get_father_of_all()), 20)
t1 = time.time()
print ("Total time running: %s seconds" %(str(t1-t0)))
