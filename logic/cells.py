from logic.automata.automaton import CellularAutomate
class CellMaker:

	def __init__(self):
		self._automata = self.init_automata()
	def automata(self):
		return self._automata
	def all_states(self):
		return self.automata()._nodes
	def num_states(self):
		return self._num_states
	def state_in(self,num_state):
		return self.automata()._nodes[num_state-1]
	def state_with(self,porcentaje_infeccion):
		posicion = round(porcentaje_infeccion*(self.num_states()-1)/100)
		return self.all_states()[posicion]
	def create(self,state):
		#state = self.state_with(porcentaje_infeccion)
		return Cell(self.automata(),state)
	def init_automata(self):
		from logic.utilities import read_ranges_file
		self._num_states, STATES = self.init_estados()
		T = []
		pivotes = read_ranges_file()
		for ei,_ in STATES:
			
			for (ef,_) in STATES:
				if ef<ei:
					continue
				pibote = pivotes.__next__()
				if pibote  == -1:
					break
				T.append((ei,ef,round(pibote)))
			if pibote != -1:
				pibote = pivotes.__next__()
		return CellularAutomate(STATES,(0,100),T) # guarda el automata en un atributo de  Neighborhood
	def init_estados(self):
		from logic.utilities import read_colors_file
		colors = read_colors_file()
		num_estados = len(colors)
		porcentaje_estado = 100/(num_estados-1)
		return num_estados,[(round(i*porcentaje_estado),color) for  i,color in enumerate(colors)]
class Cell:

	def __init__(self,automata , state):
		self._automata = automata
		self._state = state

	def automata(self):
		return self._automata
	def state(self):
		return self._state

	def set_state(self,new_state):
		self._state = new_state
	def evolucionar(self,porcentaje_infeccion):
		old_state = self.state()
		new_state = self.automata().get_new_state(self.state(),[porcentaje_infeccion])
		self.set_state(new_state)
		return new_state.element()- old_state.element()
