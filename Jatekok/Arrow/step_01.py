import pygame
import math
import random

# Inicializálás
pygame.init()

# Állandók
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAVITY = 0.5

# Ablak
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Középkori íjász párbaj")
clock = pygame.time.Clock()

# Íjász pozíciók
player_pos = (100, HEIGHT - 200)

 

target_pos = pygame.Rect(700, 400, 40, 50)

# Lövés változók
angle = 45
power = 20
arrow = None

 
# Főciklus
running = True
while running:
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and arrow is None:
                # ide jön majd az a rész hogy kilőjjük a nyilat
                print("Kilőve!")

    # Irányítás
    if keys[pygame.K_UP]:
        angle = min(90, angle + 1)
    if keys[pygame.K_DOWN]:
        angle = max(0, angle - 1)
    if keys[pygame.K_LEFT]:
        power = max(5, power - 1)
    if keys[pygame.K_RIGHT]:
        power = min(50, power + 1)

 
    # Íjász és célpont kirajzolása
    pygame.draw.rect(screen, BLUE, (player_pos[0]-10, player_pos[1], 10, 60))
    pygame.draw.rect(screen, RED, target_pos)

 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()