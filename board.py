import pygame
from field import Field

class Board:
    def __init__(self, start_x, start_y, rows, cols, field_size, field_border_size):
        self.start_x = start_x
        self.start_y = start_y
        self.rows = rows
        self.cols = cols
        self.field_size = field_size
        self.field_border_size = field_border_size
        self.fields = self.create_board()

    def create_board(self):
        fields = []
        for row in range(self.rows):
            fields_row = []
            for col in range(self.cols):
                cx = self.start_x + col * (self.field_size) + self.field_size // 2
                cy = self.start_y + row * (self.field_size) + self.field_size // 2
                field = Field((1, 1, 1), self.field_border_size, normal_color=(0, 128, 255), hover_color=(0, 200, 255), w=self.field_size, h=self.field_size, cx=cx, cy=cy)
                fields_row.append(field)
            fields.append(fields_row)
        return fields

    def draw(self, screen, hide_ships=False):
        for row in self.fields:
            for field in row:
                if hide_ships and field.occupied and not field.hit:
                    field.normal_color = (0, 128, 255)  # Hide the ship
                field.draw(screen)

    def check_hover(self, mouse_pos):
        for row in self.fields:
            for field in row:
                field.check_hover(mouse_pos)

    def check_click(self, mouse_pos, mouse_button_down):
        for row in self.fields:
            for field in row:
                if field.check_click(mouse_pos, mouse_button_down):
                    return field
        return None

    def can_place_ship(self, row, col, size, direction):
        if direction == 'H':
            if col + size > self.cols:
                return False
            for c in range(col, col + size):
                if self.fields[row][c].occupied:
                    return False
        else:
            if row + size > self.rows:
                return False
            for r in range(row, row + size):
                if self.fields[r][col].occupied:
                    return False
        return True

    def place_ship(self, row, col, size, direction, ship_positions):
        if direction == 'H':
            for c in range(col, col + size):
                self.fields[row][c].occupied = True
                self.fields[row][c].normal_color = (128, 128, 128)  # Change color to indicate ship placement
                ship_positions.append((row, c))
        else:
            for r in range(row, row + size):
                self.fields[r][col].occupied = True
                self.fields[r][col].normal_color = (128, 128, 128)  # Change color to indicate ship placement
                ship_positions.append((r, col))
