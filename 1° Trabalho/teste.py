# -*- encoding:utf-8 -*-
#!/usr/bin/python

from Tree import No


# def __init__(self, data, level):
#     	self.father		= None
# 		self.data       = data
# 		self.leaf_one   = None
# 		self.leaf_two   = None
# 		self.leaf_three = None
# 		self.leaf_four  = None
# 		self.level		= level

tree_1 = No(10)     # Pai
tree_2 = No(20)     # Filho

tree_2.set_father(tree_1)

print(tree_1.get_father())

juca = tree_2.get_father()

print(juca.get_data())

#print(tree.get_data())