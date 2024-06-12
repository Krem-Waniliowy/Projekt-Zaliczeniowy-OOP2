import pygame

class Tile:
    def __init__(self, normal_color, hover_color, w, h, cx, cy, border_color=(0, 0, 0), border_width=2):
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.width = w
        self.height = h
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (cx, cy)
        self.border_color = border_color
        self.border_width = border_width
        self.current_color = normal_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.normal_color

    def check_click(self, mouse_pos, mouse_button_down):
        if self.rect.collidepoint(mouse_pos) and mouse_button_down:
            return True
        return False