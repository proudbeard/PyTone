#!/usr/bin/env/python
#-*- coding: utf-8 -*-
"""
	topic:	Intro sequence
	os:		Mac OS X 10.7.5

	author:	Mikael Svensson
	date:	2013-08-25
"""

import pygame
from knob import Knob
from locals import *
from gradient import Gradient


class Intro:
	""" Calling the run function will display an intro animation """
	screen = None
	surfaces = []
	knobs = []
	pos = []
	duration = 0
	start = 0 #start time
	running = False
	clock = None

	def __init__(self, gradient, img_path, duration=5000):
		""" 
			Inits graphical components

			gradient: A gradient object to act as background
			img_path: path to images
			duration: duration of intro sequence in milliseconds
		"""
		self.screen = gradient
		self.duration = duration

		#knob image
		img = pygame.image.load(img_path + 'knob.png')
		#img = pygame.transform.scale(img, (150, 150))

		#plates
		rust = pygame.image.load(img_path + 'rust.png')
		rust = pygame.transform.scale(rust, (120, 120))

		#petrolium
		petrol = pygame.image.load(img_path + 'petrol.png')
		petrol = pygame.transform.scale(petrol, (120, 120))

		for i in range(2):
			knob = Knob(img)
			knob.set_shadow((-6,-4), 150, 25)
			self.knobs.append(knob)

		#the two diffrent plates in a pattern
		self.knobs[0].set_plate(rust)
		self.knobs[1].set_plate(petrol)

		#position the knobs
		img_center = img.get_rect().center
		self.pos.append((125 - img_center[0], 125 - img_center[1]))
		self.pos.append((275 - img_center[0], 125 - img_center[1]))

		#texts
		center = self.screen.get_rect().center #screen center

		#logo
		font = pygame.font.Font(pygame.font.get_default_font(), 40)
		logo = font.render('PyTone', True, BLACK)
		logo_cnt = logo.get_rect().center # texts center
		logo = (logo, (center[0] - logo_cnt[0], 250 - logo_cnt[1])) #storing surface & position in a tuple
		self.surfaces.append(logo)

		#credits
		font = pygame.font.Font(img_path + 'Actor-Regular.ttf', 10)
		credits = font.render('MIKAEL SVENSSON 2013', True, BLACKER)
		cred_cnt = credits.get_rect().center
		credits = (credits, (center[0] - cred_cnt[0], 364 - cred_cnt[1])) #storing surface & position in a tuple
		self.surfaces.append(credits)

		self.clock = pygame.time.Clock()
		

	def run(self):
		if self.running:
			return False

		self.start = pygame.time.get_ticks() # set start time
		self.running = True
		degrees = 0#0.5

		#run for a while...
		while (pygame.time.get_ticks() - self.start) < self.duration:
			self.clock.tick(60)
			self.screen.clear()
			pygame.event.pump()
			#rotate the knobs
			for i in range(len(self.knobs)):
				if (i + 1) % 2 == 0:
					self.knobs[i].rotate(-degrees)
				else:
					self.knobs[i].rotate(degrees)	
				self.screen.blit(self.knobs[i], self.pos[i])

			if degrees < 360:
				degrees += 1
			else:
				degrees = 0
			
			#redraw screen
			for surf in self.surfaces:
				self.screen.blit(surf[0], surf[1])
			self.screen.draw()
			self.clock.tick(60)


		#intro's done! Fade out....
		self.screen.fadeOut(500,50)
		self.running = False
		return True