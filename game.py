import pygame
import random
import sys
from button import Button
from board import Board


class Game:
    def __init__(self, screen):
        # USTAWIENIA GRY
        self.end_size = (800, 600)
        self.game_size = (1000, 500)
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.rows, self.cols = 10, 10
        self.field_size = 40
        self.field_border_size = 2
        self.p_x, self.p_y = 50, 50
        self.c_x, self.c_y = 550, 50

        # PLANSZA GRACZA I KOMPUTERA
        self.player_board = Board(self.p_x, self.p_y, self.rows, self.cols, self.field_size, self.field_border_size)
        self.computer_board = Board(self.c_x, self.c_y, self.rows, self.cols, self.field_size, self.field_border_size)

        self.ships = {
            "Carrier": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Destroyer": 2
        }

        # PRZYCISKI
        self.buttons = self.create_buttons()
        self.orientation_button = Button((0, 128, 255), (255, 0, 0), 150, 50, 600, 425,'Horizontal', (255, 255, 255), 20, 'Arial')
        self.menu_screen_buttons = [
            Button((0, 128, 255), (255, 0, 0), 200, 50, 400, 250, 'Start', (255, 255, 255), 30, 'Arial'),
            Button((0, 128, 255), (255, 0, 0), 200, 50, 400, 350, 'Exit', (255, 255, 255), 30, 'Arial')
        ]
        self.end_screen_buttons = [
            Button((0, 128, 255), (255, 0, 0), 200, 50, 400, 250, 'Restart', (255, 255, 255), 30, 'Arial'),
            Button((0, 128, 255), (255, 0, 0), 200, 50, 400, 350, 'Exit', (255, 255, 255), 30, 'Arial')
        ]

        # ZMIENNE GRY
        self.selected_ship = None
        self.selected_ship_size = 0
        self.selected_ship_direction = 'H'
        self.player_ships = []
        self.computer_ships = []
        self.game_state = "MENU"
        self.player_turn = True
        self.mouse_button_released = True
        self.placed_ships = set()
        # cele dla komputera
        self.targets = []

        # ROZMIESZCZENIE STATKÓW KOMPUTERA
        self.place_computer_ships()

    def create_buttons(self):
        buttons = []
        x = 600
        y = 75
        gap = 60
        for ship in self.ships.keys():
            button = Button((0, 128, 255), (255, 0, 0), 150, 50, x, y, ship, (255, 255, 255), 20, 'Arial')
            buttons.append(button)
            y += gap
        return buttons

    # losowe rozmieszczenie statków
    def place_computer_ships(self):
        for ship, size in self.ships.items():
            while True:
                direction = random.choice(['H', 'V'])
                if direction == 'H':
                    row = random.randint(0, self.rows - 1)
                    col = random.randint(0, self.cols - size)
                else:
                    row = random.randint(0, self.rows - size)
                    col = random.randint(0, self.cols - 1)
                # jeżeli place_ship zwróci True to kończymy pętlę while
                if self.computer_board.place_ship(row, col, size, direction, self.computer_ships):
                    break

    def place_player_ships(self, mouse_pos, mouse_button_down):
        # kliknięcie na wybór statku
        for button in self.buttons:
            button.check_hover(mouse_pos)
            if button.check_click(mouse_pos, mouse_button_down) and self.mouse_button_released:
                self.selected_ship = button.text
                self.selected_ship_size = self.ships[self.selected_ship]

        # kliknięcie na wybór orientacji
        self.orientation_button.check_hover(mouse_pos)
        if self.orientation_button.check_click(mouse_pos, mouse_button_down) and self.mouse_button_released:
            if self.selected_ship_direction == 'H':
                self.selected_ship_direction = 'V'
            else:
                self.selected_ship_direction = 'H'
            if self.selected_ship_direction == 'V':
                self.orientation_button.text = 'Vertical'
            else:
                self.orientation_button.text = 'Horizontal'

        # rozmieszczanie statków jeżeli mamy jakiś wybrany
        if self.selected_ship:
            for row in range(self.rows):
                for col in range(self.cols):
                    field = self.player_board.board[row][col]
                    field.check_hover(mouse_pos)
                    if field.check_click(mouse_pos, mouse_button_down) and self.selected_ship not in self.placed_ships:
                        if self.player_board.place_ship(row, col, self.selected_ship_size, self.selected_ship_direction, self.player_ships):
                            self.disable_button(self.selected_ship)
                            self.placed_ships.add(self.selected_ship)
                            self.selected_ship = None

        # rysowanie planszy gracza i przycisków
        self.player_board.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        self.orientation_button.draw(self.screen)

        # zmiana stanu gry na 'GAME'
        # sprawdza czy ilość rozmieszczonych statków jest równa ilości statków w słowniku
        if len(self.placed_ships) == len(self.ships):
            self.game_state = "GAME"

    def game_phase(self, mouse_pos, mouse_button_down):
        # ruch gracza
        if self.player_turn and mouse_button_down and self.mouse_button_released:
            # sprawdzenie kliknięcia na planszę komputera
            field = self.computer_board.check_click(mouse_pos, mouse_button_down)
            if field and not field.hit and not field.miss:
                field.hit = field.occupied
                field.miss = not field.occupied
                self.player_turn = False
                if self.check_victory(self.computer_ships, self.computer_board):
                    self.game_state = "END"
                    self.end_message = "Wygrana!"
                    pygame.display.set_mode(self.end_size)
                    return

        # ruch komputera
        elif not self.player_turn:
            row, col = self.hunt_target()
            if self.process_attack(self.player_board, self.player_ships, row, col):
                return
            self.player_turn = True

        # rysowanie plansz
        self.player_board.draw(self.screen)
        self.computer_board.draw(self.screen, True)

    def process_attack(self, board, ships, row, col):
        field = board.board[row][col]
        if not field.hit and not field.miss:
            field.hit = field.occupied
            field.miss = not field.occupied
            if field.hit:
                self.add_targets(row, col)
            if self.check_victory(ships, board):
                self.game_state = "END"
                if self.player_turn:
                    self.end_message = "Wygrana!"
                else:
                    self.end_message = "Przegrana!"
                pygame.display.set_mode(self.end_size)
                return True
        return False

    # wybiera losowe współrzędne do trafienia lub wykorzystuje potencjalne cele
    def hunt_target(self):
        if not self.targets:
            while True:
                row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
                field = self.player_board.board[row][col]
                if not field.hit and not field.miss:
                    break
        else:
            row, col = self.targets.pop()
        return row, col

    # dodaje do listy celów sąsiednie pola
    def add_targets(self, row, col):
        targets = [(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)]
        for target_row, target_col in targets:
            # sprawdza czy nie wychodzi poza planszę
            if 0 <= target_row < self.rows and 0 <= target_col < self.cols:
                field = self.player_board.board[target_row][target_col]
                if not field.hit and not field.miss and (target_row, target_col) not in self.targets:
                    self.targets.append((target_row, target_col))

    # tylko wyszarza
    def disable_button(self, ship):
        for button in self.buttons:
            if button.text == ship:
                button.normal_color = (128, 128, 128)
                button.hover_color = (128, 128, 128)
                button.current_color = (128, 128, 128)
                break

    def check_victory(self, ships, board):
        return all(board.board[row][col].hit for row, col in ships)

    # odpowiedzialne za ekrany menu i końca gry
    def display_menu(self, buttons, text, mouse_pos, mouse_button_down):
        self.screen.fill((255, 255, 255))

        font = pygame.font.SysFont('Arial', 75)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 110))
        self.screen.blit(text_surface, text_rect)

        for button in buttons:
            button.check_hover(mouse_pos)
            if button.check_click(mouse_pos, mouse_button_down):
                if button.text == 'Start':
                    self.game_state = "PLACEMENT"
                    pygame.display.set_mode(self.game_size)
                elif button.text == 'Exit':
                    pygame.quit()
                    sys.exit()
                elif button.text == 'Restart':
                    self.__init__(self.screen) # reinicializacja obiektu do stanu początkowego
                    self.game_state = "PLACEMENT"
                    pygame.display.set_mode(self.game_size)
            button.draw(self.screen)

    # PĘTLA GRY
    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            mouse_button_down = pygame.mouse.get_pressed()[0]

            # używane tylko w przypadku wychodzenia z okna za pomocą 'x'
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((200, 200, 200))

            # zmiany stanu gry
            if self.game_state == "MENU":
                self.display_menu(self.menu_screen_buttons, "BATTLESHIPS", mouse_pos, mouse_button_down)
            elif self.game_state == "PLACEMENT":
                self.place_player_ships(mouse_pos, mouse_button_down)
            elif self.game_state == "GAME":
                self.game_phase(mouse_pos, mouse_button_down)
            elif self.game_state == "END":
                self.display_menu(self.end_screen_buttons, self.end_message, mouse_pos, mouse_button_down)

            # rozwiązanie problemu z przytrzymanym przyciskiem myszy
            if not mouse_button_down:
                self.mouse_button_released = True
            else:
                self.mouse_button_released = False

            self.clock.tick(self.FPS)
            pygame.display.update()
