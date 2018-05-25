# -*- encoding:utf-8 -*-
#!/usr/bin/python

from Tree import No

tree_1 = No(10)
tree_2 = No(20)

tree_2.set_father(tree_1)

print(tree_1.get_father())

juca = tree_2.get_father()

print(juca.get_data())

#print(tree.get_data())