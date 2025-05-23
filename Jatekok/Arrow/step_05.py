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

 

def random_target():
    x = random.randint(WIDTH // 2 + 100, WIDTH - 60)
    y = HEIGHT - 100 - random.randint(0, 100)
    return pygame.Rect(x, y, 40, 50)

target_pos = random_target()

# Lövés változók
angle = 45
power = 20
arrow = None

# Nyíl létrehozása
class Arrow:
    def __init__(self, x, y, angle, power):
        self.x = x
        self.y = y
        rad = math.radians(angle)
        self.vx = math.cos(rad) * power
        self.vy = -math.sin(rad) * power

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), 5)

 
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
                arrow = Arrow(player_pos[0], player_pos[1], angle, power)


    # Irányítás
    if keys[pygame.K_UP]:
        angle = min(90, angle + 1)
    if keys[pygame.K_DOWN]:
        angle = max(0, angle - 1)
    if keys[pygame.K_LEFT]:
        power = max(5, power - 1)
    if keys[pygame.K_RIGHT]:
        power = min(50, power + 1)

     # Célzás megjelenítése
    rad = math.radians(angle)
    dx = math.cos(rad) * power * 2
    dy = -math.sin(rad) * power * 2
    aim_end = (int(player_pos[0] + dx), int(player_pos[1] + dy))
    pygame.draw.line(screen, (0, 150, 0), player_pos, aim_end, 2)

    # Nyíl frissítése
    if arrow:
        arrow.update()
        arrow.draw(screen)
        if target_pos.collidepoint(arrow.x, arrow.y):
            print("Találat!")
            arrow = None
            target_pos = random_target()
 
        elif arrow.x > WIDTH or arrow.y > HEIGHT:
            arrow = None

    # Íjász és célpont kirajzolása
    pygame.draw.rect(screen, BLUE, (player_pos[0]-10, player_pos[1], 10, 60))
    pygame.draw.rect(screen, RED, target_pos)

     # Szög és erő kiírása
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Szög: {angle}°, Erő: {power}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()