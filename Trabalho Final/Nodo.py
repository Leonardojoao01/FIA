# -*- encoding:utf-8 -*-

class No:
    def __init__(self):
        #self.father		= None
        self.movement   = None
        #self.leaf       = []
        self.board      = []
        #self.level		= None

    def set_data(self, data, board,level=None):
        self.movement = data
        self.board     = board
        #self.level    = level
    
    def get_data(self):
        return self.movement

    def set_board(self, data):
        self.board = data

    def get_board(self):
        return self.board

    def set_father(self, data):
        self.father = data

    def get_father(self):
        return self.father

    def get_level(self):
        return self.level

    def set_leaf(self, data):
        self.leaf.append(data)

    def get_leaf(self):
        return self.leaf

    def print_leaf(self):
        print(self.leaf)


