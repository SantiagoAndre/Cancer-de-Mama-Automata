# -*- coding: utf-8 -*-
from logic.map import Neighborhood
from time import sleep,time

#imports interface
import pygame,sys
from pygame.locals import *

class InterfaceNeighborhood:
	#constructor
	def __init__(self,porcentaje_infeccion,rows=50,columns=50):
		self._calculate_dimencions(500,500,rows,columns)
		self.init_interface()
		self._neighborhood = Neighborhood(porcentaje_infeccion,rows,columns)
		self.draw_states_bar()
	#geterts
	def Neighborhood(self):
		return self._neighborhood
	def cell_large(self):
		return self._cell_large
	def dimencions(self):
		return self._dimencions
	def display(self):
		return self._display
	def init_interface(self):
		pygame.init() #se llama el init de pygame
		self._display = pygame.display.set_mode(self.dimencions()) #se obtiene el display, entregando una dupla = (ancho, alto) con las dimenciones de este
		pygame.display.set_caption("Cellular Automata") #se coloca el nombre de la pantalla
		pygame.display.update() # se actualiza el display

	#calcula las dimenciones del display y el tamaño de cada celula con base al numero de filas y columnas y el maximo largo del display, cada celula es un cuadrado
	def _calculate_dimencions(self,max_long,max_width,columns,rows):
		self._desplazamiento_y =110
		if max_long > max_width:
			self._cell_large = max_width / columns
			high = max_width
			width = self._cell_large*rows+self._desplazamiento_y
		else:
			self._cell_large = max_long / rows
			width = max_long+self._desplazamiento_y
			high = self._cell_large*columns
		
		self._dimencions=  int(high),int(width)
	#metodo principal, aqui se atrapan todos los eventos, se llama al metodo next_generation para que se vaya generando y dibujando cada fila, para luego
	#actualizar el display
	def start(self, generations = 100):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			#start_time = time()
			self.update_cells()
			self.dibujar_porcentaje_infeccion()
			#end_time = time()
			#print(end_time-start_time)
			pygame.display.update()#actualizar el diaplay
			sleep(1)
	def update_cells(self):
		for state_cell,i,j in self._neighborhood.next_generation():
			self.draw_cell(state_cell,i,j)
	#dibuja una celula, recibe como parametro el estado de la celula, y la posicion en la matriz
	def draw_cell(self,state_cell,column,row):
		# se  transforma la posicion en la matriz a la posicion en el display(pantalla)
		posx= self.cell_large()*row 
		posy = self.cell_large()*column + self._desplazamiento_y
		# se le dice a pygame q ue dibuje un rectangulo
		pygame.draw.rect(self.display(),state_cell.color(),(posx,posy,self.cell_large(),self.cell_large()))
		#                     display   , color           ,(posx,posy, largo            , ancho)
	def draw_states_bar(self):
		num_colors = len(self.Neighborhood().automata()._nodes)
		high_bar = 20
		width_bar = self._dimencions[0]*0.8
		posx_bar,posy_bar =  (self._dimencions[0]-width_bar)/2,  (self._desplazamiento_y-high_bar)*0.1
		increment_x = width_bar/num_colors
		for i,state in enumerate(self.Neighborhood().automata()._nodes):
			color = state.color()
			pygame.draw.rect(self.display(),color, (posx_bar+(increment_x*i),posy_bar,increment_x,high_bar))
		#DRAW ARROWS
		init_arrow = pygame.image.load("resources/img/arrow.png")
		self.display().blit(init_arrow,(posx_bar+(increment_x/2)-15,posy_bar+high_bar))
		self.display().blit(init_arrow,(posx_bar+width_bar-(increment_x/2)-15,posy_bar+high_bar))
		#DRAW TEXT STATES
		myfont = pygame.font.SysFont('Freesansbold.ttf', 20)
		text_sana = myfont.render('SANA', True, (255,255,255))
		text_enferma = myfont.render('ENFERMA', True, (255,255,255))
		self.display().blit(text_sana,(posx_bar+(increment_x/2)-21,posy_bar+high_bar+20))
		self.display().blit(text_enferma,(posx_bar+width_bar-(increment_x/2)-34,posy_bar+high_bar+20))
	def dibujar_porcentaje_infeccion(self):
		porcentaje_infeccion = self._neighborhood.porcentaje_infeccion_total()
		#barra
		alto_barra = 20		
		ancho_barra = self._dimencions[0]*0.7*porcentaje_infeccion/100
		posx_barra,posy_barra = (self._dimencions[0]-ancho_barra)/2,  (self._desplazamiento_y-alto_barra)*0.9
		gris = (50,50,50)
		negro= (0,0,0)
		pygame.draw.rect(self.display(),gris, (posx_barra,posy_barra,ancho_barra,alto_barra))
		#text
		pos_text =((self._dimencions[0]-150)/2,posy_barra - 20)
		#clean text
		pygame.draw.rect(self.display(),negro, (pos_text[0],pos_text[1],150,alto_barra))
		#show text
		
		myfont = pygame.font.SysFont('Freesansbold.ttf', 20)
		textsurface = myfont.render('porcentaje infeccion: '+ int(porcentaje_infeccion).__str__(), True, (255,255,255))
		self.display().blit(textsurface,(pos_text))
	