# -*- coding: utf-8 -*-
from time import sleep,time
from random import randint as rand
from logic.automata.automaton import CellularAutomate


class Neighborhood:
	#constructor
	def __init__(self,porcentaje_infeccion,rows=50,columns=50):
		self.init_automata()
		self.init_generation(rows, columns,porcentaje_infeccion)
		self._dimencions = (rows,columns)
	#geterts
	def automata(self):
		return self._automata
	def cells(self):
		return self._cells
	def cell_large(self):
		return self._cell_large
	def dimencions(self):
		return self._dimencions
	def porcentaje_infeccion_total(self):
		return self._infeccion/(self.dimencions()[0]*self.dimencions()[1])
	#inicializa el automata, este tiene las reglas del siguiente destado de una celula de acuerdo a las condiciones en  las que se encuentra
	def init_automata(self):
		#colors = [(224,242,241),(128,203,196),(0,150,136),(0,77,64)]
		#colors = [(224,242,241),(0,77,64),(0,150,136),(128,203,196)]
		num_estados, STATES = self.init_estados()
		T = []
		cte = 100/num_estados
		for ei,_ in STATES:
			pibote = 0
			for i,(ef,_) in enumerate(STATES):
				pibote +=cte
				if ef<ei:
					continue
				T.append((ei,ef,round(pibote)))
		self._automata = CellularAutomate(STATES,(0,100),T) # guarda el automata en un atributo de  Neighborhood
	def init_estados(self):
		colors =  self.read_colors_file()
		num_estados = len(colors)
		porcentaje_estado = 100/(num_estados-1)
		return num_estados,[(round(i*porcentaje_estado),color) for  i,color in enumerate(colors)]
	#genera la primera generacion
	def init_generation(self,rows, columns, porcentaje = 95):
		FASE0 = self.automata()._nodes[0] #estado sano
		self._infeccion = 0
		cells = [[FASE0 for _ in range(columns)] for _ in  range(rows)]
		if porcentaje == 0:
			self._cells = cells
			return
		infectados = int(rows*columns*(porcentaje/100))
		max_pos_estado = len(self.automata()._nodes)-1
		for i in range(infectados):
			#celulas aleatorias en la placa de celulas
			r = rand(0,rows-1)
			c = rand(0,columns-1)
			if cells[r][c] != FASE0:
				i = i-1
				continue
			##Proceso de asignar el estado
			pos_nuevo_estado = rand (1,max_pos_estado)
			nuevo_estado = self.automata()._nodes[pos_nuevo_estado]
			cells[r][c] = nuevo_estado
			self._infeccion = self._infeccion + nuevo_estado.element()
		self._cells = cells
	def read_colors_file(self):
		file = open("resources/files/colors_file.txt")
		colors = []
		color = file.readline()
		while color:
			if color[-1] is "\n":
				color = color[:-1]
			if color[0] is "#":
				color = Neighborhood.hex_to_rgb(color[1:])
			else:
				color = eval(color)
			colors.append(color)
			color = file.readline()
		file.close()
		return colors
	def porcentaje_infeccion(self, i,j,max_infeccion):# que tan infectado esta el barrio de cada celula
		cells = self.cells()
		prof = 1
		max_i,max_j = len(cells)-1,len(cells[0])-1
		if i-prof<=0:
			a = 0
		else:
			a = i-prof
		if i + prof >= max_i:
			b = max_i
		else:
			b = i + prof
		if j-prof<=0:
			c = 0
		else:
			c = j-prof
		if j + prof >= max_j:
			d = max_j
		else:
			d = j + prof
		infeccion = 0
		for it,row in enumerate(cells[a:(b+1)]):
			for jt,cell in enumerate(row[c:(d+1)]):
				infeccion += cell.element()
		infeccion -= cells[i][j].element()
		vecinos =(b-a+1)*(d-c+1) - 1
		return infeccion/(vecinos)
	def next_generation(self): #con base a la anterior generacion(anterior fila) crea la siguiente
		cells  = self.cells() #saca las celulas en una variable
		for i,row in enumerate(cells): #recorre la ultima fila, obteniendo la posicion de cada columna y la celula
			for j,cell in enumerate(row):
				porcentaje_infeccion = self.porcentaje_infeccion(i,j,self.automata()._nodes[-1].element())
				new_state = self.automata().get_new_state(cell,[porcentaje_infeccion])
				self._infeccion = self._infeccion +new_state.element()-cell.element()
				cells[i][j] = new_state
				yield cell,i,j
	#nada que ve con la clase
	def hex_to_rgb(hex):
		#hex = hex.lstrip('#')
		hlen = len(hex)
		return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))