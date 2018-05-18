# -*- encoding:utf-8 -*-
from __future__ import print_function


class BSTNode(object):

    def __init__(self, key, value=None, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def get(self, key):
        if key < self.key:
            return self.left.get(key) if self.left else None
        elif key > self.key:
            return self.right.get(key) if self.right else None
        else:
            return self


    def add(self, node):
        if node.value < self.value:
            if self.left is None:
                self.left = node
            else:
                self.left.add(node)
        else:
            if self.right is None:
                self.right = node
            else:
                self.right.add(node)

    # Direção do movimento
    # 1 = SI; 2 = IS; 3 = ED; 4 = DE
    #def add(self, node, dir):
    #    if (1 == dir):
    #        if self.left is None:
    #            self.left = node
    #        else:
    #            self.left.add(node)
    #    else:
    #        if self.right is None:
    #            self.right = node
    #        else:
    #            self.right.add(node) 

    def traverse(self, visit, order='pre'):
        """Percorre a árvore na ordem fornecida como parâmetro (pre, pos ou in) 
           visitando os nós com a função visit() recebida como parâmetro.
        """
        if order == 'pre':
            visit(self.key)
        if self.left is not None:
            self.left.traverse(visit, order)
        if order == 'in':
            visit(self.key)
        if self.right is not None:
            self.right.traverse(visit, order)
        if order == 'post':
            visit(self.key)



    def print(self, order='pre'):
        self.traverse(print, order)


if __name__ == '__main__':

    matriz1 = [[ 2,2,2,],
              [ 2,2,2,],
              [ 1,1,0,]]

    matriz2 = [[ 2,2,2,],
              [ 2,2,0,],
              [ 1,1,2,]]


    tree = BSTNode('m')
    tree.add('a')

    tree.print()

    #print(matriz)
