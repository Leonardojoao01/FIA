# -*- encoding:utf-8 -*-
#!/usr/bin/python

from memory_profiler import memory_usage
from Tree import No
import copy
import random
import time
#import os
#import psutil
#import gc, sys
#import resource
import heapq

class Puzzle_slider(object):
    
    # matrix_origin = None
    # matrix_compare = None

    # size = None

    # fila_1 = None
    # indice_1 = None

    # fila_2 = None
    # indice_2 = None

    list_DFS    = []
    list_BFS    = []
    list_IDS    = []
    list_A_star = []

    # Verificar se os dados passados são válidos(size. date)
    def __init__(self, size, date=None):
        self.size     = size

        self.fila_1   = []
        self.indice_1 = 0
        self.fila_2   = []
        self.indice_2 = 0

        if date is not None:
            self.create_matrix_with_date(size, date)
        else:
            self.create_matrix_without_date(size)

    def get_matrix_origin(self):
        return self.matrix_origin

    def get_matrix_compare(self):
        return self.matrix_compare

    # ================Fila de prioridade da matrix================
    def inserir_matrix(self, item, prioridade):
        heapq.heappush(self.fila_1, (prioridade, self.indice_1, item))
        self.indice_1 += 1

    def remover_matrix(self):
        return heapq.heappop(self.fila_1)[-1]
    #=======Fila de prioridade do depth relacionado a matrix=======
    def inserir_depth(self, item, prioridade):
        heapq.heappush(self.fila_2, (prioridade, self.indice_2, item))
        self.indice_2 += 1

    def remover_depth(self):
        return heapq.heappop(self.fila_2)[-1]
    #==============================================================

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

        self.matrix_origin[size-1][size-1]=0
        self.matrix_compare[size-1][size-1]=0

        return self.matrix_origin


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
        matrix_aux = copy.copy(matrix)
        if amount == 1:
            matrix_aux[p_free_i][p_free_j] = matrix_aux[p_free_i+1][p_free_j]
            matrix_aux[p_free_i+1][p_free_j] = 0

        elif amount == 2:
            matrix_aux[p_free_i][p_free_j] = matrix_aux[p_free_i-1][p_free_j]
            matrix_aux[p_free_i-1][p_free_j] = 0

        elif amount == 3:
            matrix_aux[p_free_i][p_free_j] = matrix_aux[p_free_i][p_free_j+1]
            matrix_aux[p_free_i][p_free_j+1] = 0

        elif amount == 4:
            matrix_aux[p_free_i][p_free_j] = matrix_aux[p_free_i][p_free_j-1]
            matrix_aux[p_free_i][p_free_j-1] = 0

        else:
            print("Movimento ilegal")

        return matrix_aux

    def print_t(self, matrix):
            for i in range(self.size):
                print(matrix[i])

        #return self.matrix


    def matrix_reorder_all(self, amount, matrix):
    
        for iterations in range(amount):
            i,j = self.position_free(matrix)
            list_moviment_free = self.move_free(i,j)

            moviment = random.choice(list_moviment_free)
            self.matrix_reorder(moviment, matrix, i,j)

        return matrix


    def compare_matrix(self, matrix_process):
        status = False
        if self.matrix_compare == matrix_process:
                status = True

        return status
        
    
    def Depth_First_Search(self, matrix):
        list_procs = []
        #list_DFS = []
        depth = 0

        list_procs.append(matrix)
        matrix = list_procs.pop()

        status_compare = self.compare_matrix(matrix)

        while not status_compare:
            self.list_DFS.append(matrix)

            i,j = self.position_free(matrix)
            list_moviment_free = self.move_free(i,j)

            moviment = random.choice(list_moviment_free)
            matrix = self.matrix_reorder(moviment, matrix, i,j)

            list_procs.append(matrix)
            matrix = list_procs.pop()

            status_compare = self.compare_matrix(matrix)
            depth = depth +1

        self.list_DFS.append(matrix)
        print(depth)
        return matrix
    
    def Breadth_First_Search(self, matrix):
        list_procs = []
        #self.list_BFS = []
        list_BFS_level = []
        depth = 0
        #depth_final = 0

        list_procs.append(matrix)
        matrix = list_procs.pop()

        status_compare = self.compare_matrix(matrix)

        #self.list_BFS.append(matrix)

        while not status_compare:
            self.list_BFS.append(matrix)
            depth = depth + 1
            i,j = self.position_free(matrix)
            list_moviment_free = self.move_free(i,j)

            for moviment in list_moviment_free:
                matrix_aux = self.matrix_reorder(moviment, copy.deepcopy(matrix), i,j)
                list_procs.append(matrix_aux)
                list_BFS_level.append(depth)

            matrix = list_procs.pop(0)
            depth =  list_BFS_level.pop(0)
            status_compare = self.compare_matrix(matrix)
            self.list_BFS.append(matrix)

        print(depth)
        self.list_BFS.append(matrix)
        return matrix
    
    def Iterative_Depth_Search(self, matrix, level):
        list_procs = []
        self.list_IDS = []
        depth = 0

        self.list_IDS.append(matrix)
        status_compare = self.compare_matrix(matrix)

        while depth <= level and not status_compare:
            depth = depth + 1

            while len(self.list_IDS) != 0:
                matrix = self.list_IDS.pop()

                i,j = self.position_free(matrix)
                list_moviment_free = self.move_free(i,j)
                for moviment in list_moviment_free:
                    matrix_aux = self.matrix_reorder(moviment, copy.deepcopy(matrix), i,j)
                    list_procs.append(matrix_aux)
            
            for matrix in list_procs:
                self.list_IDS.append(matrix)
                status_compare_aux = self.compare_matrix(matrix)
                if status_compare_aux:
                    status_compare = True

        print(depth)  
        return matrix    

    def heuristic_1(self, matrix):
        h=0    
        for x in range(self.size):
            for y in range(self.size):
                if matrix[x][y] != (self.size*x + y+1):
                    h +=1
        
        if matrix[self.size-1][self.size-1] == 0:
            h -=1

        return h
    
    def heuristic_2(self, puzzle):
        distanciaManhattanTotal = 0
          
        for i in range(self.size):
            for j in range(self.size):
                if puzzle[i][j] == 0: continue
                distanciaManhattanTotal += abs(i - (puzzle[i][j]/4)) + abs(j -  (puzzle[i][j]%4));
        return distanciaManhattanTotal

    def heuristic_3(self, puzzle):
        distanciaManhattanTotal = 0
          
        for i in range(self.size):
            for j in range(self.size):
                if puzzle[i][j] == 0: continue
                distanciaManhattanTotal += abs(i - (puzzle[i][j]/4)) * abs(j -  (puzzle[i][j]%4));
        return distanciaManhattanTotal

    def A_star(self, matrix, heuristic):
        list_A_star = []
        list_A_star_level = []
        depth = 0

        status_compare = self.compare_matrix(matrix)
        list_A_star.append(matrix)

        value_heuristic = self.heuristic_1(matrix)
        self.inserir_matrix(matrix, value_heuristic)
        matrix = self.remover_matrix()

        # value_heuristic = self.heuristica(matrix)
        # print("value_heuristic:", value_heuristic)

        # value_heuristic = self.heuristic_1(matrix)
        # print("value_heuristic:", value_heuristic)
        
        while not status_compare:
            i,j = self.position_free(matrix)
            list_moviment_free = self.move_free(i,j)

            for moviment in list_moviment_free:
                matrix_aux = self.matrix_reorder(moviment, copy.deepcopy(matrix), i,j)

                value_heuristic = self.heuristic_3(matrix_aux)
                F = depth *10 + value_heuristic
                self.inserir_matrix(matrix_aux, F)
                self.inserir_depth(depth+1, F)

            matrix = self.remover_matrix()
            depth = self.remover_depth()
            list_A_star.append(matrix)
            status_compare = self.compare_matrix(matrix)
        
        print(depth)
        return matrix


