import pygame
import sys
from game import Game

pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Battleship")

game = Game(screen)
game.run()