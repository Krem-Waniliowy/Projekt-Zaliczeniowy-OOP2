import pygame
from tile import Tile


class Field(Tile):
    def __init__(self, normal_color, hover_color, w, h, cx, cy, border_color, border_width):
        super().__init__(normal_color, hover_color, w, h, cx, cy, border_color, border_width)
        self.occupied = False
        self.hit = False
        self.miss = False
        self.highlight_ship = False

    def draw(self, screen):
        self.check_hover(pygame.mouse.get_pos())
        if self.hit:
            self.current_color = (255, 0, 0)
        elif self.miss:
            self.current_color = (255, 255, 255)
        elif self.highlight_ship:
            self.current_color = (255, 255, 0)
        super().draw(screen)
