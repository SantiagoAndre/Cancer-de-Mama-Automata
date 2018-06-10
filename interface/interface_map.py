# -*- coding: utf-8 -*-
from logic.map import Neighborhood
from time import sleep,time

#imports interface
import pygame,sys
from pygame.locals import *

class InterfaceNeighborhood:
	#constructor
	def __init__(self,porcentaje_infeccion,rows_cells,columns_cells=50):
		self._neighborhood = Neighborhood(porcentaje_infeccion,rows_cells,columns_cells)
		self.init_panels(500)
		self.init_interface()
		self.draw_panels()
	#geterts
	def Neighborhood(self):
		return self._neighborhood
	def cell_large(self):
		return self._cell_large
	def dimencions(self):
		return self._dimencions
	def display(self):
		return self._display
	def panelNeighborhood(self):
		return self._panelNeighborhood
	def panelstates(self):
		return self._panelstates
	def panelinfogeneration(self):
		return self._panelinfogeneration
	def bar_infeccion(self):
		return self._bar_infeccion
	def init_interface(self):
		self._calculate_dimencions()
		pygame.init() #se llama el init de pygame
		self._display = pygame.display.set_mode(self.dimencions()) #se obtiene el display, entregando una dupla = (ancho, alto) con las dimenciones de este
		pygame.display.set_caption("Simulacion de la celulas cancerígenas") #se coloca el nombre de la pantalla
	def init_panels(self,width_panels):
		#crea los panels: Panelinfogeneracion: Tiene la informacion del porcentage de infeccion de la generacion actual
											#PanelNeighborhood: tiene el Neighborhood, tiene un metodo update cells que hace avanzar a a siguiente #generacion
											#PanelStates: tiene la informacion del significado de cada estado
		#Estos panels van en ese orden en lista hacia abajo
		high_panelinfo = 100 #largo del primer panel
		high_panelstates = 70 # largo del ultimo panel
		#no se sabe la altura del panelneighborhood
		pos =(0,high_panelinfo)
		self._panelNeighborhood = PanelNeighborhood(self,pos,width_panels,self.Neighborhood())# con base al tama;o de la matriz de celulas calcula su alto
		#los otros dos panels necesitan unos colores
		backgroundcolor = (255,255,255)# gris oscuro
		seccolor = (183,28,28) # gris claro
		textcolor = (0,0,0) # blanco
		#panelinfogeneration
		dimencions = (width_panels,high_panelinfo)
		pos =(0,0)
		self._panelinfogeneration = PanelInfoGeneration(self,pos,dimencions,backgroundcolor,seccolor,textcolor)
		#panel states
		dimencions = (width_panels,high_panelstates)
		pos =(0,high_panelinfo+self.panelNeighborhood().high())
		self._panelstates = PanelStates(self,pos,dimencions,backgroundcolor,seccolor,textcolor)

	#calcula las dimenciones del display y el tamaño de cada celula con base al numero de filas y columnas y el maximo largo del display, cada celula es un cuadrado
	def _calculate_dimencions(self):
		width = self.panelstates().width()
		high = self.panelNeighborhood().high() + self.panelstates().high() + self.panelinfogeneration().high()
		self._dimencions=  width,int(high)

	def draw_panels(self):
		#self.panelNeighborhood().draw()
		self.panelstates().draw(self.Neighborhood().cell_maker().all_states())
		self.panelinfogeneration().draw()
	#metodo principal, aqui se atrapan todos los eventos, se llama al metodo next_generation para que se vaya generando y dibujando cada fila, para luego
	#actualizar el display
	def start(self, generations = 100):
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			self.panelNeighborhood().update_cells()
			self.panelinfogeneration().draw_next()
			pygame.display.update()#actualizar el display
			sleep(1)
class Panel():#un panel solo con posicion tama;o y el display, es una clase abstracta
	def __init__(self,parent,pos,dimencions):
		self._pos = pos
		self._dimencions = dimencions
		self._parent = parent
	def parent(self):
		return self._parent
	def display(self):
		return self.parent().display()
	def pos(self):
		return self._pos
	def dimencions(self):
		return self._dimencions
	def width(self):
		return self.dimencions()[0]
	def high(self):
		return self.dimencions()[1]
	def posx(self):
		return self._pos[0]
	def posy(self):
		return self._pos[1]
	def set_pos(self,new_pos):
		self._pos = new_pos
	def sef_dimencions(self,new_dimensions):
		self._dimensions = new_dimensions
