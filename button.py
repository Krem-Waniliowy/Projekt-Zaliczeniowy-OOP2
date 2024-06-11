import pygame
from tile import Tile

class Button(Tile):
    def __init__(self, border_color, border_width, normal_color, hover_color, w, h, cx, cy, text, text_color, font_size, font_type):
        super().__init__(border_color, border_width, normal_color, hover_color, w, h, cx, cy)
        self.text = str(text)
        self.text_color = text_color
        self.font_size = font_size
        self.font_type = font_type
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)


    def draw(self, screen):
        # dziedziczenie z tile
        super().draw(screen)
        # część z button
        screen.blit(self.text_surf, self.text_rect)


    def check_click(self, mouse_pos, mouse_button_down):
        if self.rect.collidepoint(mouse_pos) and mouse_button_down:
            return True
        return False
    