#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from locals import *


class Tuner( pygame.Surface ):
    """ 
        Tuner graphics
    """
    m_width = 216#213
    m_height = 48#40#33

    m_x_off = None #x-axis offset
    m_font = None
    m_line_height = 0

    font = None
    def __init__(self, path):
        pygame.Surface.__init__(self, (self.m_width,self.m_height), pygame.SRCALPHA, 32)

        self.image = pygame.Surface((self.m_width,self.m_height), pygame.SRCALPHA, 32)
        self.cursor = pygame.Surface((self.m_width,self.m_height), pygame.SRCALPHA, 32)

        rect = self.get_rect()
        self.center = rect.center #public

        #init font
        self.m_font = pygame.font.Font(path + "Actor-Regular.ttf", 10)
        self.m_line_height = self.m_font.get_height() - 3

        self.__labels() #labels

        #draw tuner
        for i in range(101):
            y_low = 4 * self.m_line_height + 1
            if i == 0 or i == 50 or i == 100:
                y_top =  2*self.m_line_height + 4
            elif i % 10 == 0:
                y_top =  2*self.m_line_height + 8
            else:
                y_top =  2*self.m_line_height + 11
            pygame.draw.aaline(self.image, (160,160,160), (i * 2 + self.m_x_off, y_top), (i * 2 + self.m_x_off, y_low))
        
        self.blit(self.image, (0,0))

    def __labels(self):
        """ create labels. Method also initiates the offset value for the line system. """
        
        cents =  self.m_font.render("CENTS", True, BLACK)
        cents_xp = self.center[0] - cents.get_rect().center[0]
        self.blit(cents, (cents_xp, 0))

        low = self.m_font.render("-50", True, BLACK)
        low_rect = self.blit(low, (0,self.m_line_height)) # rect needed for x-offset
        zero = self.m_font.render("0", True, BLACK)
        zero_xp = self.center[0] - zero.get_rect().center[0]  
        self.blit(zero, (zero_xp, self.m_line_height))
        high = self.m_font.render("50", True, BLACK)
        high_xp = self.m_width - high.get_rect()[2]
        self.blit(high, (high_xp, self.m_line_height))

        self.m_x_off = low_rect.center[0] - 1# offset for getting the line system centered


    def update(self, cents):
        #out of range marks as 50/-50
        if cents > 50: cents = 50
        elif cents < -50: cents = -50


        cents += 50 # offset

        xp = int(round(cents))*2 + self.m_x_off
        y_low = 4 * self.m_line_height + 5
        y_top = 2 * self.m_line_height + 7

        self.cursor.fill((0))
        pygame.draw.aaline(self.cursor, (0,0,0), (xp - 1, y_top), (xp + 2, y_top ))
        pygame.draw.aaline(self.cursor, (0,0,0), (xp, y_top + 1), (xp, y_low))
        pygame.draw.aaline(self.cursor, (0,0,0), (xp - 1, y_low), (xp + 2, y_low))

        self.fill(0)
        self.blit(self.image, (0,0))
        self.blit(self.cursor, (0,0))
        self.__labels()

    def get_width(self):
        return self.m_width

    def get_height(self):
        return self.m_height

    def get_size(self):
        return (self.m_width, self.m_width)


