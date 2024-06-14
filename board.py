import pygame
from field import Field

class Board:
    def __init__(self, x, y, rows, cols, field_size, field_border_size):
        self.x = x # początek planszy x
        self.y = y # początek planszy y
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
                cx = self.x + col * (self.field_size) + self.field_size // 2
                cy = self.y + row * (self.field_size) + self.field_size // 2
                field = Field((0, 128, 255), (0, 200, 255), self.field_size, self.field_size, cx, cy, (0, 0, 0), self.field_border_size)
                fields_row.append(field) # dołączamy poszczególne pola (do listy reprezentującej rząd)
            fields.append(fields_row) # dołączamy poszczególne rzędy (do listy reprezentującej planszę)
        return fields

    def draw(self, screen, hide_ships=False):
        for row in self.fields:
            for field in row:
                # ukrywanie statków na planszy komputera
                # w przypadku gdy jest zajęte i nie trafione
                if hide_ships and field.occupied and not field.hit:
                    field.normal_color = (0, 128, 255)
                field.draw(screen)

    def check_hover(self, mouse_pos):
        for row in self.fields:
            for field in row:
                # czy 'nad' z klasy Tile
                field.check_hover(mouse_pos)

    def check_click(self, mouse_pos, mouse_button_down):
        for row in self.fields:
            for field in row:
                # czy 'kliknięte' z klasy Tile
                if field.check_click(mouse_pos, mouse_button_down):
                    return field # zwraca konkretne kliknięte pole
        return None

    def can_place_ship(self, row, col, size, direction):
        if direction == 'H':  # poziomo
            # czy mieści się na planszy
            if col + size > self.cols:
                return False
            for c in range(col, col + size):
                # czy pole jest zajęte
                if self.fields[row][c].occupied:
                    return False
        else:  # pionowo
            # czy mieści się na planszy
            if row + size > self.rows:
                return False
            # czy pole jest zajęte
            for r in range(row, row + size):
                if self.fields[r][col].occupied:
                    return False
        # jeżeli wszystko się zgadza to zwracamy Ture = statek może zostać umieszczony
        return True

    def place_ship(self, row, col, size, direction, ship_positions):
        if direction == 'H':  #  poziomo
            for c in range(col, col + size):
                # ustaw na zajęte
                self.fields[row][c].occupied = True
                # zmień kolor, żeby użytkownik wiedział że zajęte
                self.fields[row][c].normal_color = (128, 128, 128)
                ship_positions.append((row, c))
        else:  # pionowo
            for r in range(row, row + size):
                # ustaw na zajęte
                self.fields[r][col].occupied = True
                # zmień kolor, żeby użytkownik wiedział że zajęte
                self.fields[r][col].normal_color = (128, 128, 128)
                ship_positions.append((r, col))
