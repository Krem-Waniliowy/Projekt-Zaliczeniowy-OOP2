import pygame
from tile import Tile

class Field(Tile):
    def __init__(self, border_color, border_size, normal_color, hover_color, w, h, cx, cy):
        super().__init__(normal_color, hover_color, w, h, cx, cy, border_color, border_size)
        self.occupied = False
        self.hit = False
        self.miss = False

    def draw(self, screen):
        self.current_color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.normal_color
        if self.hit:
            self.current_color = (255, 0, 0)
        elif self.miss:
            self.current_color = (255, 255, 255)
        super().draw(screen)