class PanelInfo(Panel):#hereda de panel, y maneja colores,
	def __init__(self,parent,pos,dimencions,backgroundcolor,seccolor,textcolor):
		Panel.__init__(self,parent,pos,dimencions)
		self.init_interface(backgroundcolor,textcolor,seccolor)
		self._text_font = None
	def backgroundcolor(self):
		return self._backgroundcolor
	def seccolor(self):
		return self._seccolor
	def textcolor(self):
		return self._textcolor
	def text_font(self):
		return self._text_font
	def set_font(self,sizefont):
		self._text_font = myfont = pygame.font.SysFont('Freesansbold.ttf', sizefont)
	def init_interface(self,backgroundcolor,textcolor,seccolor):
		self._backgroundcolor = backgroundcolor
		self._textcolor = textcolor
		self._seccolor = seccolor
	def draw(self):
		pygame.draw.rect(self.display(),self.backgroundcolor(),(self.pos()+self.dimencions()))
	def draw_text(self,pos,text,center=False,transparent=True):
		font = self.text_font()
		if transparent:
			surface = font.render(text, True, self.textcolor())
		else:
			surface = font.render(text, True, self.textcolor(),self.backgroundcolor())
		if center:
			rect = surface.get_rect(center=pos)
		else:
			rect = surface.get_rect(topleft=pos)
		self.display().blit(surface,rect)
		return rect #retorno un rectangulo que reprecenta donde esta eel texto y que dimenciones tiene
	def sizefont(width,sizetext):
		#return round(width/sizetext*1.9)
		return round(width/sizetext*1.4)

class PanelNeighborhood(Panel):
	def __init__(self,parent,pos,width,neighborhood):
		self._neighborhood = neighborhood
		rows_map,columns_map = neighborhood.dimencions()
		self._cell_large = width/columns_map
		high= (self._cell_large*rows_map)
		Panel.__init__(self,parent,pos,(width,high))
	def cell_large(self):
		return self._cell_large
	def Neighborhood(self):
		return self._neighborhood
	def update_cells(self):
		for state_cell,i,j in self.Neighborhood().next_generation():
			self.draw_cell(state_cell,i,j)
	def draw_cell(self,cell,column,row):
		# se  transforma la posicion en la matriz a la posicion en el display(pantalla)
		posx= self.cell_large()*row + self.posx() # se le suma la posicion del panel para que sea una posicion real
		posy = self.cell_large()*column + self.posy()
		# se le dice a pygame q ue dibuje un rectangulo
		pygame.draw.rect(self.display(),cell.state().color(),(posx,posy,self.cell_large(),self.cell_large()))
		#                     display   , color           ,(posx,posy, largo            , ancho)
