#!/usr/bin/env/python
#-*- coding: utf-8 -*-
"""
    topic:  Shadow effects taken from the Fallen Spire util.py
            https://code.google.com/p/fallenspire/
    os:     Mac OS X 10.7.5

    author: -
    date:   2013-08-26
"""

# Copyright (C) 2009, Peter Rogers
#
# This file is part of Fallen Spire.
#
# Fallen Spire is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fallen Spire is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fallen Spire.  If not, see <http://www.gnu.org/licenses/>.
#


import pygame
import numpy

def soften_surf(orig, n=1):
    rgbarray = pygame.surfarray.pixels_alpha(orig).astype("int")
    surf = numpy.array(rgbarray)
    surf[n:,:]  += rgbarray[:-n,:]*8
    surf[:-n,:] += rgbarray[n:,:]*8
    surf[:,n:]  += rgbarray[:,:-n]*8
    surf[:,:-n] += rgbarray[:,n:]*8
    surf /= 33
    #surf = pygame.surfarray.make_surface(surf).convert_alpha()
    pygame.surfarray.pixels_alpha(orig)[:] = surf
    return orig

# Adds an empty border around the given surface
def pad_surf(surf, size):
    (w, h) = surf.get_size()
    newsurf = pygame.Surface((w+size[0], h+size[1])).convert_alpha()
    newsurf.fill((0,0,0,0))
    #r = surf.get_rect()
    #r.center = newsurf.get_rect().center
    newsurf.blit(surf, (size[0]/2, size[1]/2))
    return newsurf

def blur_surf(surf, amount=5):
    for n in xrange(amount):
        surf = soften_surf(surf, n=2)
    return surf

def adjust_alpha(img, amount):
    if (type(amount) == int and amount == 255):
        # Nothing to do
        return
    if (isinstance(amount, pygame.Surface)):
        # Extract the alpha channel from the given surface
        amount = pygame.surfarray.pixels_alpha(amount)

    alpha = pygame.surfarray.pixels_alpha(img)
    alpha = (alpha*(amount/255.0))
    alpha = numpy.clip(alpha, 0, 255)
    pygame.surfarray.pixels_alpha(img)[:] = alpha.astype("uint8")
    newsurf = img.copy()
    pygame.surfarray.pixels_alpha(newsurf)[:] = alpha
    return newsurf

# Returns a surface filled with the given color, but having the same
# alpha channel as the given image.
def set_color(img, color):
    newsurf = pygame.Surface(img.get_size()).convert_alpha()
    newsurf.fill(color)
    alpha = pygame.surfarray.pixels_alpha(img)
    pygame.surfarray.pixels_alpha(newsurf)[:] = alpha
    if (len(color) == 4):
        adjust_alpha(newsurf, color[-1])
    return newsurf

# Renders a nice shadow for the given image
def add_shadow(surf, offset, alpha=240, blur=5):
    shadow = set_color(surf, (0,0,0))
    adjust_alpha(shadow, alpha)
    shadow = blur_surf(pad_surf(shadow, (blur,blur)), amount=blur)
    dest = pygame.Surface((
            max(shadow.get_width(), surf.get_width())+abs(offset[0]), 
            max(shadow.get_height(), surf.get_height())+abs(offset[1])))
    dest = dest.convert_alpha()
    dest.fill((0,0,0,0))

    if (offset[0] > 0):
        xp = offset[0]
    else:
        xp = 0
    if (offset[1] > 0):
        yp = offset[1]
    else:
        yp = 0

    dest.blit(shadow, (xp, yp))
    dest.blit(surf, (dest.get_width()-xp-shadow.get_width(),
                     dest.get_height()-yp-shadow.get_height()))

    return dest