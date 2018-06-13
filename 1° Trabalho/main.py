# -*- encoding:utf-8 -*-
#!/usr/bin/python

from Puzzle_slider import Puzzle_slider
import time
import copy
import resource
import sys

Puzzle = Puzzle_slider(3)

#matrix = Puzzle.matrix_reorder_all(20, Puzzle.get_matrix_origin())
#print(matrix)

#matrix = [[1, 3, 5], [4, 0, 2], [7, 8, 6]]         # 6 Movimentos
#matrix = [[1, 6, 2], [5, 3, 8], [4, 7, 0]]         # 8 Movimentos
#matrix = [[0, 1, 2], [4, 5, 8], [7, 6, 3]]         # 10 Movimentos
matrix = [[0, 2, 3], [1, 6, 8], [7, 5, 4]]         # 12 Movimentos
#matrix = [[1, 2, 0], [4, 5, 3], [6, 7, 8]]         # 14 Movimentos


if str(sys.argv[1]) == "DFS":
    t0 = time.time()
    matrix_DFS = Puzzle.Depth_First_Search(copy.deepcopy(matrix))
    t1 = time.time()
    print(str(t1-t0))
    print(format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f'))

elif str(sys.argv[1]) == "BFS": 
    t0 = time.time()
    matrix_BFS = Puzzle.Breadth_First_Search(copy.deepcopy(matrix))    
    t1 = time.time()
    print(str(t1-t0))
    print(format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f'))

elif str(sys.argv[1]) == "IDS":
    t0 = time.time()
    matrix_IDS = Puzzle.Iterative_Depth_Search(copy.deepcopy(matrix),12)
    t1 = time.time()
    print(str(t1-t0))
    print(format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f'))

elif str(sys.argv[1]) == "A_star":
    #print("A_star")
    t0 = time.time()
    matrix_A_star = Puzzle.A_star(copy.deepcopy(matrix),1)
    t1 = time.time()
    print(str(t1-t0))
    print(format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f'))
    
else:
    print("Nenhum dos casos")
