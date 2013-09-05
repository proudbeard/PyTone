#!/usr/bin/env/python
#-*- coding: utf-8 -*-
"""
	topic:	Main for PyTone application
	os:		Mac OS X 10.7.5

	author:	Mikael Svensson
	date:	2013-08-24
"""

import pygame
from gradient import Gradient
from intro import Intro
from menu import *
from game import Game
from instructions import Instructions

from locals import *

GRAD_START = (255,255,255,255)
GRAD_END =  (207,206,205, 255)
GRAD_END = (199,198,197,255)

def main():
	#pygame init
	pygame.mixer.pre_init(SAMPLE_RATE, BIT, CHANNELS, BUFFER_SIZE)
	pygame.init()
	pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('PyTone')

	#make background
	background = Gradient((WIDTH, HEIGHT), GRAD_START, GRAD_END)

	#path to medias
	path = 'media/'

	pygame.display.set_icon(pygame.image.load(path + 'petrol.png'))

	#intro duration in milliseconds
	duration = 4000

	#states
	intro = Intro(background, path, duration)
	menu = Menu(background, path)
	game = Game(background, path)
	instructions = Instructions(background, path)

	intro.run()

	#storing return value from menu
	running = True
	while running:
		option = menu.run()
		if option == NEW_GAME:
			option = game.run()

		elif option == INSTRUCTIONS:
			instructions.run()
		elif option == PRACTICE:
			#intro.run()
			game.set_practise(True)
			game.run()
			game.set_practise(False)

		#no elif here to make different states be able to quit as well
		if option == pygame.locals.QUIT:
			pygame.quit()
			running = False

main()