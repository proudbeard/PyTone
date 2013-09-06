#!/usr/bin/env/python
#-*- coding: utf-8 -*-
"""
	topic:	Pytones main scene.
	os:		Mac OS X 10.7.5

	author:	Mikael Svensson
	date:	2013-08-25
"""

"""
	Levels:

	Level: 		Steps: 					Guide (Hz):		Initial (steps):
	1 			1 						440 			2
	2 			12 						440 			11
	3 			5 						440				6
	4 			4 						220 < 440		rand < 12
	5 			rand < 12 (not prev.)	220 < 440		rand < 12
	6			rand (not prev.)		220 < 440		rand
	7 < inf 	rand 					220 < 440		rand

"""

import pygame
from pygame.locals import *
from knob import Knob
from locals import *
from gradient import Gradient
from oscillator import Oscillator
from interval import Interval
from tuner import Tuner # for practise mode

import random
import math


class Game:
	""" The main game class. This deals with two oscillators, of which one is adjustable.
		The diffrence between those frequencies are measured and compared to the wanted interval.
		Margin of errors is given i cents.

	 """
	screen = None
	center = None #screen center
	instructions = None #instructions surface
	interval = None #interval surface
	result = None # surface for result displaying


	path = None

	knob = None
	knob_rect = None
	plate = None

	running = False

	intevals = None
	guide_osc = None # guide note oscillator
	guide = None # guide_osc frequency
	osc = None # user ajustable oscillator
	guide_ch = None #Audio channel
	osc_ch = None #Audio channel
	pitch = None # osc frequency


	steps = 1 # number of musical notes. Level one starts at an octave
	prev_steps = []
	max_freq = 0 # 4 x base oscillator frequency (two octaves)
	min_freq = 0 # bace oscillator frequency

	level = 1

	pause = False # pausing main loop

	practise = False
	tuner = None

	acceptable_off = 10 # how many cents off for a corrects answer?


	def __init__(self, gradient, path):
		""" 
			gradient: A gradient object to act as background
			path: path to images

		"""
		self.screen = gradient
		self.center = self.screen.get_rect().center

		self.path = path

		# interval class
		self.intervals = Interval()

		self.instr_str = 'UP AND DOWN ARROWS COARSE TUNE. USE LEFT AND RIGHT FOR FINE ADJUSTMENT'
		self.conf_str = 'PRESS ENTER TO CONFIRM'

		self.setLevel(self.level)

		self.initGUI()
		#self.initAudio()

	def initGUI(self):
		""" Inits the graphical components """

		#clear background
		self.screen.clear()
		self.screen.draw()

		#knob image
		img = pygame.image.load(self.path + 'knob.png')

		#plates
		self.plate = pygame.image.load(self.path + 'rust.png')

		self.knob = Knob(img)
		self.knob.set_plate(self.plate)
		self.knob.set_shadow((-6,-4), 150, 25)
		knb_center = self.knob.get_rect().center
		self.knob = (self.knob, (self.center[0]-knb_center[0], self.center[1]-knb_center[1])) # also stores knob.rect at blit time		
		
		self.center = self.screen.get_rect().center

		#"back" 
		back_img = pygame.image.load(self.path + 'back.png')
		back_pos = (30,30)
		#tuple width the image and it's position and a third element containting elements Rect.
		self.back = (back_img, (30,30), self.screen.blit(back_img, back_pos))

		#arrow
		arrow_img = pygame.image.load(self.path + 'arrow.png')
		self.arrow = (arrow_img, (self.center[0] - arrow_img.get_width()/2, 104)) 

		#instructions, texts
		instrs = ['UP', 'DOWN', 'FINE UP', 'FINE DOWN', 'PRESS ENTER TO CONFIRM']
		font = pygame.font.Font(self.path + 'Actor-Regular.ttf', 10)

		#instructions, key images
		key_images = pygame.Surface((184, 69), pygame.SRCALPHA, 32) #collecting those images in a surface, for flexible positioning.
		key_images_cp = key_images.get_rect().center

		img = pygame.image.load(self.path + 'key.png')
		up = pygame.transform.rotozoom(img, 90, 1)
		key_images.blit(up, (key_images_cp[0] - up.get_size()[0]/2, 0)) #up arrow
		key_images.blit(font.render(instrs[0], True, BLACK), (key_images_cp[0] - font.size(instrs[0])[0]/2, 9)) #up text
		key_images.blit(font.render(instrs[3], True, BLACK), (0, key_images_cp[1] - font.size(instrs[3])[1]/2)) #left text
		left = pygame.transform.rotozoom(img, 180, 1)
		key_images.blit(left, (font.size(instrs[3])[0] + 5, key_images_cp[1] - left.get_size()[1]/2)) #left arrow
		right = img
		key_images.blit(right, (key_images.get_width() - font.size(instrs[3])[0] - 5 - right.get_size()[0], key_images_cp[1] - right.get_size()[1]/2)) #right arrow (reflects left)
		key_images.blit(font.render(instrs[2], True, BLACK), (key_images.get_width() - font.size(instrs[3])[0] + 5 - right.get_size()[0], key_images_cp[1] - font.size(instrs[2])[1]/2)) #right text
		key_images.blit(font.render(instrs[1], True, BLACK), (key_images_cp[0] - font.size(instrs[1])[0]/2, 44)) #down text
		down = pygame.transform.rotozoom(img, 270, 1)
		key_images.blit(down, (key_images_cp[0] - down.get_size()[0]/2, 69 - down.get_size()[1])) #up arrow

		#public parent container for instructions
		self.instructions = pygame.Surface((self.screen.get_width(), 115), pygame.SRCALPHA, 32)
		self.instructions.blit(key_images, (self.instructions.get_rect().center[0] - key_images_cp[0], 0))
		self.instructions.blit(font.render(instrs[4], True, BLACK),(self.instructions.get_rect().center[0] - font.size(instrs[4])[0]/2, key_images.get_height() + 20))


	def initAudio(self):
		""" Inits the two oscillators and their channels. """

		#guide tone
		self.guide_osc = Oscillator('sine', self.guide, BUFFER_SIZE)
		self.guide_ch = pygame.mixer.Channel(0)
		self.guide_ch.set_volume(0.9/2.0)

		#adjustable (the knob one), starts at same freq
		self.osc = Oscillator('sine', self.pitch, BUFFER_SIZE)
		self.osc_ch = pygame.mixer.Channel(1)
		self.osc_ch.set_volume(0.9/2.0)

	def setLevel(self, level):
		""" inits different levels """

		lowest_freq = 220 # low limit
		# for use in levels > 4
		rand_guide = self.stepToFreq(random.randint(0, 12), 220) # 220Hz < 440Hz in perfect notes.

		if level == 1:
			self.guide = 440
			self.steps = 0
			self.pitch = self.stepToFreq(1, self.guide)

		elif level == 2:
			self.guide = 440
			self.steps = 12
			self.pitch = self.stepToFreq(11, self.guide)

		elif level == 3:
			self.guide = 440
			self.steps = 7
			self.pitch = self.stepToFreq(6, self.guide)

		elif level == 4:
			self.guide = rand_guide
			self.steps = 5
			init_rand = random.randint(0, 11)
			self.pitch = self.stepToFreq(init_rand, self.guide)

		elif level == 5:
			self.guide = rand_guide
			self.steps = self.randExclude(self.prev_steps + [5], 0,12)
			init_rand = random.randint(0, 11)
			self.pitch = self.stepToFreq(11, self.guide)

		elif level == 6:
			self.guide = rand_guide
			self.steps = self.randExclude(self.prev_steps + [6])
			init_rand = random.randint(0, 24)
			self.pitch = self.stepToFreq(11, self.guide)

		elif level >= 7:
			self.guide = rand_guide
			self.steps = random.randint(0,24) # whole range
			init_rand = random.randint(0, 24)
			self.pitch = self.stepToFreq(11, self.guide)

		else:
			return False

		self.prev_steps.append(self.steps) #store, for unique intervals the first 6 levels
		
		# set min/max frequencies
		self.max_freq = self.guide * 4 # maximum frequency
		self.min_freq = self.guide - 20# minimum frequency 
		
		#set interval text
		self.setIntervalText()

	def setIntervalText(self):
		""" Text to display the wanted interval """
		font = pygame.font.Font(pygame.font.get_default_font(), 18)
		img = font.render(self.intervals.at(self.steps), True, BLACK)
		#interval surface gets made every time function is called, this is done during pauses in main loop. The inefficiency should not be a problem.
		self.interval = pygame.Surface((self.screen.get_width(), font.get_height()), SRCALPHA, 32)
		self.interval.blit(img, (self.center[0] - img.get_width()/2, 0))



	def draw(self):
		""" draw screen """

		self.back = (self.back[0], self.back[1], self.screen.blit(self.back[0], self.back[1]))
		self.screen.blit(self.arrow[0], self.arrow[1])

		self.screen.blit(self.knob[0], self.knob[1])

		if not self.pause:
			self.screen.blit(self.interval, (0, 70))
			self.screen.blit(self.instructions, (0, 285))

		#practise mode?
		if self.practise is True:
			#display tuner
			goal = self.stepToFreq(self.steps, self.guide_osc.frequency())
			cents = self.hertzToCents(goal, self.pitch)
			self.tuner.update(cents)
			self.screen.blit(self.tuner, (self.center[0]-self.tuner.center[0], 20))

		self.screen.draw()

	def updateChannels(self):
		""" update audio queues """
		if self.guide_ch.get_queue() == None:
			self.guide_ch.queue(self.guide_osc.samples())

		if self.osc_ch.get_queue() == None:
			self.osc_ch.queue(self.osc.samples())

	def set_practise(self, on=True):
		""" Turn practise mode on/off """
		self.practise = on
		self.tuner = Tuner(self.path) #initiats at practise on, and stays.

	def message(self):
		""" Checks current frequency (at the adjustable oscillator)
			and sets a message to user
		"""
		font = pygame.font.Font(pygame.font.get_default_font(), 18)

		goal = self.stepToFreq(self.steps, self.guide_osc.frequency())
		cents = self.hertzToCents(goal, self.pitch)

		self.screen.clear()

		if cents < 0: off = 'flat'
		elif cents > 0: off = 'sharp'

		msg = ''

		#ok?
		if cents > -self.acceptable_off and cents < self.acceptable_off:
			self.level += 1;
			self.setLevel(self.level)
			self.guide_osc.set_frequency(self.guide)

			msg = 'Well done! Just ' + str(round(cents,1)) + ' cents ' + off + '.'
		else:
			msg = str(round(cents,1)) + ' cents ' + off + '. Try again'

		if round(cents,1) == 0:
			msg = 'Amazing! Right on the spot!'

		#display message
		img = font.render(msg.upper(), True, BLACK)
		self.screen.blit(img, (self.center[0] - img.get_width()/2, 70))

		#instruction message
		cont = 'PRESS ANY KEY TO CONTINUE.'
		font = pygame.font.Font(self.path + 'Actor-Regular.ttf', 10)
		self.screen.blit(font.render(cont, True, BLACK),(self.center[0] - font.size(cont)[0]/2, self.screen.get_height() - font.size(cont)[1] - 13))

		self.draw()

	def run(self):
		""" main game loop.
			Always starts from level 1, and reinits the oscillators/audio channels 
		"""

		if self.running:
			return False
		self.running = True
		degrees = 0
		self.setLevel(1) # start from level 1 again
		self.initAudio() # init audio here for fresh oscillators

		clock = pygame.time.Clock()

		while self.running:
			
			if not self.pause:
				#start with checking each channels audio queue
				self.updateChannels()
				self.screen.clear()

				mx,my = pygame.mouse.get_pos()
				keystate = pygame.key.get_pressed()

				#fast increase frequency
				if keystate[K_UP]:
					if self.pitch < self.max_freq:
						self.pitch += 1.6#*= 1.01
						#self.pitch *= 1.01
						degrees += 1.3
						self.knob[0].rotate(degrees)

				#fast decrease frequency
				elif keystate[K_DOWN]:
					if self.pitch > self.min_freq:
						self.pitch -= 1.6#/= 1.01
						#self.pitch /= 1.01
						degrees -= 1.3
						self.knob[0].rotate(degrees)

				#slow decrease frequency
				elif keystate[K_LEFT]:
					if self.pitch > self.min_freq:
						self.pitch -=  0.1
						degrees -= 0.2
						self.knob[0].rotate(degrees)

				#slow increase frequency
				elif keystate[K_RIGHT]:
					if self.pitch < self.max_freq:
						self.pitch += 0.1
						degrees += 0.2
						self.knob[0].rotate(degrees)

				self.osc.set_frequency(self.pitch)
				

			for e in pygame.event.get():
				if e.type == QUIT:
					self.running = False

				elif e.type == MOUSEBUTTONDOWN:
					#check back button
					if self.back[2].collidepoint(e.pos):
						self.running = False

				elif e.type == KEYUP:
					#unpause
					if self.pause:
						self.pause = False
						break
					elif e.key == K_RETURN:
						self.pause = True
						self.message()
						
			if not self.pause:
				#redraw screen
				self.draw()
			clock.tick(60)


		self.running = False
		return True


	#helpers
	def hertzToCents(self, a, b):
		try:
			return 1200 * math.log((b/float(a)), 2)
		except Exception as e:
			print e
			return 0

	def posToDeg(self, pos): #not used
		""" Returns a positions degree from windows center """
		degree = math.degrees(math.atan2(self.center[1]-pos[1], self.center[0]-pos[0])) + 180
		if degree == 360.0:
			degree = 0
		return round(degree)

	def randExclude(self, seq, low=0, high=24):
		""" returns a random integer

			seq: numbers to exclude (list)
			low: lowest int
			high: highest int
		"""
		rand = 0
		while rand in seq:
			rand = random.randint(low, high)
		return rand

	def stepToFreq(self, step, frequency=False):
		""" returns a frequncy scale or a new frequency

			step: number of keys
			frequency: from frequency
		"""
		if not frequency:
			return math.pow(2, step/12.0)

		return frequency * math.pow(2, step/12.0)

	def freqToNote(self, freq): #not used
		""" Code for determining note name from frequency value.
			Code is written for equal temperament and A=440.
			Notes are displayed according to sharps. This can be overrided easily by changing the array definition below.

			Written by Firat Civaner (for mathlab)
			http://www.mathworks.com/matlabcentral/fileexchange/35330-frequency-to-note/content/freq2note.m


			return: A tuple with  a string with notename + octave and frequency offset in cents
		"""

		A4 = 440
		notenames = ['C' , 'C#', 'D' , 'D#' , 'E' , 'F' , 'F#', 'G' , 'G#' , 'A' , 'A#' , 'B' ]

		centdif = round( 1200 * math.log(freq/A4)/math.log(2))

		notedif = round(centdif/100)
		if centdif % 100 > 50:
			notedif = notedif + 1

		error = centdif-notedif*100
		notenumber = notedif + 9 + 12*4 #count of half tones starting from C0.

		octavenumber = round((notenumber)/12)
		place = int(round(notenumber % 12 + 1))
		if place < 0 or place > len(notenames)-1:
			print place
			return 'error'
		try:
			return (notenames[place]+str(octavenumber), error)
		except:
			return 'Error. Could not identify note'




