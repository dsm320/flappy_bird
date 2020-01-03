import os
import sys

import neat
import pygame

from bird import Bird
from pipes import Pipe
from settings import Settings


def update_screen(screen, bird, birds, pipes, background, settings, buttons, stats, sb):
    """ Method that redraws screen to reflect changes in object positions """
    background.draw_bg(screen)

    for pipe in pipes:
        pipe.draw(screen)

    background.draw_base(screen)
    
    sb.show_score()

    if stats.ai_active:
        sb.show_ai_stats()

        for bird in birds:
            bird.draw(screen, settings)
    else:
        bird.draw(screen, settings)

    if not stats.game_active:
        for button in buttons:
            button.draw_button()

    pygame.display.update()


def check_keydown_events(event, settings, screen, bird, stats):
    """ Method that checks if key has been pressed and takes appropriate action """
    if event.key == pygame.K_SPACE:
        bird.jump()
    elif event.key == pygame.K_q:
        sys.exit()


def check_events(bird, settings, screen, stats, sb, buttons=None):
    """ Method that checks if any pygame events have occured and takes appropriate action """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, bird, stats)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, buttons[0], mouse_x, mouse_y)
            check_ai_button(settings, screen, stats, sb, buttons[1], mouse_x, mouse_y)


def check_play_button(settings, screen, stats, sb, play_button, mouse_x, mouse_y):
    """ Method that checks if play button has been clicked """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True
        stats.ai_active = False

        sb.prep_score()
        sb.prep_high_score()


def check_ai_button(settings, screen, stats, sb, ai_button, mouse_x, mouse_y):
    """ Method that checks if play button has been clicked """
    button_clicked = ai_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True
        stats.ai_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_gen_count()
        sb.prep_bird_count()


def check_high_score(stats, sb):
    """ Method that compares current score to highscore and overwrites if necessary """
    if stats.score >  stats.high_score:
        stats.high_score = stats.score
        with open('highscore.txt', 'w') as file_object:
            file_object.write(str(stats.high_score))
        sb.prep_high_score()


def check_ground_collision(stats, bird, settings):
    """ Method that checks for bird and ground collision """
    if bird.y + bird.img.get_height() >= settings.init_base:
        stats.game_active = False
        bird = bird.reset(settings)
        pygame.mouse.set_visible(True)
        print("Game over - ground collision")
        print("  Score: " + str(stats.score))
        return True
        

def check_pipe_collision(stats, bird, pipe, settings):
    """ Method that checks for bird and pipe collision """
    if pipe.collide(bird):
        stats.game_active = False
        bird = bird.reset(settings)
        pygame.mouse.set_visible(True)
        print("Game over - pipe collision")
        print("  Score: " + str(stats.score))
        return True


def add_pipe(stats, sb, bird, pipe, pipes, settings):
    """ Method that adds pipe off screen to right and increases score """
    if not pipe.passed and pipe.x < bird.x:
        pipe.passed = True
        stats.score += 1
        sb.prep_score()
        pipes.append(Pipe(settings))


def remove_pipe(pipes):
    """ Method that removes pipe off screen to left """
    for pipe in pipes:
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            pipes.remove(pipe)
    

def ai_player(birds, pipes, stats, sb, settings, nets, ge):
    """ Method that runs ai to play flappy bird """
    # keeps track of pipe infront of bird
    pipe_ind = 0

    stats.bird_count = len(birds)
    sb.prep_bird_count()
    if len(birds) > 0:
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1
    else:
        # resets after failed generation
        pipes.clear()
        pipes = [Pipe(settings)]
        stats.gen_count += 1
        stats.score = 0
        return False

    # moves every bird and increases their fitness based on time survived
    for x, bird in enumerate(birds):
        bird.move(settings)
        ge[x].fitness += 0.1

        output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

        # determines if bird should jump based on outputs of neural network
        if output[0] > 0.5:
            bird.jump()
            # print('Bird', x, 'should jump here\n')

    # if bird collides with pipe, decrease fitness and remove bird
    for pipe in pipes:
        for x, bird in enumerate(birds):
            if pipe.collide(bird):
                # print('Bird', x, 'collided with pipe')
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        add_pipe(stats, sb, bird, pipe, pipes, settings)
        pipe.move()

    remove_pipe(pipes)

    # if bird collides with ground, remove bird but leave fitness unchanged
    for x, bird in enumerate(birds):
        if bird.y + bird.img.get_height() >= settings.init_base:
            birds.pop(x)
            nets.pop(x)
            ge.pop(x)

    # terminates if best bird exceeds 50 pipes passed
    if stats.score > 50:
        return False

    return pipes


def human_player(bird, pipes, stats, sb, settings):
    """ Method that handles keyboard input from human player """
    bird.move(settings)

    # checks for bird collision with ground
    if check_ground_collision(stats, bird, settings):
        pipes.clear()
        pipes = [Pipe(settings)]

    for pipe in pipes:
        # checks for bird collision with pipes
        if check_pipe_collision(stats, bird, pipe, settings):
            pipes.clear()
            pipes = [Pipe(settings)]

        # adds a new pipe off screen to right and moves into view
        add_pipe(stats, sb, bird, pipe, pipes, settings)
        pipe.move()

        # checks if new score is greater than current highscore
        check_high_score(stats, sb)

    # removes pipes off screen to left
    remove_pipe(pipes)

    return pipes