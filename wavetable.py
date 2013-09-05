#!/usr/bin/env/python
"""
	file:	wavetable.py
	topic:	WaveTable class

	author:	Mikael Svensson
	date:	2013-08-20
"""

import numpy

class WaveTable:
	""" 
		Wave tables in numpy array.
		Currently only supporty sine and square tables.

		TODO: Fix square wave pulse
	"""
	m_amp = 0
	m_scale = 2.0 * numpy.pi
	m_offset = 0
	m_rate = 0
	m_table = None

	def __init__(self, table='sine', sampleRate=44100, format=-16):
		if format == -16:
			dtype = numpy.iinfo(numpy.int16)
		elif format == 16:
			dtype = numpy.iinfo(numpy.uint16)
		elif format == -8:
			dtype = numpy.iinfo(numpy.int8)
		elif format == 8:
			dtype = numpy.iinfo(numpy.uint8)

		self.m_amp = (dtype.max - dtype.min)  / 2.0
		self.m_offset = dtype.max - self.m_amp

		self.m_rate = sampleRate

		self.m_table = numpy.zeros(self.m_rate, dtype=dtype)

		if table == 'sine':
			self.sine()
		elif table == 'square':
			self.square()
		else:
			print "invalid table type"
			#TODO: throw exception?

	def sine(self):
		_max = 0
		for i in range(self.m_rate):
			self.m_table[i] = int(self.m_amp * numpy.sin(self.m_scale * i/float(self.m_rate)) + self.m_offset)
			if self.m_table[i] > _max:
				_max = self.m_table[i]

	def square(self):
		arr = []
		for i in range(self.m_rate):
			self.m_table[i] = int(self.m_amp * numpy.sign(numpy.sin(self.m_scale * i/float(self.m_rate)) + self.m_offset))

	def sampleRate(self):
		return self.m_rate

	def dataType(self):
		return self.m_table.dtype

	def changeWave(self, table):
		if table == 'sine':
			self.sine()
		elif table == 'square':
			self.square()
		else:
			print "invalid table type"

	def table(self):
		return self.m_table

	def at(self, idx):
		try:
			return self.m_table[idx]
		except:
			print "WaveTable array out of range: " + str(idx)
			#TODO: throw exception?