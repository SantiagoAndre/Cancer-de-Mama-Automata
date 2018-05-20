# -*- coding: utf-8 -*- 
from time import sleep
from random import randint as rand
from automaton import CellularAutomate
#imports interface
import pygame,sys
from pygame.locals import *

class Neighborhood:
	#constructor
	def __init__(self,rows=10,columns=10):
		self._calculate_dimencions(1024,rows,columns)
		self.init_interface()
		self.init_automata()
		self.init_generation(rows, columns)
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
	#inicializa el automata, este tiene las reglas del siguiente destado de una celula de acuerdo a las condiciones en  las que se encuentra
	def init_automata(self):
		#dos colores
		white = (125,125,125)
		black = (0,0,0)
		#dos estados
		LIVE = 1 #vivo
		DEAD = 0 #muerto
		#S = [(LIVE,white),(DEAD,black)] #se guardan en un vector
		S = [(LIVE,white),(DEAD,black)] #se guardan en un vector
		alphabet = [0,1,2,3,4,5,6,7] # un alfabeto
		T = [(LIVE,DEAD,7),(LIVE,DEAD,6),(DEAD,DEAD,5),(DEAD,LIVE,4),(LIVE,LIVE,3),(LIVE,LIVE,2),(DEAD,LIVE,1),(DEAD,DEAD,0)] # las transiciones
		self._automata = CellularAutomate(S,alphabet,T) # guarda el automata en un atributo de  Neighborhood
		
	def init_generation(self,rows, columns):
		SLIVE = self.automata()._nodes[0] #state live
		SDEAD = self.automata()._nodes[1] #state dead
		self._cells = []
		self._cells.append([(SLIVE if rand(0,1) == 0 else SDEAD)  for _ in range(columns) ] )
		#self._cells.append([(SLIVE if j in(0,2,3,10,8,7) else SDEAD)  for _ in range(columns/10) for j in range(10)] )
	def next_generation(self): #con base a la anterior generacion(anterior fila) crea la siguiente
		cells  = self.cells() #saca las celulas en una variable
		fnl_row = self.cells()[len(self.cells())-1] #obtiene la ultima fila
		new_row = [] # inicializa la nueva fila
		for c,state_cell in enumerate(fnl_row): #recorre la ultima fila, obteniendo la posicion de cada columna y la celula
												  #yaa que en cada posicion de la matriz se guarda el estado de la celula llamo a a variable state_cell
			# se obtiene el siguiente patron: vivo= 1, muerto= 0, se obtienen los estados de la celula anterior, actual y siguiete,
			# estos tres numeroos forman un numero binario el bit 'anterior' es el bit de mayor peso
			
			pattern =  state_cell.element()*2 
			if c != 0:
				pattern = pattern + fnl_row[c-1].element()*4
			if len(fnl_row) != c+1:
				pattern = pattern + fnl_row[c+1].element()
			# este numero se tranforma en decimal y se envia al automata, con el estado de la celula central
			new_state = self.automata().get_new_state(state_cell,[pattern])
			# se añade el nuevo estado(en si es la nueva celula con el estado que arroo el automata pero no hice celula) a la nueva fila
			new_row.append(new_state)
			# se dibua la celula
			self.draw_cell(state_cell,len(self.cells())-1,c)
		#se añade la nueva fia a las celulas
		self.cells().append(new_row)
	# inicializa la interfaz
	def init_interface(self):
		pygame.init() #se llama el init de pygame
		self._display = pygame.display.set_mode(self.dimencions()) #se obtiene el display, entregando una dupla = (ancho, alto) con las dimenciones de este
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
