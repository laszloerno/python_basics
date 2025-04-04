import pygame
import math
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYER_POS = (WIDTH // 2, HEIGHT // 2)
BULLET_SPEED = 10
ENEMY_SPEED = 2 # ellenség sebessége
SPAWN_INTERVAL = 120 # ellenség megjelenési időköz (FPS-ben)


# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter")
clock = pygame.time.Clock()

# játékos képének betöltése 
player = pygame.image.load("./player.png").convert_alpha()
player = pygame.transform.scale(player, (50, 40))


# Lövedékek listája
bullets = []

#ellenség 
# Load and scale enemy image
enemy_easy = pygame.image.load("enemy_easy.png").convert_alpha()
enemy_easy = pygame.transform.scale(enemy_easy, (50, 40))

strong_enemy = pygame.image.load("enemy_strong_full.png").convert_alpha()
strong_enemy = pygame.transform.scale(strong_enemy, (50, 50))

strong_enemy3 = pygame.image.load("enemy_strong3.png").convert_alpha()
strong_enemy3 = pygame.transform.scale(strong_enemy3, (50, 50))

strong_enemy2 = pygame.image.load("enemy_strong2.png").convert_alpha()
strong_enemy2 = pygame.transform.scale(strong_enemy2, (50, 50))

strong_enemy1 = pygame.image.load("enemy_strong1.png").convert_alpha()
strong_enemy1 = pygame.transform.scale(strong_enemy1, (50, 50))

enemies = []
spawn_timer = 0

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
        # ha az egérgombot lenyomják, akkor lövedéket indítunk
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Bal egérgomb klikkelése
                dx = math.cos(angle) * BULLET_SPEED #  x irányú sebesség
                dy = math.sin(angle) * BULLET_SPEED #  y irányú sebesség
                bullets.append({
                    "x": PLAYER_POS[0], # kezdő x pozíció a játékos pozíciója
                    "y": PLAYER_POS[1], # kezdő y pozíció a játékos pozíciója
                    "dx": dx, # x irányú sebesség
                    "dy": dy # y irányú sebesség
                })


    # a lövedékek mozgása és újra rajzolása
    for bullet in bullets[:]:
        bullet["x"] += bullet["dx"]
        bullet["y"] += bullet["dy"]
        pygame.draw.line(screen, RED, (bullet["x"], bullet["y"]), (bullet["x"] - bullet["dx"] * 2, bullet["y"] - bullet["dy"] * 2), 3)
        #   ellenőrizzük, hogy a lövedékek a képernyőn kívülre kerültek-e
        if bullet["x"] < 0 or bullet["x"] > WIDTH or bullet["y"] < 0 or bullet["y"] > HEIGHT:
            # ha igen, eltávolítjuk őket a listából
            bullets.remove(bullet)

    # Spawn enemies
    spawn_timer += 1
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_timer = 0
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x, y = random.randint(0, WIDTH), 0
        elif side == "bottom":
            x, y = random.randint(0, WIDTH), HEIGHT
        elif side == "left":
            x, y = 0, random.randint(0, HEIGHT)
        else:
            x, y = WIDTH, random.randint(0, HEIGHT)
        
        
        if random.random() < 0.95:  # 15% eséllyel erős ellenség
            # egy új tulajdonság került fel ami a HP így tudjuk számolni, hogy mennyi ereje van még
            enemies.append({"x": x, "y": y, "type": "strong", "hp": 4})
        else:
            enemies.append({"x": x, "y": y, "type": "normal", "hp": 1})


   # ellenségek mozgása
    for enemy in enemies[:]:
        dx = PLAYER_POS[0] - enemy["x"]
        dy = PLAYER_POS[1] - enemy["y"]
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist * ENEMY_SPEED, dy / dist * ENEMY_SPEED
        enemy["x"] += dx
        enemy["y"] += dy

        # Draw enemy
        #attól függően, hogy milyen ellenség van, más képet rajzolunk ki
        if enemy["type"] == "strong":
            if enemy["hp"] == 4:
                img = strong_enemy
            elif enemy["hp"] == 3:
                img = strong_enemy3
            elif enemy["hp"] == 2:
                img = strong_enemy2
            elif enemy["hp"] == 1:
                img = strong_enemy1
        else:
            img = enemy_easy
        #a képet lecseréljük a forgatott képre
        # a forgatás szögét a dx és dy alapján számítjuk ki
        rotated_enemy = pygame.transform.rotate(img, -math.degrees(math.atan2(dy, dx)))
        rect = rotated_enemy.get_rect(center=(enemy["x"], enemy["y"]))
        screen.blit(rotated_enemy, rect.topleft)

        # Ha találat éri akkor levesszük a lövedéket és az ellenséget
        for bullet in bullets[:]:
            if math.hypot(enemy["x"] - bullet["x"], enemy["y"] - bullet["y"]) < 10: # 10 pixel távolságra van a lövedéktől a közepe (=szive)
                if bullet in bullets:
                    bullets.remove(bullet)
                # ha a lövedék eltalálja az ellenséget, akkor levonunk 1 HP-t
                enemy["hp"] -= 1
                if enemy["hp"] <= 0:
                    enemies.remove(enemy)
                break

    # megrajzoljuk a játékost és a forgását
    rotated_image = pygame.transform.rotate(player, -math.degrees(angle))
    new_rect = rotated_image.get_rect(center=PLAYER_POS)
    screen.blit(rotated_image, new_rect.topleft)

 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()