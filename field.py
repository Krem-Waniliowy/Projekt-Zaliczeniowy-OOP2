import pygame
from tile import Tile

class Field(Tile):
    def __init__(self, normal_color, hover_color, w, h, cx, cy, border_color, border_width):
        super().__init__(normal_color, hover_color, w, h, cx, cy, border_color, border_width)
        self.occupied = False
        self.hit = False
        self.miss = False

    def draw(self, screen):
        # sprawdzanie czy 'nad' z klasy bazowej
        self.check_hover(pygame.mouse.get_pos())
        # jeśli trafiono statek -> zmień kolor na czerwony
        if self.hit:
            self.current_color = (255, 0, 0)
        # jeśli trafiono wodę -> zmień kolor na biały
        elif self.miss:
            self.current_color = (255, 255, 255)
        # rysowanie kafelka z klasy bazowej
        super().draw(screen)