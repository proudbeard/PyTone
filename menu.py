#!/usr/bin/env/python
#-*- coding: utf-8 -*-
"""
	topic:	Main menu
	os:		Mac OS X 10.7.5

	author:	Mikael Svensson
	date:	2013-08-20
"""

import pygame
from pygame.locals import *
from itertools import izip
from knob import Knob
from locals import *
from gradient import Gradient

#enum like...
PRACTICE = 0
NEW_GAME = 1
INSTRUCTIONS = 2




class Menu:
	""" Main menu for PyTone """
	screen = None
	snap = 30
	options = {} #map to keep track of our menu options. dict[degree] = (option_rect, return value)
		

	def __init__(self, gradient, path):
		""" 
			gradient: A gradient object to act as background
			path: path to media
		"""
		start = 330
		stop = 60
		self.screen = gradient
		img = pygame.image.load(path + 'switch.png')
		self.switch = Knob(img, self.snap, (start, stop))
		snd = pygame.mixer.Sound(path + 'switch_snd.ogg')
		self.switch.set_sound(snd)
		self.switch.set_volume(0.5)
		self.path = path

	def draw(self):
		#clear
		self.screen.clear()
			
		#blit switch object
		pos = self.tupleSub(self.screen.get_rect().center, self.switch.get_rect().center)
		self.screen.blit(self.switch, pos)
	
		#draw lines
		line_practice = pygame.draw.aalines(self.screen, BLACK, False, ((254, 167), (257,164),(280,164)))
		line_newGame = pygame.draw.aaline(self.screen, BLACK, (264, 200), (280,200))
		line_instr = pygame.draw.aalines(self.screen, BLACK, False, ((254, 233), (257,236),(280,236)))
		line_quit = pygame.draw.aalines(self.screen, BLACK, False, ((236, 264), (243,272),(280,272)))

		#make labels
		#logo
		font = pygame.font.Font(pygame.font.get_default_font(), 21)
		text = font.render('PyTone', True, BLACK)
		text_size = font.size('PyTone')
		self.screen.blit(text, (50,192))


		#menu options
		font = pygame.font.Font(self.path + "Actor-Regular.ttf", 10)

		practice = font.render("PRACTICE", True, BLACK)
		self.options[330] = (self.screen.blit(practice,(290,158)), PRACTICE)

		new = font.render("NEW  GAME", True, BLACK)
		self.options[0] = (self.screen.blit(new,(290,194)), NEW_GAME)

		instructions = font.render('INSTRUCTIONS', True, BLACK)
		self.options[30] = (self.screen.blit(instructions,(290, 230)), INSTRUCTIONS)

		quit = font.render('EXIT', True, BLACK)
		self.options[60] = (self.screen.blit(quit, (290,266)), QUIT)


		#draw screen
		self.screen.draw()

	def run(self):
		while True:
			self.draw()
			for e in pygame.event.get():
				if e.type == QUIT:
					return QUIT
				if e.type == KEYUP:
					if e.key == K_UP:
						self.switch.snap('CCW')
					elif e.key == K_DOWN:
						self.switch.snap('CW')
					elif e.key in (K_RETURN, K_SPACE):
						try:
							return self.options[self.switch.degree()][1]
						except:
							print "Error. Unknown menu option: " + str(self.switch.degree())

				#check for clicks
				elif e.type == MOUSEBUTTONUP:
					for key, value in self.options.items():
						if value[0].collidepoint(e.pos):
							sw_deg = self.switch.degree()

							#Two clicks on the same label confirms
							if int(key) == int(sw_deg):
								return value[1]

							#rotate
							self.switch.rotate(key)



			pygame.time.wait(10)



	#helper functions
	def tupleAdd(self, a, b):
		""" 
			Element wise addition of two tuples 
			Credits to @delnan http://stackoverflow.com/questions/5607284/how-to-add-with-tuples
		"""
		return tuple(x + y for x, y in izip(a, b))

	def tupleSub(self, a, b):
		return tuple(x - y for x, y in izip(a, b))

