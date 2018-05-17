# -*- encoding:utf-8 -*-
from __future__ import print_function

class No:
    def __init__(self, dado):
        self.dado = dado
        self.esq = None
        self.dir = None
         

class Arvore:
    def __init__(self):
        self.raiz = None
    def pegarRaiz(self):
        return self.raiz

    def inserir(self, val):
        if self.raiz == None:
            self.raiz = No(val)
        else:
            self._inserir(val, self.raiz)

    """def _inserir(self, val, node):
        if val < node.dado:
            if(node.esq != None):
                self._inserir(val, node.esq)
                node.esq.pai = node
            else:
                node.esq = No(val)
        else:
            if node.dir != None:
                self._inserir(val, node.dir)
                node.dir.pai = node
            else:
                node.dir = No(val)"""

    def _inserir(self, val, node):
        if val < node.dado:
            if(node.esq != None):
                self._inserir(val, node.esq)
            else:
                node.esq = No(val)
        else:
            if node.dir != None:
                self._inserir(val, node.dir)
            else:
                node.dir(val)

    def traverse(self, visit):

        """visit(self.raiz.dado)
        if self.raiz.esq is not None:
            print("existe ESQ")
            self.raiz.traverse(visit)

        if self.raiz.dir is not None:
            print("existe DIR")
            print(self.raiz.dir.dado)
        #    self.dir.traverse(visit)"""
        visit(self.raiz.dado)
        if self.raiz.esq is not None:
            #print("existe ESQ")
            self.raiz.esq.pai.traverse(visit)
 
if __name__ == '__main__':

    T = Arvore()
    T.inserir(15)
    T.inserir(9)
    T.inserir(5)
    T.inserir(12)
    T.inserir(20)
    #T.traverse(print)
    #T.Altura()