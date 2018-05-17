class No:
	def __init__(self, chave):
		self.chave    = chave;
		self.esquerda = None;
		self.direita  = None;

class Arvore(object):

	def insere(self, no, chave):
		if no is None:
			no = No(chave);
		else:
			if chave < no.chave:
				no.esquerda = self.insere(no.esquerda, chave);   
			else:
				no.direita  = self.insere(no.direita, chave);  
		return no;

	def preOrdem(self, no):
		#global ImprimeArvore
		if no is None:
			return
		#ImprimeArvore += str(no.chave) + ', '
		print(no.chave)
		self.preOrdem(no.esquerda)
		self.preOrdem(no.direita)


def insere_vet(no, chave, pos):
	if no is None:
		no = Arvore(chave);
	else:
		if 1 == pos:
			no.esquerda = insere_vet(no.esquerda, chave, pos);   
		else:
			no.direita  = insere_vet(no.direita, chave, pos);  
	return no;


if __name__ == '__main__':

	no = No(10)
	tree = Arvore()
	tree.insere(no, 5)
	tree.insere(no, 10)

	#print(Arvore)

	tree.preOrdem(no)	

	#teste = Arvore(10)
	#teste.insere(5, 1)

	#teste.imprimir(teste)



	"""arvore = Arvore(3); # Cria arvore (raiz)
# Insere varios valores na arvore
	arvore = insere_vet(arvore, 2, 1);
	arvore = insere_vet(arvore, 1, 1);
	arvore = insere_vet(arvore, 4, 1);
	arvore = insere_vet(arvore, 6, 1);
	arvore = insere_vet(arvore, 8, 1);
	arvore = insere_vet(arvore, 5, 1);
	arvore = insere_vet(arvore, 7, 1);
	arvore = insere_vet(arvore, 0, 1);

	ImprimeArvore = ""
	preOrdem(arvore)
	print "PreOrdem: " + ImprimeArvore + "\n"

	matriz1 = [[ 2,2,2,],
              [ 2,2,2,],
              [ 1,1,0,]]

	matriz2 = [[ 2,2,2,],
              [ 2,2,0,],
              [ 1,1,2,]]

	arvore = insere_vet(arvore, matriz1, 1);"""
