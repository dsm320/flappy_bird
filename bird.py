import os

import pygame

from settings import Settings

# constant images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))]

class Bird:
    """ A class representing the bird objects in the game """
    
    IMGS = BIRD_IMGS

    def __init__(self, settings):
        """ Initializes the bird with constants and values from settings """
        self.x = settings.init_bird_x
        self.y = settings.init_bird_y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]


    def reset(self, settings):
        """ A method to reset the bird object upon new game """
        self.__init__(settings)


    def jump(self):
        """ A method to move the bird object vertically when jumping """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y


    def move(self, settings):
        """ A method to move the bird object based on in-game action """
        self.tick_count += 1
        
        displacement = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        #terminal velocity
        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement -= 2

        if self.y > 1:
            self.y = self.y + displacement
        else:
            self.y = self.y + 10.5

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < settings.max_rotation:
                self.tilt = settings.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= settings.rotational_vel


    def draw(self, screen, settings):
        """ A method to draw a bird object on the screen """
        self.img_count += 1

        # cycles through bird images to give appearance of wings flapping
        if self.img_count < settings.animation_time:
            self.img = self.IMGS[0]
        elif self.img_count < settings.animation_time*2:
            self.img = self.IMGS[1]
        elif self.img_count < settings.animation_time*3:
            self.img = self.IMGS[2]
        elif self.img_count < settings.animation_time*4:
            self.img = self.IMGS[1]
        elif self.img_count == settings.animation_time*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = settings.animation_time*2

        # rotates image based on velocity and tilt
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)


    def get_mask(self):
        """ A method to get the mask of a bird image """
        return pygame.mask.from_surface(self.img)
