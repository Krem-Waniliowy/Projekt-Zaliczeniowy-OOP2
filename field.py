import pygame
from tile import Tile

class Field(Tile):
    def __init__(self, border_color, border_width, normal_color, hover_color, w, h, cx, cy):
        super().__init__(border_color, border_width, normal_color, hover_color, w, h, cx, cy)
        self.occupied = False
        self.hit = False
        self.miss = False
        

    def draw(self, screen):
        super().draw(screen)
        if self.hit:
            pygame.draw.line(screen, (255, 0, 0), self.rect.topleft, self.rect.bottomright, 5)
            pygame.draw.line(screen, (255, 0, 0), self.rect.topright, self.rect.bottomleft, 5)
        elif self.miss:
            pygame.draw.circle(screen, (0, 0, 255), self.rect.center, self.width // 4, 5)

    def check_click(self, mouse_pos, mouse_button_down):
        if self.rect.collidepoint(mouse_pos) and mouse_button_down:
            if self.occupied:
                self.hit = True
            else:
                self.miss = True
            return True
        return False
