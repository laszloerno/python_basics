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

# játékos képének betöltése 
player = pygame.image.load("./player.png").convert_alpha()
player = pygame.transform.scale(player, (50, 40))


# Main loop
running = True
while running:
    screen.fill(WHITE)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # kiszámoljuk a szöget az egérmutató és a játékos között
    angle = math.atan2(mouse_y - PLAYER_POS[1], mouse_x - PLAYER_POS[0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 

 

    # megrajzoljuk a játékost és a forgását
    rotated_image = pygame.transform.rotate(player, -math.degrees(angle))
    new_rect = rotated_image.get_rect(center=PLAYER_POS)
    screen.blit(rotated_image, new_rect.topleft)

 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()