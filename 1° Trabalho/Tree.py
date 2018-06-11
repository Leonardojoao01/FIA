# -*- encoding:utf-8 -*-

class No:
	def __init__(self, data, level):
		self.father		= None
		self.data       = data
		self.leaf_one   = None
		self.leaf_two   = None
		self.leaf_three = None
		self.leaf_four  = None
		self.level		= level

	def get_data(self):
		return self.data

	def set_data(self, data):
		self.data = data

	def set_father(self, data):
		self.father = data

	def get_father(self):
		return self.father

	def get_level(self):
		return self.level

	def set_leaf(self, leaf):
		#self.leaf_one = leaf
		leaf_aux = self.verify_son_free()
		leaf_aux = leaf


	def get_leaf_one(self):
		return self.leaf_one

	def verify_son_free(self):
		leaf_aux = None
		if self.leaf_one == None:
			leaf_aux = self.leaf_one
		elif self.leaf_two == None:
			leaf_aux = self.leaf_two
		elif self.leaf_three == None:
			leaf_aux = self.leaf_three
		elif self.leaf_four == None:
			leaf_aux = self.leaf_four

		return leaf_aux

"""
class No:
	def __init__(self, data):
		self.data       = data;
		self.up_down    = None;
		self.down_up    = None;
		self.left_right = None;
		self.right_left = None;
"""
class Arvore(object):

	#def __init__(self, data):
	#	return No(data)		# Verificar se está funcionando

	#	1 = up_down; 	2 = down_up;	3 = left_right;		4 = right_left
	def insert(self, no, data, position):
		if no is None:
			no = No(data);
		else:
			if 1 == position:
				no.up_down = self.insert(no.up_down, data, position);
			elif 2 == position:
				no.down_up = self.insert(no.down_up, data, position);
			elif 3 == position:
				no.left_right = self.insert(no.left_right, data, position);
			elif 4 == position:
				no.right_left = self.insert(no.right_left, data, position);
  
		return no;

	def print_all_tree(self, no, cont):
		#global ImprimeArvore
		if no is None:
			return
		#ImprimeArvore += str(no.chave) + ', '
		print("Nivel", cont)
		print(no.data)
		self.print_all_tree(no.up_down, cont+1)
		self.print_all_tree(no.down_up, cont+1)
		self.print_all_tree(no.left_right, cont+1)
		self.print_all_tree(no.right_left, cont+1)


if __name__ == '__main__':

	no = No(10)
	tree = Arvore()
	tree.insert(no, 5, 1)
	tree.insert(no, 10, 2)
	tree.insert(no, 5, 1)


	tree.print_all_tree(no, 0)	

	"""

	matriz1 = [[ 2,2,2,],
              [ 2,2,2,],
              [ 1,1,0,]]

	matriz2 = [[ 2,2,2,],
              [ 2,2,0,],
              [ 1,1,2,]]

	arvore = insere_vet(arvore, matriz1, 1);"""
