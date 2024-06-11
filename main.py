import pygame, sys, tile

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tile Hover Example")

# Tworzenie obiektu Tile
tile = tile.Tile(normal_color=(0, 128, 255), hover_color=(255, 0, 0), w=100, h=100, cx=400, cy=300)

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pobranie pozycji myszy
    mouse_pos = pygame.mouse.get_pos()

    # Sprawdzenie najechania myszką
    tile.check_hover(mouse_pos)

    # Rysowanie kafelka
    screen.fill((255, 255, 255))
    tile.draw(screen)
    pygame.display.flip()

# Zakończenie Pygame
pygame.quit()
sys.exit()