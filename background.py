import os

import pygame

# constant images
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))

class Background:
    """ A class representing the background of the game """
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, settings):
        """ Initializes the background with constants and values from settings """
        self.y = settings.init_base
        self.x1 = 0
        self.x2 = self.WIDTH
        self.vel = settings.vel


    def move(self):
        """ A method to move the background to give the appearance of motion to the right """
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH


    def draw_bg(self, screen):
        """ A method to draw the background on the screen """
        screen.blit(BG_IMG, (0,0))


    def draw_base(self, screen):
        """ A method to draw the base on the screen """
        screen.blit(self.IMG, (self.x1, self.y))
        screen.blit(self.IMG, (self.x2, self.y))
