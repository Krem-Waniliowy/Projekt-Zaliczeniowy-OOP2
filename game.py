import pygame
import random
import sys
from button import Button
from board import Board

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.rows, self.cols = 10, 10
        self.field_size = 40
        self.field_border_size = 2
        self.p_start_x, self.p_start_y = 50, 50
        self.c_start_x, self.c_start_y = 550, 50
        self.player_board = Board(self.p_start_x, self.p_start_y, self.rows, self.cols, self.field_size, self.field_border_size)
        self.computer_board = Board(self.c_start_x, self.c_start_y, self.rows, self.cols, self.field_size, self.field_border_size)
        self.ship_types = {
            "Carrier": 5,
            "Battleship": 4,
            "Cruiser": 3,
            "Submarine": 3,
            "Destroyer": 2
        }
        self.buttons = self.create_buttons()
        self.orientation_button = Button(normal_color=(0, 128, 255), hover_color=(255, 0, 0), w=150, h=50, cx=600, cy=400, text='Horizontal', text_color=(255, 255, 255), font_size=20, font_type='Arial')
        self.selected_ship = None
        self.selected_ship_size = 0
        self.selected_ship_direction = 'H'
        self.player_ships = []
        self.computer_ships = []
        self.place_computer_ships()
        self.game_state = "PLACEMENT"
        self.player_turn = True
        self.orientation_button_pressed = False
        self.mouse_button_released = True
        self.placed_ships = set()

    def create_buttons(self):
        buttons = []
        button_x = 600
        button_y = 50
        button_gap = 60
        for ship_type in self.ship_types.keys():
            button = Button(normal_color=(0, 128, 255), hover_color=(255, 0, 0), w=150, h=50, cx=button_x, cy=button_y, text=ship_type, text_color=(255, 255, 255), font_size=20, font_type='Arial')
            buttons.append(button)
            button_y += button_gap
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
                if self.computer_board.can_place_ship(row, col, size, direction):
                    self.computer_board.place_ship(row, col, size, direction, self.computer_ships)
                    break

    def handle_placement_phase(self, mouse_pos, mouse_button_down):
        for button in self.buttons:
            button.check_hover(mouse_pos)
            if button.check_click(mouse_pos, mouse_button_down):
                self.selected_ship = button.text
                self.selected_ship_size = self.ship_types[self.selected_ship]

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

        for row in range(self.rows):
            for col in range(self.cols):
                field = self.player_board.fields[row][col]
                field.check_hover(mouse_pos)
                if self.selected_ship and field.check_click(mouse_pos, mouse_button_down) and self.selected_ship not in self.placed_ships:
                    if self.player_board.can_place_ship(row, col, self.selected_ship_size, self.selected_ship_direction):
                        self.player_board.place_ship(row, col, self.selected_ship_size, self.selected_ship_direction, self.player_ships)
                        self.disable_button(self.selected_ship)
                        self.placed_ships.add(self.selected_ship)
                        self.selected_ship = None

        self.player_board.draw(self.screen)

        for button in self.buttons:
            button.draw(self.screen)

        self.orientation_button.draw(self.screen)

        if len(self.placed_ships) == len(self.ship_types):
            self.game_state = "GAME"

    def handle_game_phase(self, mouse_pos, mouse_button_down):
        if self.player_turn and mouse_button_down and self.mouse_button_released:
            field = self.computer_board.check_click(mouse_pos, mouse_button_down)
            if field and not field.hit and not field.miss:
                field.hit = field.occupied
                field.miss = not field.occupied
                self.player_turn = False
                if self.check_victory(self.computer_ships, self.computer_board):
                    self.display_end_message("Wygrana!")
                    return

        elif not self.player_turn:
            # tura komputera (póki co głupia wersja)
            while not self.player_turn:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                field = self.player_board.fields[row][col]
                if not field.hit and not field.miss:
                    field.hit = field.occupied
                    field.miss = not field.occupied
                    self.player_turn = True  # koniec tury komputera
                    if self.check_victory(self.player_ships, self.player_board):
                        self.display_end_message("Przegrana!")
                        return
                    break

        self.player_board.draw(self.screen)
        self.computer_board.draw(self.screen, hide_ships=True)

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
                self.handle_placement_phase(mouse_pos, mouse_button_down)
            elif self.game_state == "GAME":
                self.handle_game_phase(mouse_pos, mouse_button_down)

            if not mouse_button_down:
                self.mouse_button_released = True
            else:
                self.mouse_button_released = False

            pygame.display.flip()

        pygame.quit()
        sys.exit()
