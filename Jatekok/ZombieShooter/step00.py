import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYER_POS = (WIDTH // 2, HEIGHT // 2)
BULLET_SPEED = 10

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")
clock = pygame.time.Clock()


# Fő programciklus
running = True
while running:
    screen.fill(WHITE)
    mouse_x, mouse_y = pygame.mouse.get_pos()
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
         

 
    pygame.display.flip()
    clock.tick(60)

pygame.quit()