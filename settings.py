import pygame

pygame.font.init()

class Settings:
    """ A class to represent various settings for the game """

    def __init__(self):
        """ Initializes various constants to be used throughout the game """
        self.screen_width = 500
        self.screen_height = 800

        self.init_bird_x = 230
        self.init_bird_y = 350
        self.init_base = 730
        self.init_pipes = 600

        self.max_rotation = 25
        self.rotational_vel = 20
        self.animation_time = 5

        self.gap = 200
        self.vel = 5

        self.font = pygame.font.SysFont('Sans', 40)
