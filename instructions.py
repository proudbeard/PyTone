#!/usr/bin/env/python
#-*- coding: utf-8 -*-
"""
	topic:	Intro sequence
	os:		Mac OS X 10.7.5

	author:	Mikael Svensson
	date:	2013-08-25
"""

import pygame
from pygame.locals import *
from knob import Knob
from locals import *
from gradient import Gradient


class Instructions:
	""" Calling the run function will display an instructions window """

	screen = None

	header = 'INSTRUCTIONS'
	strings = ['PyTone is an ear training software where your mission is',
			'to tune in a specified musical interval.',
			'',
			'Be focused and try listen for the beat frequency. If it feels to hard,',
			'there\'s a practice mode with a simple tuner.',
			'',
			'Use up and down arrows keys for coarse tune and',
			'left and right for final ajustments.']
			 
			 

	surfaces = [] # surfaces to be blitted
	back = None


	def __init__(self, gradient, path):
		""" 
			Inits graphical components

			gradient: A gradient object to act as background
			path: path to media resources
		"""
		self.screen = gradient

		#get center
		center = self.screen.get_rect().center

		#back
		back_img = pygame.image.load(path + 'back.png')
		back_pos = (30,30)
		self.back = (back_img, (30,30), self.screen.blit(back_img, back_pos)) #storing surface, position & rect for collision check

		#texts
		font = pygame.font.Font(pygame.font.get_default_font(), 14)
		header_pos = ((center[0] - font.size(self.header)[0]/2), 75)
		self.surfaces.append((font.render(self.header, True, BLACK), header_pos))
		
		font = pygame.font.Font(path + 'Actor-Regular.ttf', 12)
		#find max width in string array
		width, height = font.size(max(self.strings, key=len))
		px = center[0] - (width / 2)
		py = 140 # startpos y axis
		for i in range(len(self.strings)):
			self.surfaces.append((font.render(self.strings[i], True, BLACKER), (px, py + height*i)))
		


		#logo
		font = pygame.font.Font(pygame.font.get_default_font(), 12)
		logo_pos = 339, 373
		self.surfaces.append((font.render('PyTone', True, BLACK), logo_pos))

	def run(self):
		self.screen.clear()
		self.screen.blit(self.back[0], self.back[1])
		for surf in self.surfaces:
			self.screen.blit(surf[0], surf[1])
		self.screen.draw()
		while True:
			for e in pygame.event.get():
				if e.type == MOUSEBUTTONUP:
					if self.back[2].collidepoint(e.pos):
						return False
				elif e.type == QUIT:
					return False

