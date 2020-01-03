import pygame.font


class Scoreboard:
    """ A class to represent a scoreboard in the game """

    def __init__(self, settings, screen, stats):
        """ Initializes a scoreboard object with constants and values from settings """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.text_color = (30, 30, 30)
        self.font = settings.font

        self.prep_score()
        self.prep_high_score()
        self.prep_gen_count()
        self.prep_bird_count()


    def prep_score(self):
        """ A method to render the current score in the top right corner of the screen """
        self.score_image = self.font.render('Score: ' + str(self.stats.score), 1, (255, 255, 255))
        
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.right - 5 - self.score_image.get_width()
        self.score_rect.top = 20


    def prep_high_score(self):
        """ A method to render the highscore in the top left corner of the screen """
        self.high_score_image = self.font.render('Highscore: ' + str(self.stats.high_score), 1 , (255, 255, 255))

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left + 5
        self.high_score_rect.top = self.score_rect.top


    def prep_gen_count(self):
        """ A method to render current generation of the neural network """
        self.gen_text = self.font.render('Gen: ' + str(self.stats.gen_count), 1, (255, 255, 255))
        
        self.gen_rect = self.gen_text.get_rect()
        self.gen_rect.centerx = self.screen.get_width() / 3
        self.gen_rect.top = 60

    def prep_bird_count(self):
        """ A method to render the current number of living birds """
        self.birds_text = self.font.render('Birds: ' + str(self.stats.bird_count), 1, (255, 255, 255))

        self.birds_rect = self.birds_text.get_rect()
        self.birds_rect.centerx = self.screen.get_width() / 3 * 2
        self.birds_rect.top = self.gen_rect.top
        

    def show_ai_stats(self):
        """ A method to draw the current ai generation and bird count on the screen """
        self.screen.blit(self.gen_text, self.gen_rect)
        self.screen.blit(self.birds_text, self.birds_rect)


    def show_score(self):
        """ A method to draw the current score and highscore on the screen """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
