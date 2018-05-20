# -*- coding: utf-8 -*-
from nodes import *
class Graph:
	#Constructor
	def __init__(self):
		self._nodes = []
	#geters
	def nodes(self):
		return self._nodes
	#aderir nodo, resive cualquier canidad de argumentos,
	#esto se hace porque es una clase base, y las clase que heredan pueden decir que un nodo tiene mas atributos
	def add_node(self, *nodo):
		
		new_node = self.create_node(*nodo) # se crea un nuevo nodo
		if new_node in self.nodes(): # si el nodo esta en la lista de nodos se retorna el error
			raise Exception("Node %s already in graph" %  element)
		else:
			# si no esta se añade a la lista de nodos
			self.nodes().append (new_node)
	#eliminar nodo; resive el elemento que tiene ese nodo
	def del_node(self, element):
		try:
			#crea un nodo igual al que se va a eliminar, y se llama el elemento remove de nodos
			#ejecutando el metodo __eq__ si un nodo dde la lista es igual al que se envio por parametro, este elimina de la lista
			#sino retorna un error
			self.nodes().remove(self.create_node(element))
		except:
			#el error es capturado y reinterpretado
			raise Exception("Node %s not in graph" % element)
	#metodo privado que retorna un nodo con el elemento
	def _get_node(self, element):
		for node in	self._nodes:
			if node.element() == element:
				return node
		raise Exception("Node %s not in graph" % element)
	# añadir arista resive cualquier numero de parametros en una tupla, los cuales forman  una arista
	def add_edge(self, *edge):
		# toda arista siemper debe tener un elemento inicial y otro final
		init_element,fnl_element = edge[0],edge[1] # se obtienen en variables
		init_node = self._get_node(init_element) # se obtiene el nodo relacionado al priemr elemento
		fnl_node = self._get_node(fnl_element)# se obtiene el nodo relacioneado con el segundo elemento
		#y que la tupla es inmuytable genero una lista a partir de ella y la guardo en adjacency
		adjacency = list(edge)
		#elimino el primer elemento
		del adjacency[0]
		#cambio el ultimo elemento por el nodo final
		adjacency[0] = fnl_node
		#se le dice al nodo inicial que añada una adyacencia
		success = init_node.add_adjacency(*adjacency) #retorna true si se añadio
		if not success: # si no se añadio se lanza el error
			raise Exception("Edge {0} already in graph".format(edge))
	# eliminar arista resive la arista en una tupla
	def del_edge(self, *edge):
		#se hace lomismo que en añadir arista
		init_element,fnl_element = edge[0],edge[1]
		init_node = self._get_node(init_element)
		fnl_node = self._get_node(fnl_element)
		
		adjacency = list(edge)
		del adjacency[0]
		adjacency[0] = fnl_node
		success = init_node.del_adjacency(*adjacency)
		if not success:
			raise Exception("Edge {0} not in graph".format(edge))
	def add_nodes(self, nodes):
		# un metodo que resive una lista con los elementos de varios  nodos a añadir
		for node in nodes:
			#pregunta que si el elemento es una tupla
			if isinstance(node,tuple) :
				#se es asi se descompone 
				self.add_node(*node)
			else:
				# sino se envia normal
				self.add_node(node)
	#añadir varias aristas
	def add_edges(self,edges):
		for edge in edges:
			#un eje siempre va a ser una tupla asi que siempre se descompone
			self.add_edge(*edge)
#clase nodo dirigido exstiende de Graph
class DirectedWeightedGraph(Graph):
	#crear nodo, solo resive el elemento que tendra el nodo
	def create_node(self,element):
		#develve un nodo dirigido ponderado
		return DirectedWeightedNode(element)
	#geter de ejes, retorna los elementos
	def edges(self):
		edges = []
		for node in self.nodes():
			for adjacency,weigth in node.adjacencies():
				edges.append((node,adjacency,weigth))
		return edges
	
