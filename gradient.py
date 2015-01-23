#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import pygame

class Gradient( pygame.Surface ):
    """ 
        Gradient Surface class.
        Modified from dr0id' s gradients package
        http://www.pygame.org/projects/9/307/
    """
    m_size = None
    m_start = None
    m_end = None
    m_grad = None


    def __init__(self, dimension, startcolor=(255,255,255,255), endcolor=(0,0,0,255)):
        """ 
            dimension: Surface dimension

            startcolor: Gradients start color (top)

            endcolor: Gradients end color (bottom)
        """
        pygame.Surface.__init__(self, dimension, pygame.SRCALPHA, 32)
        self.m_size = dimension
        self.m_start = startcolor
        self.m_end = endcolor
        self.vertical()
        self.clear()

    def vertical(self):
        """
        Draws a vertical linear gradient filling the entire surface. Returns a
        surface filled with the gradient (numeric is only 2-3 times faster).
        """
        height = self.m_size[1]
        bigSurf = pygame.Surface((1,height)).convert_alpha()
        dd = 1.0/height
        sr, sg, sb, sa = self.m_start
        er, eg, eb, ea = self.m_end
        rm = (er-sr)*dd
        gm = (eg-sg)*dd
        bm = (eb-sb)*dd
        am = (ea-sa)*dd
        for y in range(height):
            bigSurf.set_at((0,y),
                            (int(sr + rm*y),
                             int(sg + gm*y),
                             int(sb + bm*y),
                             int(sa + am*y))
                          )
        self.m_grad = pygame.transform.scale(bigSurf, self.m_size)

    def clear(self):
        self.blit(self.m_grad,(0,0))

    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self,(0,0))
        pygame.display.flip() #flippin here as well to keep screen up to date

    def setColors(self, start, end):
        """ Sets start color and clears surface """
        self.m_start = start
        self.m_end = end
        self.vertical()
        self.clear()

    def fadeOut(self, time, end=255):
        """ 
            Fades in a new gradient layer by increasing alpha from 0 to end.
            Previous colors will still be used after fade end.

            time: fade time in milliseconds ( not very precise.... )
            end:    alpha end value

            TODO: Add curve for the fade and more precise timing
        """
        old_start = self.m_start
        old_end = self.m_end
        new_start = ()
        new_end = ()

        for i in range(end):
            new_start = (self.m_start[0], self.m_start[1], self.m_start[2], i)
            new_end = (self.m_end[0], self.m_end[1], self.m_end[2], i)
            self.setColors(new_start, new_end)
            self.draw()
            pygame.time.delay(int(time/end))

        self.setColors(old_start, old_end)
        self.draw()