class PanelInfoGeneration(PanelInfo):
	def __init__(self,parent,pos,dimencions,backgroundcolor,seccolor,textcolor):
		PanelInfo.__init__(self,parent,pos,dimencions,backgroundcolor,seccolor,textcolor)
		self._pos_textinfeccion = None
		self._pos_textgeneration = None
		self._barinfection = None
	def Neighborhood(self):
		return self.parent().Neighborhood()
	def pos_textinfeccion(self):
		return self._pos_textinfeccion
	def pos_textgeneration(self):
		return self._pos_textgeneration
	def barinfection(self):
		return self._barinfection
	def draw(self):
		PanelInfo.draw(self)
		#margen del panel, se crea un cuadrado que representa el espacio que se va ausar del panel
		#el espacio que se va a usar
		width, high = self.width()*0.9,self.high()*0.8
		posx,posy = self.width()*0.05+ self.posx(), self.high()*0.1+self.posy() # se le da una posicion real en el display
		self.draw_init(posx,posy,width,high)
	def draw_init(self,posx,posy,width,high):
		size_font = PanelInfo.sizefont(width,25)#25 es el tamano del texto mas largo que voy a escribir
																					 #width: el ancho maximo que puede ocupar
		self.set_font(size_font)
		#A continuacion se dibujan los textos
		text = "Generacion: "
		(posx_text,posy_text) = posx,posy
		rect_text = self.draw_text((posx_text,posy_text),text)
		self._pos_textgeneration= (posx_text+rect_text.width,posy_text) #cambio la posicion del texto de la generracion
		text = "Porcentaje de infeccion: "
		(posx_text,posy_text) = posx,posy+high*0.3
		rect_text = self.draw_text((posx_text,posy_text),text)
		self._pos_textinfeccion = (posx_text+rect_text.width,posy_text) #cambio la posicion del texto de infeccion
		#barra de infeccion base
		posx_bar,posy_bar = posx, posy + high*0.7
		width_bar,high_bar = width, posy + high*0.9-posy_bar
		pygame.draw.rect(self.display(),self.textcolor(),(posx_bar,posy_bar,width_bar,high_bar),3)
		self._barinfection = (posx_bar+2,posy_bar+2,width_bar-4,high_bar-4)
		pygame.draw.rect(self.display(),(180,180,180),self.barinfection())
	def draw_next(self):
		generation = self.Neighborhood().generation()
		porcentaje_infeccion,estado_general = self.Neighborhood().state_neighborhood()
		self.draw_text(self.pos_textgeneration(),generation.__str__()+ " ",transparent=False)
		self.draw_text(self.pos_textinfeccion(),int(porcentaje_infeccion).__str__()+" ",transparent=False)
		posx_bar,posy_bar,width_bar,high_bar = self.barinfection()
		width_bar = width_bar*porcentaje_infeccion/100
		pygame.draw.rect(self.display(),estado_general.color(),(posx_bar,posy_bar,width_bar,high_bar))
class PanelStates(PanelInfo):# este panel es el de abajo, tiene la informacion de los estados
	def __init__(self,parent,pos,dimencions,backgroundcolor,seccolor,textcolor):
		PanelInfo.__init__(self,parent,pos,dimencions,backgroundcolor,seccolor,textcolor)
	def draw(self,state_colors):
		PanelInfo.draw(self)
		self.draw_states_bar(state_colors)
	def draw_states_bar(self,states):
		num_states = len(states)
		high_bar = self.high()*0.2
		width_bar = self.width()*0.9
		posx_color,posy_color =  (self.width()-width_bar)/2 + self.posx(),  (self.high()*0.5-high_bar)*0.35 + self.posy()
		width_state = width_bar/num_states
		sizefont = PanelInfo.sizefont(width_state,7)
		self.set_font(sizefont)
		for i,state in enumerate(states):
			pygame.draw.rect(self.display(),state.color(), (posx_color,posy_color,width_state,high_bar))
			pygame.draw.rect(self.display(),self.textcolor(), (posx_color,posy_color,width_state,high_bar),2)
			label  = "FASE "+ i.__str__()
			self.draw_row_of_state((posx_color,posy_color,width_state,high_bar),label)
			posx_color += width_state

	def draw_row_of_state(self,state,label):#dibuja una flecha debajo del estado indicado
		#este metodo calcula un recuadro que delimita a la flecha, y uno para eltexto, y luego las ibuja por medio de metodos
		posx,posy,width,high= state
		high_row = (self.high()-high-(posy-self.posy()))*0.8
		posy_row = posy+high+high_row/8 #el 0.1 de todo el espacio, y sobraria un 0.1 al final quedando centrado el espacio
		self.draw_row((posx,posy_row,width,high_row/2))
		pos_text = posx+width/2, posy_row+high_row*0.8
		self.draw_text(pos_text,label,center=True)

	def draw_row(self,minipanel):
		posx,posy,width,high = minipanel
		#obligando a que el area se el cuadrado mas grande posible
		if width< high:
			high = width
		elif high<width:
			posx += (width-high)/2
			width = high
		#pints rows
			#####1####
			#2##3#6##7
			####4#5###
		posxleft =posx+width*0.3
		posxright =posx+width*0.7
		ymiddle = posy+high*0.63
		points = [(posx+width/2,posy),(posx,ymiddle),(posxleft,ymiddle),(posxleft,posy+high),(posxright,posy+high),(posxright,ymiddle),(posx+width,ymiddle)]
		pygame.draw.polygon(self.display(),self.seccolor(), points)
