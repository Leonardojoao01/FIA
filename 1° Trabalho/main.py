# -*- encoding:utf-8 -*-
#!/usr/bin/python

from Puzzle_slider import Puzzle_slider
import time
import copy
import resource
import sys

Puzzle = Puzzle_slider(3)

#matrix = [[0, 6, 2,], [1, 3, 8,], [4, 7, 5,]]
#matrix = [[1, 2, 3,], [4, 5, 6,], [0, 7, 8,]]
#matrix = [[1, 2, 3,], [4, 5, 0,], [7, 8, 6,]]
#matrix = [[8, 1, 3,], [4, 0, 2,], [7, 6, 5,]]

#matrix = Puzzle.matrix_reorder_all(10, Puzzle.get_matrix_origin())
#print(matrix)

matrix = [[1, 6, 2], [5, 3, 8], [4, 7, 0]]


#Puzzle = Puzzle_slider(3)

#print(sys.argv[1])

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