# print("Máximo uso de memória: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f') + " MB")

# Puzzle = Puzzle_slider(3)

# matrix_reordered = Puzzle.matrix_reorder_all(20, Puzzle.get_matrix_origin())
# print(matrix_reordered)

# print("Máximo uso de memória: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f') + " MB")

# print("DFS:")
# t0 = time.time()
# matrix_DFS = Puzzle.Depth_First_Search(copy.deepcopy(matrix_reordered))
# t1 = time.time()
# print ("Total time running: %s seconds" %(str(t1-t0)))


# print("Máximo uso de memória: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f') + " MB")

# Puzzle.print_t(matrix_DFS)

# print("Máximo uso de memória: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f') + " MB")
# print("BSF:")
# t0 = time.time()
# matrix_BFS = Puzzle.Breadth_First_Search(copy.deepcopy(matrix_reordered))
# t1 = time.time()
# print ("Total time running: %s seconds" %(str(t1-t0)))

# print("Máximo uso de memória: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f') + " MB")
# Puzzle.print_t(matrix_BFS)


# print("Máximo uso de memória: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f') + " MB")
# print("IDS:")
# t0 = time.time()
# matrix_IDS = Puzzle.Iterative_Depth_Search(copy.deepcopy(matrix_reordered), 20)
# t1 = time.time()
# print ("Total time running: %s seconds" %(str(t1-t0)))


# print("Máximo uso de memória: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f') + " MB")
# Puzzle.print_t(matrix_IDS)

