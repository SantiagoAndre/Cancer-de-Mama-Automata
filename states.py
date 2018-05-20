# -*- coding: utf-8 -*-
from nodes import DirectedWeightedNode,Node
# estado de un autamata celular, hereda de nodo dirigido ponderado
class CellularState(DirectedWeightedNode):
	#constructor      nombre, color(opcional)
	def __init__(self,name, color = None):
		self._color = color
		# se llama el constructor de la clase base
		DirectedWeightedNode.__init__(self,name)
	#geter color
	def color(self):
		return self._color
	#setter color
	def set_color(self,new_color):
		self._color = new_color
	#metodo importante de esta clase, obtener el nnuevo estado de una celula partiendo de ella misma y siguiendo un camiño
	def get_new_state(self, path): #get the state that is reached from this node, following the $path
		if not path: # path es vacio
			return self #this en java
		for (next_state,value) in self.adjacencies(): # l lista adjacencies tiene duplas (adjacency, weight) = (adyacencia,ponderacion)
			if path[0]  == value:
				return  next_state.get_new_state(path[1:])
		return None
