import pygame
from game import Game


pygame.init()
game = Game(pygame.display.set_mode((800, 600)))
game.run()
