import pygame
import random

# Beállítások
TILE_SIZE = 20
CHUNK_SIZE = 16
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
VISIBLE_CHUNKS_X = SCREEN_WIDTH // (TILE_SIZE * CHUNK_SIZE) + 2
VISIBLE_CHUNKS_Y = SCREEN_HEIGHT // (TILE_SIZE * CHUNK_SIZE) + 2

# Színek
GREEN = (0, 200, 0)
BROWN = (120, 80, 40)
PLAYER_COLOR = (0, 0, 255)
BACKGROUND = (200, 220, 255)
MAP_BG = (30, 30, 30)

# Inicializálás
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Open World Felülnézeti Játék")

# Játékos pozíció
player_x, player_y = 0, 0
speed = 5

# Chunk cache és felfedezett chunkok
discovered_chunks = set()
chunk_cache = {}

# Chunk generáló
def generate_chunk(cx, cy):
    random.seed(f"{cx},{cy}")
    tiles = []
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            if random.random() < 0.01:
                tiles.append((x, y))
    return tiles

def get_chunk(cx, cy):
    key = (cx, cy)
    if key not in chunk_cache:
        chunk_cache[key] = generate_chunk(cx, cy)
    discovered_chunks.add(key)
    return chunk_cache[key]

# Teljes térkép kirajzolás
def draw_world_map():
    map_surface = pygame.Surface((800, 800))
    map_surface.fill(MAP_BG)

    for (cx, cy), tiles in chunk_cache.items():
        for tx, ty in tiles:
            wx = cx * CHUNK_SIZE + tx
            wy = cy * CHUNK_SIZE + ty
            pygame.draw.rect(map_surface, GREEN, (wx * 2, wy * 2, 2, 2))

    # Játékos pozíció
    px = player_x // TILE_SIZE * 2
    py = player_y // TILE_SIZE * 2
    pygame.draw.circle(map_surface, PLAYER_COLOR, (px, py), 3)
    screen.blit(map_surface, (0, 0))
    pygame.display.flip()

# Minimap
MINIMAP_SIZE = 150
MINIMAP_SCALE = 0.2
minimap_surface = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))

# Főciklus
running = True
show_map = False
while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                show_map = not show_map

    if show_map:
        draw_world_map()
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_x -= speed
    if keys[pygame.K_RIGHT]: player_x += speed
    if keys[pygame.K_UP]: player_y -= speed
    if keys[pygame.K_DOWN]: player_y += speed

    cam_x = player_x - SCREEN_WIDTH // 2
    cam_y = player_y - SCREEN_HEIGHT // 2

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

    # Minimap frissítés
    minimap_surface.fill((50, 50, 50))
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            chunk_x = (player_x // (CHUNK_SIZE * TILE_SIZE)) + dx
            chunk_y = (player_y // (CHUNK_SIZE * TILE_SIZE)) + dy
            tiles = get_chunk(chunk_x, chunk_y)

            for tx, ty in tiles:
                wx = chunk_x * CHUNK_SIZE + tx
                wy = chunk_y * CHUNK_SIZE + ty

                rel_x = wx - (player_x // TILE_SIZE)
                rel_y = wy - (player_y // TILE_SIZE)

                px = MINIMAP_SIZE // 2 + int(rel_x * MINIMAP_SCALE * TILE_SIZE)
                py = MINIMAP_SIZE // 2 + int(rel_y * MINIMAP_SCALE * TILE_SIZE)
                pygame.draw.rect(minimap_surface, GREEN, (px, py, 2, 2))

    pygame.draw.circle(minimap_surface, PLAYER_COLOR, (MINIMAP_SIZE // 2, MINIMAP_SIZE // 2), 3)
    screen.blit(minimap_surface, (SCREEN_WIDTH - MINIMAP_SIZE - 10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
