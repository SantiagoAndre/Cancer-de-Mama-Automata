# -*- coding: utf-8 -*-
from time import sleep,time
from random import randint as rand
from logic.cells import CellMaker


class Neighborhood:
	#constructor
	def __init__(self,porcentaje_infeccion,rows=50,columns=50):
		self.init_generation(rows, columns,porcentaje_infeccion)
		self._dimencions = (rows,columns)
		self._generation = 0
	#geterts
	def automata(self):
		return self._automata
	def cells(self):
		return self._cells
	def dimencions(self):
		return self._dimencions
	def num_of_cells(self):
		return self.dimencions()[0]*self.dimencions()[1]
	def generation(self):
		return self._generation
	def cell_maker(self):
		return self._cell_maker
	def states_cell(self):
		return self.cell_maker().all_states()
	def state_neighborhood(self): #Cual es el estado del barrio
		porcentaje_infeccion  =self.porcentaje_infeccion_total()
		return porcentaje_infeccion,self.cell_maker().state_with(porcentaje_infeccion)
	def porcentaje_infeccion_total(self):
		return self._infeccion/self.num_of_cells()

	#crea la primera generacion
	def init_generation(self,rows, columns, pcj_celulas_infectadas = 95):
		## creador de celulas
		self._cell_maker = CellMaker()
		#obtengo todos los posibles estados de las celulas
		all_states = self.cell_maker().all_states()
		#el estado mas sano
		FASE0 = all_states[0]
		#el numero del maximo estado
		pos_max_state = len(all_states)-1
		#obtengo el estado minimo
		FASE0 = all_states[0] #estado sano
		#numero de celulas a infectar
		celulas_a_infectar = int(rows*columns*(pcj_celulas_infectadas/100))

		#genero todas las celulas
		cells = [[self.cell_maker().create(FASE0) for _ in range(columns)]for _ in  range(rows)]

		infeccion = 0
		for i in range(celulas_a_infectar):
			#calculo la posicion de la celula a infectar
			r = rand(0,rows-1)
			c = rand(0,columns-1)
			cell = cells[r][c]
			if cell.state() != FASE0:
				i = i-1
				continue
			##Proceso de asignar el estado
			pos_nuevo_estado = rand (1,pos_max_state)
			nuevo_estado = all_states[pos_nuevo_estado]
			cell.set_state(nuevo_estado)
			infeccion = infeccion + nuevo_estado.element()
		self._cells = cells
		self._infeccion = infeccion

	def porcentaje_infeccion(self, i,j,max_infeccion):# que tan infectado esta el barrio de cada celula
		cells = self.cells()
		celula_central = cells[i][j]
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
				infeccion += cell.state().element()
		infeccion -= cells[i][j].state().element()
		vecinos =(b-a+1)*(d-c+1) - 1
		return infeccion/(vecinos)

	def next_generation(self): #con base a la anterior generacion la siguiente
		cells  = self.cells() #saca las celulas en una variable
		for i,row in enumerate(cells): #recorre toda la matriz obteniendo cada fila
			for j,cell in enumerate(row): #recorre toda la celula obteniendo cada celula
				porcentaje_infeccion = self.porcentaje_infeccion(i,j,cell.automata()._nodes[-1].element())
				self._infeccion += cell.evolucionar(porcentaje_infeccion)
				yield cell,i,j
		self._generation+= 1
