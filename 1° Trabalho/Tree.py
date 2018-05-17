# -*- encoding:utf-8 -*-


class No:
	def __init__(self, data):
		self.data       = data;
		self.up_down    = None;
		self.down_up    = None;
		self.left_right = None;
		self.right_left = None;

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
