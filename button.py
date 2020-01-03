import pygame


class Button:
    """ A class to represent a basic button with text """

    def __init__(self, settings, screen, msg, x, y):
        """ Initializes the button with constants and values from settings"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200,50
        self.button_color = (0, 200, 0)
        self.text_color = (255, 255, 255)
        self.font = settings.font

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = x
        self.rect.centery = y

        self.prep_msg(msg)


    def prep_msg(self, msg):
        """ A method to render a text message in the center of a button object """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        """ A method to draw a button object on the screen"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
