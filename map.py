# -*- coding: utf-8 -*-
from time import sleep
from random import randint as rand
from automaton import CellularAutomate
#imports interface
import pygame,sys
from pygame.locals import *

class Neighborhood:
	#constructor
	def __init__(self,porcentaje_infeccion,rows=50,columns=50):
		self._calculate_dimencions(600,rows,columns)
		self.init_interface()
		self.init_automata()
		self.init_generation(rows, columns,porcentaje_infeccion)
	#geterts
	def automata(self):
		return self._automata
	def cells(self):
		return self._cells
	def cell_large(self):
		return self._cell_large
	def dimencions(self):
		return self._dimencions
	def display(self):
		return self._display
	#calcula las dimenciones del display y el tamaño de cada celula con base al numero de filas y columnas y el maximo largo del display, cada celula es un cuadrado
	def _calculate_dimencions(self,panel_large,rows,columns):
		self._cell_large = panel_large / max(rows,columns)
		width = self._cell_large*columns
		high = self._cell_large*rows
		self._dimencions= high,width
	#metodo principal, aqui se atrapan todos los eventos, se llama al metodo next_generation para que se vaya generando y dibujando cada fila, para luego
	#actualizar el display
	def start(self, generations = 100):

		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			self.next_generation()
			pygame.display.update()#actualizar el diaplay
			sleep(1)
	#inicializa el automata, este tiene las reglas del siguiente destado de una celula de acuerdo a las condiciones en  las que se encuentra
	def init_automata(self):
		#dos colores
		white = (125,125,125)

		cfase3=  (0,77,64)
		cfase2 = (0,150,136)
		cfase1 = (128,203,196)
		cfase0 = (224,242,241)
		#dos estados
		FASE0 = 0 #vivo
		FASE1 = 1 #vivo
		FASE2 = 2 #vivo
		FASE3 = 3 #vivo
		#S = [(LIVE,white),(DEAD,black)] #se guardan en un vector
		S = [(FASE0,cfase0),(FASE1,cfase1),(FASE2,cfase2),(FASE3,cfase3)] #se guardan en un vector
		alphabet = [0,1,2,3] # un alfabeto
		#T = [(LIVE,LIVE,8),(LIVE,DEAD,7),(LIVE,DEAD,6),(DEAD,DEAD,5),(DEAD,LIVE,4),(LIVE,LIVE,3),(LIVE,LIVE,2),(DEAD,LIVE,1),(DEAD,DEAD,0)] # las transiciones
		T=     [(FASE0,FASE0,0),(FASE0,FASE1,1),(FASE0,FASE2,2),(FASE0,FASE3,3)]
		T= T + [(FASE1,FASE1,0),(FASE1,FASE1,1),(FASE1,FASE2,2),(FASE1,FASE3,3)]
		T =T + [(FASE2,FASE2,0),(FASE2,FASE2,1),(FASE2,FASE2,2),(FASE2,FASE3,3)]
		T =T + [(FASE3,FASE3,0),(FASE3,FASE3,1),(FASE3,FASE3,2),(FASE3,FASE3,3)]
		self._automata = CellularAutomate(S,alphabet,T) # guarda el automata en un atributo de  Neighborhood
	def init_automata0(self):
		#dos colores
		white = (125,125,125)
		black = (0,0,0)
		#dos estados
		LIVE = 1 #vivo
		DEAD = 0 #muerto
		#S = [(LIVE,white),(DEAD,black)] #se guardan en un vector
		S = [(LIVE,white),(DEAD,black)] #se guardan en un vector
		alphabet = [0,1] # un alfabeto
		T = [(LIVE,DEAD,1),(LIVE,LIVE,0),(DEAD,DEAD,0),(DEAD,DEAD,1)] # las transiciones
		self._automata = CellularAutomate(S,alphabet,T) # guarda el automata en un atributo de  Neighborhood

		#genera la primera generacion
	def init_generation(self,rows, columns, porcentaje = 95):
		FASE0 = self.automata()._nodes[0] #estado sano
		FASE1 = self.automata()._nodes[1] #state sano intermedio
		FASE2 = self.automata()._nodes[2] #estado  enferme intermedio
		FASE3 = self.automata()._nodes[3] #estado murido

		cells = [[FASE0 for _ in range(columns)] for _ in  range(rows)]
		if porcentaje == 0:
			self._cells = cells
			return
		infectados = int(rows*columns*(porcentaje/100))
		for i in range(infectados):
			#celulas aleatorias en la placa de celulas
			r = rand(0,rows-1)
			c = rand(0,columns-1)
			if cells[r][c] != FASE0:
				i = i-1
				continue
			##Proceso de asignar el estado
			nuevo_estado = rand (1,3)
			cells[r][c] = self.automata()._get_node(nuevo_estado)
			#for _ in  range(rows):
			#	if(rand(0,1) == 0):
			#	 	row.append(SLIVE)
			#	else:
			#		row.append(SDEAD)
			#self._cells.append(row)
			self._cells = cells
		#self._cells.append([(SLIVE if j in(0,2,3,10,8,7) else SDEAD)  for _ in range(columns/10) for j in range(10)] )

	# inicializa la interfaz
	def init_interface(self):
		pygame.init() #se llama el init de pygame
		self._display = pygame.display.set_mode((int(self.dimencions()[0]),int(self.dimencions()[1]))) #se obtiene el display, entregando una dupla = (ancho, alto) con las dimenciones de este
		pygame.display.set_caption("Cellular Automata") #se coloca el nombre de la pantalla
		pygame.display.update() # se actualiza el display
	#dibuja una celula, recibe como parametro el estado de la celula, y la posicion en la matriz
	def draw_cell(self,state_cell,row,column):
		# se  transforma la posicion en la matriz a la posicion en el display(pantalla)
		posy = self.cell_large()*row
		posx = self.cell_large()*column
		# se le dice a pygame q ue dibuje un rectangulo
		pygame.draw.rect(self.display(),state_cell.color(),(posx,posy,self.cell_large(),self.cell_large()))
		#                     display   , color           ,(posx,posy, largo            , ancho)
	def porcentaje_infeccion(self, i,j,max_infeccion):# que tan infectado esta el barrio de cada celula
		cells = self.cells()
		infeccion = 0
		vecinos = 0
		#numero de las esquinas
		#0 ###### 1
		#2 ###### 3
		if i != 0 and j != 0:# si  no estoy en la esquina 0 entonces prgunte la celula de su esquina 0
			vecinos = vecinos +1
			infeccion = infeccion + cells[i-1][j-1].element()
		if i != 0:# si no estoy en la primera fila pregunte la celula de arriba
			vecinos = vecinos +1
			infeccion = infeccion +  cells[i-1][j].element()
		if i != 0  and len(cells[i]) - 1 !=  j:# si no estoy en la primera fila y no estoy en la ultima columna pregunte la esquina 1
			vecinos = vecinos +1
			infeccion = infeccion + cells[i-1][j+1].element()
		if j != 0:  # si no estoy en lla primera columna pregunte el vecino <-
			vecinos = vecinos +1
			infeccion = infeccion + cells[i][j-1].element()
		if len(cells[i]) - 1 !=  j: # si no estoy en lla ultima columna pregunte el vecino ->
			vecinos = vecinos +1
			infeccion = infeccion + cells[i][j+1].element()
		if i != len(cells)-1 and j != 0: # si no estoy en la ultima fila y no estoy en primera columna pregunte la esquina 2
			vecinos = vecinos +1
			infeccion = infeccion + cells[i+1][j-1].element()
		if i != len(cells)-1: #si no estoy en ultima fila pregunte el vecino de abajo
			vecinos = vecinos + 1
			infeccion = infeccion + cells[i+1][j].element()
		if i != len(cells)-1 and  len(cells[i]) - 1 !=  j: # si no estoy en la ultima fila y no estoy en la ultima columna pregunte a esquina 4
			vecinos = vecinos +1
			infeccion = infeccion + cells[i+1][j+1].element()
		return infeccion/(vecinos* max_infeccion)*100
	def next_generation(self): #con base a la anterior generacion(anterior fila) crea la siguiente
		cells  = self.cells() #saca las celulas en una variable
		for i,row in enumerate(cells): #recorre la ultima fila, obteniendo la posicion de cada columna y la celula
			for j,cell in enumerate(row):
				porcentaje_infeccion = self.porcentaje_infeccion(i,j,self.automata()._nodes[-1].element())
				if porcentaje_infeccion <= 35:
					cells[i][j] = self.automata().get_new_state(cell,[0])
				elif porcentaje_infeccion <= 55:
					cells[i][j] = self.automata().get_new_state(cell,[1])
				elif porcentaje_infeccion <= 75:
					cells[i][j] = self.automata().get_new_state(cell,[2])
				else:
					cells[i][j] = self.automata().get_new_state(cell,[3])
				# se dibua la celula
				self.draw_cell(cell,i,j)
class Cell:
	def __init__(self, state):
		self._state = state
	def state(self):
		return self._state
	def set_state(self,new_state):
		self._state = new_state
	def __str__(self):
		return str(self.state())
	def __repr__(self):
	    return str(self)
