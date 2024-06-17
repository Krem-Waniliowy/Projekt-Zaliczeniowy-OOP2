import pygame
from game import Game


pygame.init()
screen = pygame.display.set_mode((800, 600))
game = Game(screen)
game.run()