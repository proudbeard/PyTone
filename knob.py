#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import math
from shadows import *

class Knob( pygame.Surface ):
    """ 
        Knob class with some pygame mixer wrapper functionality for connecting audio to knob snaps.

        TODO:   Clean up, speed up.
                Rotate plate on/off
    """
    m_snap = False # snap degree
    m_limits = None # degree limits

    m_image = None # org image
    m_plate = None # top plate
    m_rot_image = None # the rotated image

    m_rect = None # surface rect  #exlude?
    m_center = None 

    m_angle = 0 #current degree   
    m_sound = None #sound fx

    m_shadow = False # shadow control
    m_shadow_offset = None
    m_shadow_alpha = None
    m_shadow_blur = None

    m_all_degrees = 0


    def __init__(self, image, snap_degree=1, limits=(360,360)):
        """ 
            image: a Surface object to be used as the knob

            snap_degree: nr of degrees to rotate in a snap_degree

            limits: (start, stop). Start at 0 needs to be 360
        """
        self.m_snap = snap_degree
        self.m_limits = limits

        #self.m_image = image.convert_alpha()
        self.m_image = image
        self.m_rot_image = self.m_image

        pygame.Surface.__init__(self, self.m_image.get_size(), pygame.SRCALPHA, 32)
        #store center for proper rotation
        self.m_rect = self.blit(self.m_image, (0,0))
        self.m_center = self.m_rect.center

    def check_limits(self, degrees):
        """ Check if in specified range"""
        degrees = degrees % 360

        if degrees < self.m_limits[0] and degrees > self.m_limits[1]:
            return False

        return True


    def snap(self, direction):
        """ snaps knob in clockwise or counter clockwise
            
            direction: string 'CW' or 'CCW'
        """
        #start with quantizing the current angle
        self.m_angle = int(self.m_snap * round(float(self.m_angle)/self.m_snap))

        if isinstance(direction,str):
            if direction.upper() == 'CW':
                self.rotate(self.m_angle + self.m_snap)
            elif direction.upper() == 'CCW':
                self.rotate((self.m_angle - self.m_snap))

    def get_snap(self):
        return self.m_snap

    def rotate(self, degrees, limits_off=False, sound=True):
        """ Rotates the knob """

        #degrees = degrees % 360 # remove?
        if not limits_off:
            if not self.check_limits(degrees):
                return False

        #play sound, if any
        if sound:
            if self.m_sound != None:
                self.play()

        self.m_angle = degrees % 360

        self.m_rot_image = pygame.transform.rotozoom(self.m_image, -degrees, 1)

        rot_rect = self.m_rot_image.get_rect(center=self.m_center)
        self.fill((0,0,0,0)) #clear

    
        #shadow will blit the original image
        if self.m_shadow:
            self.set_shadow(self.m_shadow_offset, self.m_shadow_alpha, self.m_shadow_blur)
        else:
            self.blit(self.m_rot_image, rot_rect)
            #if no shadow, plate must be redrawn here.
            if self.m_plate != None:
                self.blit(self.m_plate, self.m_plate_rect)

    def rotate_pos(self, center, pos):
        """ Rotate from a calculated degree from a center point """
        degree = math.degrees(math.atan2(center[1]-pos[1], center[0]-pos[0])) + 180
        if degree == 360.0:
            degree = 0
        self.rotate(degree, False, False)


    def set_sound(self, snd):
        self.m_sound = snd

    def get_sound(self):
        return self.m_sound

    def is_sound_loaded(self):
        return self.m_sound != None

    def play(self):
        if self.is_sound_loaded():
            self.m_sound.play()

    def set_volume(self, vol):
        if self.is_sound_loaded():
            self.m_sound.set_volume(vol)

    def degree(self):
        return self.m_angle % 360

    def set_plate(self, img):
        self.m_plate = img
        self.m_plate_rect = self.m_plate.get_rect()
        self.m_plate_rect.center = self.m_center
        self.blit(self.m_plate, self.m_plate_rect)

    def get_plate(self):
        return self.m_plate

    def get_rect(self):
        return self.m_image.get_rect()

    def set_shadow(self, offset=(0,0), alpha=240, blur=5):
        """ Adds a shadow to the knob. This might increase Surface size,
            depending on settings.

            offset: pixel offset
            alpha: alpha level
            blur: blur amount
        """
        #store settings
        self.m_shadow = True
        self.m_shadow_offset = offset
        self.m_shadow_alpha = alpha
        self.m_shadow_blur = blur

        #make shadow
        image = self.m_rot_image.convert_alpha()
        image = add_shadow(image, offset, alpha, blur)
        pygame.Surface.__init__(self, image.get_size(), pygame.SRCALPHA, 32)
        self.fill((0,0,0,0)) #clear

        # get center 
        image_center = self.m_center[0] + offset[0]/2.0 + blur/2.0, self.m_center[1] + offset[1]/2.0 + blur/2
        rect = image.get_rect(center=image_center)
        self.m_rect = self.blit(image, rect) #blit

        #redraw the plate
        if self.m_plate != None:
            self.blit(self.m_plate, self.m_plate_rect)

    def unset_shadow(self):
        self.m_shadow = False








