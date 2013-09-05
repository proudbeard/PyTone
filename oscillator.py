#!/usr/bin/env/python
"""
	file:	oscillator.py
	topic:	Oscillator class

	author:	Mikael Svensson
	date:	2013-08-20
"""

import numpy, pygame
from wavetable import WaveTable

class Oscillator:
	"""
		Simple oscillator for pygame mixer.
		This is ment to be used by repeatedly calling the getSamples() member function,
		which will return a pygame Sound object with the length of the buffer size.
		Please note that this requires the buffer size to be choosen with care.

		TODO: Fix stereo compability
	"""
	m_table = None
	m_type = None
	m_buffer = None
	m_frequency = 0
	m_pos = 0
	m_length = 0

	def __init__(self, wave='sine', freq=440.0, buffersize=4096):
		inits = pygame.mixer.get_init()
		if inits == None:
			print "Error. pygame not initialized"
			return

		#detect bit
		if inits[1] == -16:
			self.m_type = numpy.int16
		elif inits[1]  == 16:
			self.m_type = numpy.uint16
		elif inits[1]  == -8:
			self.m_type = numpy.int8
		elif inits[1]  == 8:
			self.m_type = numpy.uint8
		else:
			print "Error. Unknown bit size"

		self.m_length = buffersize
		self.m_table = WaveTable(wave, inits[0], inits[1])
		self.m_frequency = freq

	def samples(self):
		wanted = self.m_length
		self.m_buffer = numpy.zeros(self.m_length, dtype=self.m_type)

		if self.m_frequency < 20 or self.m_frequency > 20000:
			return pygame.sndarray.make_sound(self.m_buffer) # returning silence

		idx = 0
		while wanted > 0:
			self.m_buffer[idx] = self.m_table.at(self.m_pos)
			self.m_pos += self.m_frequency
			if (self.m_pos >= self.rate()):
				self.m_pos -= self.rate()
			wanted -= 1
			idx += 1
		return pygame.sndarray.make_sound(self.m_buffer)

	def set_frequency(self, frq):
		self.m_frequency = frq

	def frequency(self):
		return self.m_frequency

	def set_size(self, length):
		self.m_length = length

	def size(self):
		return self.m_length

	def rate(self):
		return self.m_table.sampleRate()

	def set_position(self, pos):
		""" No need for error checking, since it's taken care of by samples() """
		self.m_pos = pos

	def position(self):
		return self.m_pos


