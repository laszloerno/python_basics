import pygame
import random
import time
from chunk import generate_chunk, get_chunk

WIDTH = 1000
HEIGHT = 700

TILE_SIZE = 20
CHUNK_SIZE = 16
VISIBLE_CHUNKS_X = WIDTH // (TILE_SIZE * CHUNK_SIZE ) + 2
VISIBLE_CHUNKS_Y = HEIGHT // (TILE_SIZE * CHUNK_SIZE) + 2

BACKGROUND = (200,220,255)
PLAYER_COLOR = (0,0,255)
TREE_COLOR = (0,200,0)
MAP_BG = (30,30,30)
TEXT1 = (0,0,0)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None,18)

player_x, player_y = 0,0
speed = 5

# ----- INVENTORY -----
inventory = {"tree":0, "rock":0, "mushroom":0, "crystal":0}

# ----- RESPAWN -----
respawn_list = []

# ----- BUNKER -----
BUNKER_COLOR = (150, 120, 80)  # egyszerű barna
BUNKER_SIZE_TILES = 2          # 2x2 csempe
bunkers = []                   # elemek: {"x": int(px), "y": int(py), "storage": {...}}

def build_bunker_at(px, py):
    """Lerak egy 2x2-es bunkert px,py világkoordinátára igazítva (csempe-rácsra)."""
    bx = (px // TILE_SIZE) * TILE_SIZE
    by = (py // TILE_SIZE) * TILE_SIZE
    bunkers.append({
        "x": bx,
        "y": by,
        "storage": {"tree":0, "rock":0, "mushroom":0, "crystal":0}
    })

def player_near_bunker_rect():
    """Visszaadja a bunker dict-et és pygame.Rect-et, ha a játékos hozzáér valamelyik bunkerhez, különben (None, None)."""
    player_rect = pygame.Rect(player_x, player_y, TILE_SIZE, TILE_SIZE)
    for b in bunkers:
        rect = pygame.Rect(b["x"], b["y"], BUNKER_SIZE_TILES*TILE_SIZE, BUNKER_SIZE_TILES*TILE_SIZE)
        if player_rect.colliderect(rect):
            return b, rect
    return None, None

OBJECT_TYPES = {
    "tree":(34,139,34),
    "rock":(128,128,128),
    "mushroom":(255,0,255),
    "crystal":(0,255,255)
}

OBJECT_IMAGES = {
    "tree":pygame.image.load("Jatekok/OpenWorld/tree.png").convert_alpha(),
    "rock":pygame.image.load("Jatekok/OpenWorld/rock.png").convert_alpha(),
    "mushroom":pygame.image.load("Jatekok/OpenWorld/mushroom.png").convert_alpha(),
    "crystal":pygame.image.load("Jatekok/OpenWorld/crystal.png").convert_alpha()
}





MINIMAP_SIZE = 150
MINIMAP_SCALE = 0.1
minimap_surface = pygame.Surface((MINIMAP_SIZE,MINIMAP_SIZE))

map_visible = False
running = True
while running:
    screen.fill(BACKGROUND)

    # ---- RESPawn biztonságos bejárás ----
    now = time.time()
    for resp in respawn_list[:]:
        if now - resp["time"] >= 5:
            cx,cy = resp["chunk"]
            tiles = get_chunk(cx,cy)
            tiles.append({"type":resp["type"], "x":resp["x"], "y":resp["y"]})
            respawn_list.remove(resp)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ----- KEYDOWN események: bunker építés / letét / felvét -----
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                # pici debounce nélkül – ha kell, tedd vissza a sleep-et
                map_visible = not map_visible

            # Bunker építés: 5 fa
            if event.key == pygame.K_b:
                if inventory["tree"] >= 5:
                    inventory["tree"] -= 5
                    build_bunker_at(player_x, player_y)
                # (külön UI üzenetet is írhatsz ki, ha kevés a fa)

            # Bunker interakció (ha rajta állsz)
            # Z = deposit all; X = withdraw all
            if event.key in (pygame.K_z, pygame.K_x):
                b, _ = player_near_bunker_rect()
                if b is not None:
                    if event.key == pygame.K_z:
                        # deposit all
                        for k in ("tree","rock","mushroom","crystal"):
                            amt = inventory.get(k,0)
                            if amt > 0:
                                b["storage"][k] += amt
                                inventory[k] = 0
                    elif event.key == pygame.K_x:
                        # withdraw all
                        for k in ("tree","rock","mushroom","crystal"):
                            amt = b["storage"].get(k,0)
                            if amt > 0:
                                inventory[k] += amt
                                b["storage"][k] = 0

    # Mozgás
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_x -= speed
    if keys[pygame.K_RIGHT]: player_x += speed
    if keys[pygame.K_UP]: player_y -= speed
    if keys[pygame.K_DOWN]: player_y += speed

    cam_x = player_x - WIDTH//2
    cam_y = player_y - HEIGHT //2

    player_obj = pygame.Rect(player_x, player_y, TILE_SIZE, TILE_SIZE)

    # TILE-ek + pickup
    for dx in range(-1, VISIBLE_CHUNKS_X):
        for dy in range(-1,VISIBLE_CHUNKS_Y):
            chunk_x = ( cam_x // ( CHUNK_SIZE*TILE_SIZE) ) + dx
            chunk_y = ( cam_y // ( CHUNK_SIZE*TILE_SIZE) ) + dy
            tiles = get_chunk(chunk_x, chunk_y)

            to_remove = []
            for obj in tiles:
                world_x = chunk_x * CHUNK_SIZE * TILE_SIZE + obj["x"] *TILE_SIZE
                world_y = chunk_y * CHUNK_SIZE * TILE_SIZE + obj["y"] *TILE_SIZE
                screen_x = world_x - cam_x
                screen_y = world_y - cam_y

                image = OBJECT_IMAGES.get(obj["type"])
                if image:
                    image = pygame.transform.scale(image, (TILE_SIZE,TILE_SIZE))
                    screen.blit(image,(screen_x,screen_y))
                else:
                    color = OBJECT_TYPES.get(obj["type"],(255,255,255))
                    pygame.draw.rect(screen, color, (screen_x,screen_y,TILE_SIZE, TILE_SIZE) )

                tile_obj = pygame.Rect(world_x,world_y, TILE_SIZE, TILE_SIZE)
                if player_obj.colliderect(tile_obj):
                    collectKey = pygame.key.get_pressed()
                    if collectKey[pygame.K_SPACE]:
                        inventory[obj["type"]] = inventory[obj["type"]] + 1
                        to_remove.append(obj)
                        respawn_list.append({
                            "chunk":(chunk_x, chunk_y),
                            "type": obj["type"],
                            "x":obj["x"],
                            "y":obj["y"],
                            "time":time.time()
                        })

            if to_remove:
                for rem in to_remove:
                    try:
                        tiles.remove(rem)
                    except ValueError:
                        pass

    # ----- Bunkerek kirajzolása -----
    for b in bunkers:
        # kamerához igazított pozíció:
        sx = b["x"] - cam_x
        sy = b["y"] - cam_y
        pygame.draw.rect(
            screen,
            BUNKER_COLOR,
            (sx, sy, BUNKER_SIZE_TILES*TILE_SIZE, BUNKER_SIZE_TILES*TILE_SIZE)
        )
        # dísz keret
        pygame.draw.rect(
            screen,
            (90,70,50),
            (sx, sy, BUNKER_SIZE_TILES*TILE_SIZE, BUNKER_SIZE_TILES*TILE_SIZE),
            2
        )

    # Minimap
    if map_visible:
        minimap_surface.fill(MAP_BG)
        for dx in range(-3,4):
            for dy in range(-3,4):
                chunk_x = ( cam_x // ( CHUNK_SIZE*TILE_SIZE) ) + dx
                chunk_y = ( cam_y // ( CHUNK_SIZE*TILE_SIZE) ) + dy
                tiles = get_chunk(chunk_x, chunk_y)

                for obj in tiles:
                    world_x = chunk_x * CHUNK_SIZE  + obj["x"]
                    world_y = chunk_y * CHUNK_SIZE  + obj["y"]

                    rel_x = world_x - (player_x //TILE_SIZE)
                    rel_y = world_y - (player_y //TILE_SIZE)

                    px = MINIMAP_SIZE // 2 + int(rel_x * MINIMAP_SCALE *TILE_SIZE)
                    py = MINIMAP_SIZE // 2 + int(rel_y * MINIMAP_SCALE *TILE_SIZE)
                    color = OBJECT_TYPES.get(obj["type"],(255,255,255))
                    pygame.draw.rect(minimap_surface, color, (px,py,2, 2) )

        # bunker pötty a minimapon (opcionális)
        for b in bunkers:
            rel_x = (b["x"]//TILE_SIZE) - (player_x//TILE_SIZE)
            rel_y = (b["y"]//TILE_SIZE) - (player_y//TILE_SIZE)
            px = MINIMAP_SIZE // 2 + int(rel_x * MINIMAP_SCALE *TILE_SIZE)
            py = MINIMAP_SIZE // 2 + int(rel_y * MINIMAP_SCALE *TILE_SIZE)
            pygame.draw.rect(minimap_surface, (200,160,100), (px,py,3,3))

        pygame.draw.circle(minimap_surface, PLAYER_COLOR, (MINIMAP_SIZE //2,MINIMAP_SIZE//2), 3)

    # Játékos
    pygame.draw.rect(screen, PLAYER_COLOR,(WIDTH//2, HEIGHT//2, TILE_SIZE,TILE_SIZE) )

    # HUD: inventory
    inv_text = f"Wood: {inventory['tree']}  Rock: {inventory['rock']}  Food: {inventory['mushroom']}  Crystal: {inventory['crystal']}"
    text_surface = font.render(inv_text,True,TEXT1)
    screen.blit(text_surface,(10, HEIGHT-30 ))

    # HUD: bunker help / storage, ha közelben vagy
    near_bunker, near_rect = player_near_bunker_rect()
    if near_bunker:
        help1 = "[Z] Letét (összes), [X] Felvét (összes)"
        screen.blit(font.render(help1, True, (0,0,0)), (10, 10))
        stor = near_bunker["storage"]
        stext = f"Bunker: Wood {stor['tree']}  Rock {stor['rock']}  Food {stor['mushroom']}  Crystal {stor['crystal']}"
        screen.blit(font.render(stext, True, (0,0,0)), (10, 28))
    else:
        # építés súgó
        build_help = "Bunker epites: [B] (kell 5 fa)"
        screen.blit(font.render(build_help, True, (0,0,0)), (10, 10))

    if map_visible:
        screen.blit(minimap_surface, (WIDTH-MINIMAP_SIZE-10 , 10 ))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
