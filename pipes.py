import os
import random

import pygame

# constant image
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))

class Pipe:
    """ A class to represent a pair of pipe objects in the game """

    def __init__(self, settings):
        """ Initializes the pipes with constants and values from settings """
        self.x = settings.init_pipes
        self.height = 0
        self.gap = settings.gap
        self.vel = settings.vel

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()


    def set_height(self):
        """ A method to set the height of the pipes randomly """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap


    def move(self):
        """ A method to move the pipes across the screen """
        self.x -= self.vel


    def draw(self, screen):
        """ A method to draw a pair of pipe objects on the screen"""
        screen.blit(self.PIPE_TOP, (self.x, self.top))
        screen.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird):
        """ A method to check for collision between pipe masks and bird mask """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False
