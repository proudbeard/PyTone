#!/usr/bin/env/python
#-*- coding: utf-8 -*-
"""
	topic:	Musical intervals
	os:		Mac OS X 10.7.5

	author:	Mikael Svensson
	date:	2013-08-25
"""

import random

class Interval:
	""" Interval class to keep track of intervals """
	m_intervals = ['UNISON', 'MINOR SECOND', 'MAJOR SECOND', 'MINOR THIRD', 'MAJOR THIRD',
					'PERFECT FOURTH', 'AUGMENTED FORTH', 'PERFECT FIFTH', 'MINOR SIXTH',
					'MAJOR SIXTH', 'MINOR SEVENTH', 'MAJOR SEVENTH', 'PERFECT OCTAVE',
					'MINOR 9th', 'MAJOR 9th', 'MINOR 10th', 'MAJOR 10th', 'PERFECT 11th',
					'AUGMENTED 11th', 'PERFECT 12th', 'MINOR 13th', 'MAJOR 13th', 'MINOR 14th', 'MAJOR 14th',
					'DOUBLE OCTAVE']
	m_length = len(m_intervals)
	
	def __init__(self):
		pass

	def random(self, max_idx=m_length-1):
		if max_idx > self.m_length-1:
			max_idx = self.m_length-1

		rand_nr = random.randint(0, max_idx)
		return self.m_intervals[rand_nr]
	def at(self, idx):
		""" Returns interval string
			idx: number of steps from unison
		"""
		if idx > self.m_length:
			return False
		return self.m_intervals[idx]


	def length(self):
		return self.m_length





