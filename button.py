import pygame
from tile import Tile

class Button(Tile):
    def __init__(self, normal_color, hover_color, w, h, cx, cy, text, text_color, font_size, font_type):
        super().__init__(normal_color, hover_color, w, h, cx, cy)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(font_type, font_size)

    def draw(self, screen):
        # rysowanie kafelka z klasy bazowej
        super().draw(screen)
        # rysowanie tekstu na kafelku
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)