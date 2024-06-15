import pygame
import random
import sys
from button import Button
from board import Board


class Game:
    def __init__(self, screen):
        # USTAWIENIA GRY
        self.menu_size = (800, 600)
        self.game_size = (1000, 800)
        self.end_size = (800, 600)
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.rows, self.cols = 10, 10
        self.field_size = 40
        self.field_border_size = 2
        self.p_x, self.p_y = 50, 50
        self.c_x, self.c_y = 550, 50

        # UTWORZENIE PLANSZY GRACZA I KOMPUTERA
        self.p_board = Board(self.p_x, self.p_y, self.rows, self.cols, self.field_size, self.field_border_size)
        self.c_board = Board(self.c_x, self.c_y, self.rows, self.cols, self.field_size, self.field_border_size)

        # DEFINICJE STATKÓW
        self.ship_types = {
            "Carrier": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Destroyer": 2
        }

        # PRZYCISKI
        self.buttons = self.create_buttons()
        self.orientation_button = Button((0, 128, 255), (255, 0, 0), 150, 50, 600, 425,
                                         'Horizontal', (255, 255, 255), 20, 'Arial')
        self.main_menu_buttons = [
            Button((0, 128, 255), (255, 0, 0), 200, 50, 300, 200, 'Start', (255, 255, 255), 30, 'Arial'),
            Button((0, 128, 255), (255, 0, 0), 200, 50, 300, 300, 'Exit', (255, 255, 255), 30, 'Arial')
        ]
        self.end_screen_buttons = [
            Button((0, 128, 255), (255, 0, 0), 200, 50, 300, 200, 'Restart', (255, 255, 255), 30, 'Arial'),
            Button((0, 128, 255), (255, 0, 0), 200, 50, 300, 300, 'Exit', (255, 255, 255), 30, 'Arial')
        ]

        # INICJALIZACJA ZMIENNYCH GRY
        self.selected_ship = None
        self.selected_ship_size = 0
        self.selected_ship_direction = 'H'
        self.p_ships = []
        self.c_ships = []
        self.place_computer_ships()
        self.game_state = "MENU"
        self.player_turn = True
        self.orientation_button_pressed = False
        self.mouse_button_released = True
        self.placed_ships = set()

    def create_buttons(self):
        """
        Tworzy przyciski dla statków w fazie rozmieszczania statków.
        """
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
        """
        Losowo rozmieszcza statki komputera na planszy.
        """
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
        """
        Faza rozmieszczania statków przez gracza.
        """
        # Sprawdzenie kliknięć na przyciski wyboru statków
        for button in self.buttons:
            button.check_hover(mouse_pos)
            if button.check_click(mouse_pos, mouse_button_down):
                self.selected_ship = button.text
                self.selected_ship_size = self.ship_types[self.selected_ship]

        # Sprawdzenie kliknięcia na przycisk zmiany orientacji
        self.orientation_button.check_hover(mouse_pos)
        if self.orientation_button.check_click(mouse_pos, mouse_button_down) and not self.orientation_button_pressed:
            self.orientation_button_pressed = True
            if self.selected_ship_direction == 'H':
                self.selected_ship_direction = 'V'
                self.orientation_button.text = 'Vertical'
            else:
                self.selected_ship_direction = 'H'
                self.orientation_button.text = 'Horizontal'
        if not mouse_button_down:
            self.orientation_button_pressed = False

        # Rozmieszczanie statków na planszy
        for row in range(self.rows):
            for col in range(self.cols):
                field = self.p_board.fields[row][col]
                field.check_hover(mouse_pos)
                if self.selected_ship and field.check_click(mouse_pos, mouse_button_down) and self.selected_ship not in self.placed_ships:
                    if self.p_board.can_place_ship(row, col, self.selected_ship_size, self.selected_ship_direction):
                        self.p_board.place_ship(row, col, self.selected_ship_size, self.selected_ship_direction,
                                                self.p_ships)
                        self.disable_button(self.selected_ship)
                        self.placed_ships.add(self.selected_ship)
                        self.selected_ship = None

        # Rysowanie planszy i przycisków
        self.p_board.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        self.orientation_button.draw(self.screen)

        # Zmiana stanu gry na "GAME", gdy wszystkie statki są rozmieszczone
        if len(self.placed_ships) == len(self.ship_types):
            self.game_state = "GAME"
            self.change_window_size(self.game_size)

    def game_phase(self, mouse_pos, mouse_button_down):
        """
        Faza główna gry - naprzemienne strzelanie gracza i komputera.
        """
        if self.player_turn and mouse_button_down and self.mouse_button_released:
            # Sprawdzenie kliknięcia na planszę komputera
            field = self.c_board.check_click(mouse_pos, mouse_button_down)
            if field and not field.hit and not field.miss:
                field.hit = field.occupied
                field.miss = not field.occupied
                self.player_turn = False
                # Sprawdzenie wygranej gracza
                if self.check_victory(self.c_ships, self.c_board):
                    self.game_state = "END"
                    self.end_message = "Wygrana!"
                    self.change_window_size(self.end_size)
                    return

        elif not self.player_turn:
            # Ruch komputera
            while not self.player_turn:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                field = self.p_board.fields[row][col]
                if not field.hit and not field.miss:
                    field.hit = field.occupied
                    field.miss = not field.occupied
                    self.player_turn = True
                    # Sprawdzenie wygranej komputera
                    if self.check_victory(self.p_ships, self.p_board):
                        self.game_state = "END"
                        self.end_message = "Przegrana!"
                        self.change_window_size(self.end_size)
                        return
                    break

        # Rysowanie plansz
        self.p_board.draw(self.screen)
        self.c_board.draw(self.screen, True)

    def disable_button(self, ship):
        """
        Wyłącza przycisk statku po jego rozmieszczeniu (wizualne wyszarzenie).
        """
        for button in self.buttons:
            if button.text == ship:
                button.normal_color = (128, 128, 128)
                button.hover_color = (128, 128, 128)
                button.current_color = (128, 128, 128)
                break

    def check_victory(self, ships, board):
        """
        Sprawdza, czy wszystkie pola z rozmieszczonymi statkami zostały trafione.
        """
        return all(board.fields[row][col].hit for row, col in ships)

    def main_menu(self, mouse_pos, mouse_button_down):
        """
        Wyświetla główne menu gry.
        """
        self.screen.fill((255, 255, 255))
        for button in self.main_menu_buttons:
            button.check_hover(mouse_pos)
            if button.check_click(mouse_pos, mouse_button_down):
                if button.text == 'Start':
                    self.game_state = "PLACEMENT"
                    self.change_window_size(self.game_size)
                elif button.text == 'Exit':
                    pygame.quit()
                    sys.exit()
            button.draw(self.screen)

    def end_screen(self, mouse_pos, mouse_button_down):
        """
        Wyświetla ekran końcowy gry z opcjami restartu lub wyjścia.
        """
        self.screen.fill((255, 255, 255))

        # Wyświetlanie komunikatu o wyniku gry
        font = pygame.font.SysFont('Arial', 50)
        text_surface = font.render(self.end_message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, 150))
        self.screen.blit(text_surface, text_rect)

        # Wyświetlanie przycisków
        for button in self.end_screen_buttons:
            button.check_hover(mouse_pos)
            if button.check_click(mouse_pos, mouse_button_down):
                if button.text == 'Restart':
                    self.__init__(self.screen)
                    self.game_state = "PLACEMENT"
                    self.change_window_size(self.game_size)
                elif button.text == 'Exit':
                    pygame.quit()
                    sys.exit()
            button.draw(self.screen)

    def change_window_size(self, new_size):
        """
        Zmienia rozmiar okna gry.
        """
        pygame.display.set_mode(new_size)

    def run(self):
        """
        Główna pętla gry.
        """
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_button_down = pygame.mouse.get_pressed()[0]
            mouse_button_up = not mouse_button_down

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))

            # obsługa stanu gry
            if self.game_state == "MENU":
                self.main_menu(mouse_pos, mouse_button_down)
            elif self.game_state == "PLACEMENT":
                self.placement_phase(mouse_pos, mouse_button_down)
            elif self.game_state == "GAME":
                self.game_phase(mouse_pos, mouse_button_down)
            elif self.game_state == "END":
                self.end_screen(mouse_pos, mouse_button_down)

            # aktualizacja stanu myszy
            if not mouse_button_down:
                self.mouse_button_released = True
            else:
                self.mouse_button_released = False

            self.clock.tick(self.FPS)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
