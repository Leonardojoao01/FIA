# -*- encoding:utf-8 -*-
#!/usr/bin/python

#import requests
import urllib.request
import sys
import random
import time 
import re
import copy
import time
from numba import jit
from Nodo import No

class boku(object):
    
    player = None
    plays = None
    host = "http://localhost:8080"
    #teste = No()

    def __init__(self):
        self.player = self.turn()
        self.teste = No()
        #return None

    def turn(self):             # Verifica o jogador
        resp = urllib.request.urlopen("%s/jogador" % self.host)
        player_turn = int(resp.read())
        return player_turn
    
    def board(self):
        resp = urllib.request.urlopen("%s/tabuleiro" % self.host)
        board = eval(resp.read())
        return board
    
    def movements(self):
        resp = urllib.request.urlopen("%s/movimentos" % self.host)
        movements = eval(resp.read())
        return movements

    def send_movement(self, movement):
        resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (self.host,self.player,movement[0],movement[1]))
        msg = eval(resp.read())
        return msg

    @jit
    def neighbors(self, board, column, line):
        l = []

        if line > 1:
            l.append((column, line-1))  # up
        else:
            l.append(None)

        if (column < 6 or line > 1) and (column < len(board)):
            if column >= 6:
                l.append((column+1, line-1))  # upper right
            else:
                l.append((column+1, line))  # upper right
        else:
            l.append(None)
        if (column > 6 or line > 1) and (column > 1):
            if column > 6:
                l.append((column-1, line))  # upper left
            else:
                l.append((column-1, line-1))  # upper left
        else:
            l.append(None)

        if line < len(board[column-1]):
            l.append((column, line+1))  # down
        else:
            l.append(None)

        if (column < 6 or line < len(board[column-1])) and column < len(board):
            if column < 6:
                l.append((column+1, line+1))  # down right
            else:
                l.append((column+1, line))  # down right
        else:
            l.append(None)

        if (column > 6 or line < len(board[column-1])) and column > 1:
            if column > 6:
                l.append((column-1, line+1))  # down left
            else:
                l.append((column-1, line))  # down left
        else:
            l.append(None)

        return l

    @jit
    def is_final_state(self, board):
        # test vertical
        for column in range(len(board)):
            s = ""
            for line in range(len(board[column])):
                state = board[column][line]
                s += str(state)
                if "11111" in s:
                    #print("Ganhou")
                    return 1
                if "22222" in s:
                    print("Perdeu")
                    return 2

        # test upward diagonals
        diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
        for column_0, line_0 in diags:
            s = ""
            coords = (column_0, line_0)
            while coords != None:
                column = coords[0]
                line = coords[1]
                state = board[column-1][line-1]
                s += str(state)
                if "11111" in s:
                    #print("Ganhou")
                    return 1
                if "22222" in s:
                    print("Perdeu")
                    return 2
                coords = self.neighbors(board, column, line)[1]

        # test downward diagonals
        diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                 (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
        for column_0, line_0 in diags:
            s = ""
            coords = (column_0, line_0)
            while coords != None:
                column = coords[0]
                line = coords[1]
                state = board[column-1][line-1]
                s += str(state)
                if "11" in s:
                    #print("Ganhou")
                    return 1
                if "22222" in s:
                    print("Perdeu")
                    return 2
                coords = self.neighbors(board, column, line)[4]

        return None

    def player_random(self):
        
        done = False
        while not done:

            if self.turn() == self.player:      # Se for a vez do jogador
                movements = self.movements()
                movement = random.choice(movements)
                msg = self.send_movement(movement)
                
                if msg[0]==0:
                    print("I win")
                    done = True


            elif self.turn() == 0:
                print("I lose")
                done = True


            time.sleep(1)
        return None


    def leaf_generating(self, father, board, level):   # Gera os filhos de um unico pai
        x = y = counter = 0         # Arrumar esse valor do level

        x_size_table = len(board)           # Tamanho em relação ao X da tabela
        while x < x_size_table:
            y_size_table = len(board[x])    # Tamanho em relação do Y da tabela, realizado a cada iteração pois o tamamnho altera    
            while y < y_size_table:
                if board[x][y] == 0:
                    aux_board = copy.deepcopy(board)       # Utilizado p/ criar uma copia da TABELA, pois terá um valor alterado e armazedo
                    aux_board[x][y] = 1
                    #=====Etapa de criação dos filhos e atribuição ao pai=====
                    leaf = No()
                    leaf.set_data([y,x], aux_board, level)
                    father.set_leaf(leaf)
                    #=========================================================
                y+=1
            y=0
            x+=1

        # Aqui que deve ser feita o poda ALFA/BETA ou no WHILE
        # Retorna a lista de filhos para o pai passado
        return father.get_leaf()

    # , board):    # Gera os filhos de todos os pais, utilizando o metodo superior
    def leafs_generating(self, father, depth):
        
        x = level = 0
        list_aux_father = []
        list_aux_leaf = []
        #print(type(father))
        #print(level)
        while level < depth:        # Verificar quantas vezes está entrando, 
                                    # pois FATHER é passado por referencia, pode estar entrando mais vezes
            size_list_father = len(father)
            while x < size_list_father:
                father_aux = father.pop(0)
                board = father_aux.get_board()
                #list_aux_leaf = self.leaf_generating(father[x], board, level) 
                #list_aux_father.extend(list_aux_leaf)
                father.extend(self.leaf_generating(father_aux, board, level))
                x+=1
            #father = copy.deepcopy(list_aux_father)
            #father = list_aux_leaf
            #print(type(father))
            x=0
            level+=1

    def player_nodo_tree(self):

        movements = self.movements()
        number_movements = len(movements)

        if number_movements > 2:        # Então não cai naquele caso de tirar a peça do adversário
            board = self.board()
            self.teste.set_board(board)
            self.leafs_generating([self.teste], 3)

            list_father = self.teste.get_leaf()
            leaf = list_father[2].get_leaf()

        else:                           # Cai no caso de tirar a peça do adversário
            return None

    #================================================================
    #============================ MODO 2 ============================
    @jit
    def leaf_generating_matrix(self, board, level=None):
        x = y = counter = 0         # Arrumar esse valor do level
        list_leaf = []
        x_size_table = len(board)           # Tamanho em relação ao X da tabela
        while x < x_size_table:
            # Tamanho em relação do Y da tabela, realizado a cada iteração pois o tamamnho altera
            y_size_table = len(board[x])
            while y < y_size_table:
                if board[x][y] == 0:
                    # Utilizado p/ criar uma copia da TABELA, pois terá um valor alterado e armazedo
                    aux_board = copy.deepcopy(board)
                    #=========================================================
                    if level % 2 == 0:
                        aux_board[x][y] = 1
                    else:
                        aux_board[x][y] = 2
                    #=========================================================



                    
                    #=====Etapa de criação dos filhos=====
                    leaf = No()
                    leaf.set_data([y, x], aux_board)#, level)
                    #father.set_leaf(leaf)
                    list_leaf.append(leaf)
                    #=========================================================
                    self.is_final_state(aux_board)
                    #=========================================================
                y += 1
            y = 0
            x += 1
        return list_leaf

    @jit
    def leafs_generating_matrix(self, father, depth):
        x = level = 0
        #list_aux_father = []
        #list_aux_leaf = []
        #print(type(father))
        #print(level)
        while level < depth:        # Verificar quantas vezes está entrando,
                                    # pois FATHER é passado por referencia, pode estar entrando mais vezes
            size_list_father = len(father)
            while x < size_list_father:
                #board = father[x].get_board()
                #father_aux = father.pop(0)
                board = father.pop(0).get_board()
                #print(board)
                #print("")

                #print(type(self.leaf_generating_matrix(father[x], board, level)))
                #list_aux_leaf.extend(self.leaf_generating_matrix(board, level))
                father.extend(self.leaf_generating_matrix(board, level))
                x += 1
            print(x)
        
            x = 0
            level += 1
        
        
            

    def player_nodo_matrix(self):
        
        movements = self.movements()
        number_movements = len(movements)

        if number_movements > 2:
            board = self.board()
            self.teste.set_board(board)
            self.leafs_generating_matrix([self.teste], 3)

            
        else:
            
            return None

        #leafs = self.teste.get_leaf()
        #leaf = leafs[0].get_board()
        #print(leaf)

    #================================================================
    #============================ MODO 3 ============================

    def leaf_generating_matrix2(self, board, level=None):
        x = y = counter = 0         # Arrumar esse valor do level
        list_leaf = []
        x_size_table = len(board)           # Tamanho em relação ao X da tabela
        while x < x_size_table:
            # Tamanho em relação do Y da tabela, realizado a cada iteração pois o tamamnho altera
            y_size_table = len(board[x])
            while y < y_size_table:
                if board[x][y] == 0:
                    # Utilizado p/ criar uma copia da TABELA, pois terá um valor alterado e armazedo
                    aux_board = copy.deepcopy(board)
                    aux_board[x][y] = 1
                    #=====Etapa de criação dos filhos=====
                    #leaf = No()
                    #leaf.set_data([y, x], aux_board)  # , level)
                    #father.set_leaf(leaf)
                    list_leaf.append(aux_board)
                    #=========================================================
                y += 1
            y = 0
            x += 1
        return list_leaf

    def leafs_generating_matrix2(self, father, depth):
        x = level = 0
        #list_aux_father = []
        #list_aux_leaf = []
        #print(type(father))
        #print(level)
        while level < depth:        # Verificar quantas vezes está entrando,
                                    # pois FATHER é passado por referencia, pode estar entrando mais vezes
            size_list_father = len(father)
            while x < size_list_father:
                #print("ENTROU")
                father.extend(self.leaf_generating_matrix2(father.pop(0)))  # , level))
                x += 1
            print(x)

            x = 0
            level += 1

    def player_nodo_matrix2(self):

        movements = self.movements()
        number_movements = len(movements)

        if number_movements > 2:
            board = self.board()
            #self.teste.set_board(board)
            self.leafs_generating_matrix2([board], 3)

        else:

            return None
    


play = boku()

t0 = time.time()
#play.player_nodo_tree()
play.player_nodo_matrix()
#play.player_nodo_matrix2()
t1 = time.time()
print(str(t1-t0))
