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
        self.board = self.create_board()

    def create_board(self):
        board = []
        for row in range(self.rows):
            board_row = []
            for col in range(self.cols):
                cx = self.x + col * (self.field_size) + self.field_size // 2
                cy = self.y + row * (self.field_size) + self.field_size // 2
                field = Field((0, 128, 255), (0, 0, 0), self.field_size, self.field_size, cx, cy,
                              (0, 0, 0), self.field_border_size)
                board_row.append(field) # dołączamy poszczególne pola (do listy reprezentującej rząd)
            board.append(board_row) # dołączamy poszczególne rzędy (do listy reprezentującej planszę)
        return board

    def draw(self, screen, hide_ships=False):
        for row in self.board:
            for field in row:
                # ukrywanie statków na planszy komputera
                if hide_ships and field.occupied and not field.hit:
                    field.normal_color = (0, 128, 255)
                field.draw(screen)

    def check_hover(self, mouse_pos, selected_ship_size, selected_ship_orientation):
        for row in self.board:
            for field in row:
                field.check_hover(mouse_pos)
                field.highlight_ship = False

        # podświetlanie kładzionego statku
        if selected_ship_size > 0:
            for row in range(self.rows):
                for col in range(self.cols):
                    field = self.board[row][col]
                    if field.rect.collidepoint(mouse_pos):
                        # czy nie wychodzi poza planszę
                        if selected_ship_orientation == 'H' and not col + selected_ship_size > self.cols:
                            # czy nie zajęte przez statki
                            if all(not self.board[row][c].occupied for c in range(col, col + selected_ship_size)):
                                for c in range(col, col + selected_ship_size):
                                    self.board[row][c].highlight_ship = True
                        elif selected_ship_orientation == 'V' and not row + selected_ship_size > self.rows:
                            if all(not self.board[r][col].occupied for r in range(row, row + selected_ship_size)):
                                for r in range(row, row + selected_ship_size):
                                    self.board[r][col].highlight_ship = True

    def check_click(self, mouse_pos, mouse_button_down):
        for row in self.board:
            for field in row:
                if field.check_click(mouse_pos, mouse_button_down):
                    return field # zwraca konkretne kliknięte pole

    def can_place_ship(self, row, col, size, direction):
        if direction == 'H':
            # czy nie wychodzi poza planszę
            if col + size > self.cols:
                return False
            # czy pola nie są zajęte przez statek
            return all(not self.board[row][c].occupied for c in range(col, col + size))
        else:
            if row + size > self.rows:
                return False
            return all(not self.board[r][col].occupied for r in range(row, row + size))

    # dołącza do przekazanej w parametrach funkcji listy 'ship_positions' współrzędne zajętego przez statek pola
    def place_ship(self, row, col, size, direction, ship_positions):
        if not self.can_place_ship(row, col, size, direction):
            return False
        if direction == 'H':
            for c in range(col, col + size):
                # ustaw na zajęte
                self.board[row][c].occupied = True
                # zmień kolor
                self.board[row][c].normal_color = (128, 128, 128)
                ship_positions.append((row, c))
        else:
            for r in range(row, row + size):
                self.board[r][col].occupied = True
                self.board[r][col].normal_color = (128, 128, 128)
                ship_positions.append((r, col))
        return True
