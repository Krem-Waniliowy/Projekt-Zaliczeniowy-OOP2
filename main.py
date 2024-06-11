import pygame, sys
from tile import Tile
from button import Button
from field import Field

# inicjalizacja Pygame
pygame.init()

# ustawienia gry
ROWS, COLS = 10, 10
FIELD_SIZE = 40
FIELD_BORDER_SIZE = 2

P_START_X = 50 # początek x planszy gracza
P_START_Y = 50 # początek y planczy gracza

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Test")

# # tworzenie obiektu Tile
# tile = Tile(normal_color=(0, 128, 255), hover_color=(255, 0, 0), w=100, h=100, cx=200, cy=400)
#
# # tworzenie obiektu Button
# button = Button(normal_color=(0, 128, 255), hover_color=(255, 0, 0), w=100, h=100, cx=400, cy=400, text='Click Me', text_color=(255, 255, 255), font_size=30, font_type='Arial')

# tworzenie planszy z pól
fields = []
for row in range(ROWS):
    fields_row = []
    for col in range(COLS):
        cx = P_START_X + col * (FIELD_SIZE) + FIELD_SIZE // 2
        cy = P_START_Y + row * (FIELD_SIZE) + FIELD_SIZE // 2
        field = Field((1, 1, 1), FIELD_BORDER_SIZE, normal_color=(0, 128, 255), hover_color=(0, 200, 255), w=FIELD_SIZE, h=FIELD_SIZE, cx=cx, cy=cy)
        fields_row.append(field)
    fields.append(fields_row)

# główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pobranie pozycji myszy
    mouse_pos = pygame.mouse.get_pos()
    mouse_button_down = pygame.mouse.get_pressed()[0]
    print(mouse_pos)

    screen.fill((255, 255, 255))
    
    # sprawdzenie najechania myszką
    # tile.check_hover(mouse_pos) # kafelek
    # button.check_hover(mouse_pos) # przycisk

    # rysowanie kafelka
    # tile.draw(screen)
    # button.draw(screen)
    for row in fields:
        for field in row:
            field.check_hover(mouse_pos)
            field.check_click(mouse_pos, mouse_button_down)
            field.draw(screen)

    pygame.display.flip()

# Zakończenie Pygame
pygame.quit()
sys.exit()
