# -*- encoding:utf-8 -*-
#!/usr/bin/python

from Puzzle_slider import Puzzle_slider
import time
import copy
import resource
import sys

Puzzle = Puzzle_slider(3)

#matrix = Puzzle.matrix_reorder_all(10, Puzzle.get_matrix_origin())
#print(matrix)

#matrix = [[0, 3], [2, 1]]                           # 6 Movimentos

#matrix = [[1, 3, 5], [4, 0, 2], [7, 8, 6]]         # 6 Movimentos
#matrix = [[1, 6, 2], [5, 3, 8], [4, 7, 0]]         # 10 Movimentos
#matrix = [[0, 2, 3], [1, 6, 8], [7, 5, 4]]         # 12 Movimentos
matrix = [[1, 2, 0], [4, 5, 3], [6, 7, 8]]         # 14 Movimentos


#matrix = [[1, 2, 3, 4], [5, 6, 0, 8], [9, 10, 7, 12], [13, 14, 11, 15]]    # 3 Movimentos
#matrix = [[1, 0, 3, 4], [5, 2, 6, 8], [9, 10, 7, 12], [13, 14, 11, 15]]    # 5 Movimentos
#matrix = [[2, 5, 3, 4], [9, 1, 6, 8], [0, 11, 7, 12], [13, 10, 14, 15]]    # 12 Movimentos
#matrix = [[5, 1, 3, 4], [10, 9, 6, 7], [13, 2, 14, 12], [15, 0, 8, 11]]    # 22 Movimentos

#matrix = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [11, 12, 13, 14, 15, 16, 17, 18, 19, 20], [21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [31, 32, 33, 34, 35, 36, 37, 38, 39, 40], [41, 42, 43, 44, 45, 46, 47, 49, 0, 50], [51, 52, 53, 54, 55, 56, 57, 48, 59, 60], [61, 62, 63, 64, 65, 66, 67, 58, 69, 70], [71, 72, 73, 74, 75, 76, 77, 68, 79, 80], [81, 82, 83, 84, 85, 86, 87, 78, 88, 90], [91, 92, 93, 94, 95, 96, 97, 98, 89, 99]]


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
    matrix_IDS = Puzzle.Iterative_Depth_Search(copy.deepcopy(matrix),15)
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
