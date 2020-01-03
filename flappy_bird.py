import os
import random
import sys
import time

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

import neat
import pygame

import game_functions as gf
from background import Background
from bird import Bird
from button import Button
from game_stats import GameStats
from pipes import Pipe
from scoreboard import Scoreboard
from settings import Settings

# declares global stats variable
stats = GameStats()

def main(genomes, config):
    """ Main driving function for Flappy Bird game """

    # initialize bird, pipes, background, game statistics, screen, and scoreboard
    settings = Settings()
    bird = Bird(settings)
    background = Background(settings)
    pipes = [Pipe(settings)]
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Flappy Bird')
    sb = Scoreboard(settings, screen, stats)
    buttons = []

    # create buttons if game is not active and ai is not active
    if not stats.game_active and not stats.ai_active:
        play_button = Button(settings, screen, 'Play', screen.get_rect().centerx, screen.get_rect().centery + 50)
        ai_button = Button(settings, screen, 'AI', screen.get_rect().centerx, screen.get_rect().centery + 110)
        buttons.append(play_button) 
        buttons.append(ai_button)

    # set variables for use by ai
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(settings))
        g.fitness = 0
        ge.append(g)

    # create clock to monitor fps
    clock = pygame.time.Clock()

    # main game loop
    run = True
    while run:
        # sets animation to 30fps
        clock.tick(30)

        # checks for any kind of pygame event (ie button push, mouse click, etc...)
        gf.check_events(bird, settings, screen, stats, sb, buttons)

        # checks if game is running
        if stats.game_active:

            # check if player is human
            if not stats.ai_active:
                # print('AI active:',stats.ai_active)
                pipes = gf.human_player(bird, pipes, stats, sb, settings)
            # conditional check for ai flag
            elif stats.ai_active:
                # print('AI active:',stats.ai_active)
                pipes = gf.ai_player(birds, pipes, stats, sb, settings, nets, ge)
                if pipes is False:
                    break

            # moves background to give appearance of flight
            background.move()

        # redraws screen with appropriate changes
        gf.update_screen(screen, bird, birds, pipes, background, settings, buttons, stats, sb)


def run(config_path):
    """ Method that configures neural network and prints simple statistics for each generation """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                    config_path)

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)