# -*- encoding:utf-8 -*-
#!/usr/bin/python

from Puzzle_slider import Puzzle_slider
import time
import copy
import resource


matrix = [[0, 6, 2,], [1, 3, 8,], [4, 7, 5,]]

Puzzle = Puzzle_slider(3)

#print("DFS:")
t0 = time.time()
matrix_DFS = Puzzle.Breadth_First_Search(copy.deepcopy(matrix))
t1 = time.time()
#print ("Total time running: %s seconds" %(str(t1-t0)))
print(str(t1-t0))
#print("Máximo uso de memória: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f') + " MB")
print(format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.2f'))