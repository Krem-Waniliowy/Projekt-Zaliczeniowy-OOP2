import pygame
import random
import sys
from button import Button
from board import Board

class Game:
    def __init__(self, screen):
        # USTAWIENIA GRY
        self.screen = screen # rozmiar jest określany w main.py
        self.rows, self.cols = 10, 10
        self.field_size = 40
        self.field_border_size = 2
        self.p_x, self.p_y = 50, 50
        self.c_x, self.c_y = 550, 50
        self.p_board = Board(self.p_x, self.p_y, self.rows, self.cols, self.field_size, self.field_border_size)
        self.c_board = Board(self.c_x, self.c_y, self.rows, self.cols, self.field_size, self.field_border_size)
        self.ship_types = {
            "Carrier": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Destroyer": 2
        }
        # TWORZENIE PRZYCISKÓW
        self.buttons = self.create_buttons()
        self.orientation_button = Button((0, 128, 255),(255, 0, 0), 150, 50, 600, 425,
                                         'Horizontal', (255, 255, 255), 20, 'Arial')

        self.selected_ship = None           # aktualnie wybrany statek
        self.selected_ship_size = 0         # rozmiar aktualnie wybranego statku
        self.selected_ship_direction = 'H'  # kierunek stawiania statku
        self.p_ships = []
        self.c_ships = []
        self.place_computer_ships()
        self.game_state = "PLACEMENT"
        self.player_turn = True
        self.orientation_button_pressed = False
        self.mouse_button_released = True
        self.placed_ships = set()

    def create_buttons(self):
        buttons = []
        x = 600
        y = 75
        gap = 60
        for ship_type in self.ship_types.keys():
            button = Button((0, 128, 255), (255, 0, 0), 150, 50, x, y,
                            ship_type, (255, 255, 255), 20, 'Arial')
            buttons.append(button)
            y += gap
        return buttons

    def place_computer_ships(self):
        for ship, size in self.ship_types.items():
            while True:
                direction = random.choice(['H', 'V'])
                if direction == 'H':
                    row = random.randint(0, self.rows - 1)
                    col = random.randint(0, self.cols - size)
                else:
                    row = random.randint(0, self.rows - size)
                    col = random.randint(0, self.cols - 1)
                if self.c_board.can_place_ship(row, col, size, direction):
                    self.c_board.place_ship(row, col, size, direction, self.c_ships)
                    break

    def placement_phase(self, mouse_pos, mouse_button_down):
        # najechanie i kliknięcie myszką na któryś z przycisków statków
        for button in self.buttons:
            button.check_hover(mouse_pos)
            if button.check_click(mouse_pos, mouse_button_down):
                self.selected_ship = button.text                                # pobiera nazwę statku
                self.selected_ship_size = self.ship_types[self.selected_ship]   # pobiera rozmiar statku

        # najechanie i kliknięcie na przycisk hover
        self.orientation_button.check_hover(mouse_pos)
        # sprawdzanie czy 'kliknięty' i zapobieganie wielokrotnemu kliknięciu (wielokrotny odczyt)
        if self.orientation_button.check_click(mouse_pos, mouse_button_down) and not self.orientation_button_pressed:
            self.orientation_button_pressed = True
            if self.selected_ship_direction == 'H':
                self.selected_ship_direction = 'V'
                self.orientation_button.text = 'Vertical'
            else:
                self.selected_ship_direction = 'H'
                self.orientation_button.text = 'Horizontal'

        # NIEPOTRZEBNY WARUNEK
        # if not mouse_button_down:
        #     self.orientation_button_pressed = False

        # przebieg stawiania statku
        for row in range(self.rows):
            for col in range(self.cols):
                field = self.p_board.fields[row][col]
                field.check_hover(mouse_pos)
                if self.selected_ship and field.check_click(mouse_pos, mouse_button_down) and self.selected_ship not in self.placed_ships:
                    if self.p_board.can_place_ship(row, col, self.selected_ship_size, self.selected_ship_direction):
                        self.p_board.place_ship(row, col, self.selected_ship_size, self.selected_ship_direction, self.p_ships)
                        self.disable_button(self.selected_ship)
                        self.placed_ships.add(self.selected_ship)
                        self.selected_ship = None

        # rysowanie planszy gracza
        self.p_board.draw(self.screen)

        # rysowanie przycisków statków
        for button in self.buttons:
            button.draw(self.screen)

        # rysowanie przycisku orientacji
        self.orientation_button.draw(self.screen)

        # jeżeli wszystkie statki umieszczone -> zmień fazę na grę
        if len(self.placed_ships) == len(self.ship_types):
            self.game_state = "GAME"

    def game_phase(self, mouse_pos, mouse_button_down):
        # TURA GRACZA
        if self.player_turn and mouse_button_down and self.mouse_button_released:
            field = self.c_board.check_click(mouse_pos, mouse_button_down)
            # sprawdza czy to faktycznie pole oraz (1. czy nie trafienie, 2. czy nie chybienie)
            if field and not field.hit and not field.miss:
                # update stanu pola
                field.hit = field.occupied      # jeśli było zajęte przez statek -> HIT
                field.miss = not field.occupied # jeśli nie było zajęte przez statek -> MISS
                self.player_turn = False        # skończyła się tura gracza
                # sprawdzenie zwycięstwa
                if self.check_victory(self.c_ships, self.c_board):
                    self.display_end_message("Wygrana!")
                    return

        # TURA KOMPUTERA (póki co głupia wersja)
        elif not self.player_turn:
            while not self.player_turn:
                # wybór losowego pola do trafienia
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                field = self.p_board.fields[row][col]
                # sprawdzenie czy już tam strzelano
                if not field.hit and not field.miss:
                    # update stanu pola
                    field.hit = field.occupied
                    field.miss = not field.occupied
                    self.player_turn = True # skończyła się tura komputera
                    # sprawdzenie przegranej
                    if self.check_victory(self.p_ships, self.p_board):
                        self.display_end_message("Przegrana!")
                        return
                    break

        self.p_board.draw(self.screen)
        self.c_board.draw(self.screen, True)

    def disable_button(self, ship):
        for button in self.buttons:
            if button.text == ship:
                button.normal_color = (128, 128, 128)
                button.hover_color = (128, 128, 128)
                button.current_color = (128, 128, 128)
                break

    def check_victory(self, ships, board):
        return all(board.fields[row][col].hit for row, col in ships)

    def display_end_message(self, message):
        self.screen.fill((255, 255, 255))
        font = pygame.font.SysFont('Arial', 50)
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    def run(self):
        # GŁÓWNA PĘTLA GRY
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_button_down = pygame.mouse.get_pressed()[0]
            mouse_button_up = not mouse_button_down

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))

            if self.game_state == "PLACEMENT":
                self.placement_phase(mouse_pos, mouse_button_down)
            elif self.game_state == "GAME":
                self.game_phase(mouse_pos, mouse_button_down)

            if not mouse_button_down:
                self.mouse_button_released = True
            else:
                self.mouse_button_released = False

            pygame.display.flip()

        pygame.quit()
        sys.exit()