# -*- coding: utf-8 -*-
from map import Neighborhood
from time import sleep,time

#imports interface
import pygame,sys
from pygame.locals import *

class InterfaceNeighborhood:
	#constructor
	def __init__(self,porcentaje_infeccion,rows=50,columns=50):
		self.init_interface(rows,columns)
		self._neighborhood = Neighborhood(porcentaje_infeccion,rows,columns)
	#geterts
	def cell_large(self):
		return self._cell_large
	def dimencions(self):
		return self._dimencions
	def display(self):
		return self._display
	def init_interface(self,rows,columns):
		dimenciones = self._calculate_dimencions(500,500,rows,columns)
		pygame.init() #se llama el init de pygame
		self._display = pygame.display.set_mode(dimenciones) #se obtiene el display, entregando una dupla = (ancho, alto) con las dimenciones de este
		pygame.display.set_caption("Cellular Automata") #se coloca el nombre de la pantalla
		pygame.display.update() # se actualiza el display
	

	#calcula las dimenciones del display y el tamaño de cada celula con base al numero de filas y columnas y el maximo largo del display, cada celula es un cuadrado
	def _calculate_dimencions(self,max_long,max_width,columns,rows):
		self._desplazamiento_y = 100
		if max_long > max_width:
			self._cell_large = max_width / columns
			high = max_width
			width = self._cell_large*rows+self._desplazamiento_y
		else:
			self._cell_large = max_long / rows
			width = max_long+self._desplazamiento_y
			high = self._cell_large*columns
		
		self._dimencions= rows,columns
		return int(high),int(width)
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
			#sleep(1)
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
	def dibujar_porcentaje_infeccion(self):
		porcentaje_infeccion = self._neighborhood.porcentaje_infeccion_total()
		#barra
		alto_barra = 20		
		ancho_barra = self._dimencions[0]*0.7*porcentaje_infeccion/100
		posx_barra,posy_barra = (self._dimencions[0]-ancho_barra)/2,  (self._desplazamiento_y-alto_barra)*0.75
		gris = (50,50,50)
		negro = (0,0,0)
		pygame.draw.rect(self.display(),gris, (posx_barra,posy_barra,ancho_barra,alto_barra))
		#text
		pos_text =((self._dimencions[0]-150)/2,posy_barra - 50)
		#clean text
		pygame.draw.rect(self.display(),negro, (pos_text[0],pos_text[1],150,alto_barra))
		#show text
		
		myfont = pygame.font.SysFont('Freesansbold.ttf', 20)
		textsurface = myfont.render('porcentaje infeccion: '+ int(porcentaje_infeccion).__str__(), True, (255,255,255))
		self.display().blit(textsurface,(pos_text))