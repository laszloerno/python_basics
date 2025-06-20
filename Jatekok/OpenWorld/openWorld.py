import pygame
import random

# Beállítások
TILE_SIZE = 20
CHUNK_SIZE = 16  # chunkonként 16x16 tile
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
VISIBLE_CHUNKS_X = SCREEN_WIDTH // (TILE_SIZE * CHUNK_SIZE) + 2
VISIBLE_CHUNKS_Y = SCREEN_HEIGHT // (TILE_SIZE * CHUNK_SIZE) + 2

# Színek
GREEN = (0, 200, 0)
BROWN = (120, 80, 40)
PLAYER_COLOR = (0, 0, 255)
BACKGROUND = (200, 220, 255)

# Inicializálás
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Játékos pozíció (világ koordináta)
player_x, player_y = 0, 0
speed = 5

# Chunk generáló
def generate_chunk(cx, cy):
    random.seed(f"{cx},{cy}")  # deterministic
    tiles = []
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            if random.random() < 0.005:  # 10% esély fa generálására
                tiles.append((x, y))
    return tiles

# Felfedezett chunkok cache-ben
chunk_cache = {}

def get_chunk(cx, cy):
    key = (cx, cy)
    if key not in chunk_cache:
        chunk_cache[key] = generate_chunk(cx, cy)
    return chunk_cache[key]

# Főciklus
running = True
while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Irányítás
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_x -= speed
    if keys[pygame.K_RIGHT]: player_x += speed
    if keys[pygame.K_UP]: player_y -= speed
    if keys[pygame.K_DOWN]: player_y += speed

    # Kamera pozíció (bal felső sarok világ koordináta)
    cam_x = player_x - SCREEN_WIDTH // 2
    cam_y = player_y - SCREEN_HEIGHT // 2

    # Chunkok kirajzolása
    for dx in range(-1, VISIBLE_CHUNKS_X):
        for dy in range(-1, VISIBLE_CHUNKS_Y):
            chunk_x = (cam_x // (CHUNK_SIZE * TILE_SIZE)) + dx
            chunk_y = (cam_y // (CHUNK_SIZE * TILE_SIZE)) + dy
            tiles = get_chunk(chunk_x, chunk_y)

            for tx, ty in tiles:
                world_x = chunk_x * CHUNK_SIZE * TILE_SIZE + tx * TILE_SIZE
                world_y = chunk_y * CHUNK_SIZE * TILE_SIZE + ty * TILE_SIZE
                screen_x = world_x - cam_x
                screen_y = world_y - cam_y
                pygame.draw.rect(screen, GREEN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

    # Játékos kirajzolása
    pygame.draw.rect(screen, PLAYER_COLOR, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
