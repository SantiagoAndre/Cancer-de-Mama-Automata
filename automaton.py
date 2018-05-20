# -*- coding: utf-8 -*-
from graphs import DirectedWeightedGraph
from states import *
#clase automata celular, extiende de grafo dirigido
class CellularAutomate(DirectedWeightedGraph):
	#constructor como la definicion formal de un automata, resive los estados, el afabeto y las transiciones
	# se decidio que no tubiera un estado inicial, y que no tueviera estados finales
	#ya que la filosofoia de este es estregar un nuevo estado, en vez de definir un lengiaje
	def __init__(self,states,alphabet,transitions):
		DirectedWeightedGraph.__init__(self)#constructor de la clase base
		self._alphabet = alphabet
		self.add_nodes(states)
		self.add_edges(transitions)
	#geter
	def alphabet(self):
		return self._alphabet
	#sobre escribe el metod crear nodo de la clase base
	def create_node(self,*node):
		#retorna un automata celular
		return CellularState(*node)
	#el metodo principal de esta clase, retorna el estado al que se llega partiendo de u estado, y sieguiendo un camino
	def get_new_state(self, start_state,path): #get the state that is reached from this node, following the $path
		new_state = start_state.get_new_state(path)
		if new_state is None:
				raise Exception("no se llega a ningun estado. partiendo de %s y siguiendo el camino %s."%(start_state,path))
		return new_state
