# -*- coding: utf-8 -*-
#modulo nodos
#clase base Node
class Node:
	#constructor  resive el elemento que guardara
	def __init__(self, element):
		self._element = element
		self._adjacencies = [] #inicializa la lista de adyacencias
	#geters
	def element(self):
		return self._element
	def adjacencies(self):
		return self._adjacencies
	#seters
	def set_element(self, new_element):
		self._element= new_element
	#to string en java
	def __str__(self):
		return str(self.element())
	# cuando es llamado el to string en una lista
	def __repr__(self):
	    return str(self)
	#comparar con otro objeto equals en java
	def __eq__(self, other):
		return self.element() == other.element()
	#añadir adyacencia, resive cualquier numero de parametros y los guarda en la tupla 'adjacency'
	def add_adjacency(self,*adjacency):
		if self.validate_adjacency(*adjacency): #pregunta si es valida la adyacencia
			#si es cierto construlle la adyacencia y la añade a la lista de adyacencias
			self.adjacencies().append(self.build_adjacency(*adjacency))
			return True
		#si no es cierto retorna false, no se realizo la adicion
		return False
	# validar adyacencia, lo unico que tiene que hacer es preguntar si no  existe la adyacencia, en ese caso es valida
	def validate_adjacency(self,*adjacency):
		return not self.exist_adjacency(*adjacency)
# clase nodo dirigido ponderado, extiende de Node
class DirectedWeightedNode(Node):
	#eliminar adyacencia recive el nodo adyacente, y la ponderacion
	def del_adjacency(self,adjacent_node,weigth):
		try:
			#crea una tupla con los valores de la adyacencia a eliminar y le dice a la lista de asyacencias que la elimine
			#esta eecutara el metodo __Eq__ para cada para cada adyacencia de la lista mandadole la asyacencia que se acabo de construir
			# las adyacencias son iguales la elimina
			self.adjacencies().remove((adjacent_node,weigth))
			#si no existe se lanza un error
			return True
		except:
			#el error es capturado y se retorna falso
			return False # no se elimino nada, no existia la adyacencia
	# dice si existe una adyacenica
	def exist_adjacency(self, other_node,weigth):
		# construye la adyacencia y pregunta si esta en las adyacencias del nodo, hace lo mismo que en del_adjacency
		return (other_node,weigth)  in self.adjacencies()
	#construye una adyacencia para un nodo ponderado
	#resive cualquier cantidad de parametros en una tupla
	# como siempre se va a llamar con los parametros: adjacent_node, weight adjacency va a ser: (adjacent_node,weight)
	def build_adjacency(self,*adjacency):
		return adjacency
