import pygame
import random
import time
from chunk import get_chunk, update_chunk_mobs
from parameters import  OBJECT_TYPES, RECIPES, item_names, CRAFT_TEXT_COLOR, CRAFT_NOT_POSSIBLE_COLOR, get_item_capacity
import craft
import bunkers

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

PATH_STR = './Jatekok/OpenWorld/'
OBJECT_IMAGES = {
    "wood":pygame.image.load(PATH_STR + "tree.png").convert_alpha(),
    "rock":pygame.image.load(PATH_STR + "rock.png").convert_alpha(),
    "mushroom":pygame.image.load(PATH_STR + "mushroom.png").convert_alpha(),
    "crystal":pygame.image.load(PATH_STR + "crystal.png").convert_alpha(),
    'bokor':pygame.image.load(PATH_STR + 'bokor.png').convert_alpha(),
    'varazskristaly':pygame.image.load(PATH_STR + 'varazskristaly.png').convert_alpha(),
    'allat':pygame.image.load(PATH_STR + 'allat.png').convert_alpha(),
    'madar':pygame.image.load(PATH_STR + 'madar.png').convert_alpha(),
    'vaserc':pygame.image.load(PATH_STR + 'vaserc.png').convert_alpha()
}
# ----- INVENTORY -----
inventory = {key : 100 for key in item_names}

# ----- RESPAWN -----
respawn_list = []


MINIMAP_SIZE = 150
MINIMAP_SCALE = 0.1
minimap_surface = pygame.Surface((MINIMAP_SIZE,MINIMAP_SIZE))

map_visible = False


inventory_visible = False
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
                map_visible = not map_visible
            elif event.key == pygame.K_i:
                inventory_visible = not inventory_visible                     
            # Bunker építés: 5 fa
            elif event.key == pygame.K_b:
                if inventory["wood"] >= 5:
                    inventory["wood"] -= 5
                    bunkers.build_bunker_at(player_x, player_y,TILE_SIZE)

            elif event.key in (pygame.K_1, pygame.K_2):
                b, _ = bunkers.player_near_bunker_rect(player_x, player_y, TILE_SIZE)
                if b is not None:
                    if event.key == pygame.K_1:
                        bunkers.open_bunker_menu("deposit", b, inventory, item_names)
                    elif event.key == pygame.K_2:
                        bunkers.open_bunker_menu("withdraw", b, inventory, item_names)
  

            if bunkers.handle_keydown(event, inventory):
                continue
            if craft.handle_keydown(event,inventory):
                continue

    # Mozgás
    keys = pygame.key.get_pressed()
    if not craft.is_open() and not bunkers.is_menu_open():
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
            update_chunk_mobs(chunk_x, chunk_y, now)            
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
                if not craft.is_open() and not bunkers.is_menu_open() and player_obj.colliderect(tile_obj):
                    collectKey = pygame.key.get_pressed()
                    if collectKey[pygame.K_SPACE]:
                        'bokor','allat' 

                        if obj["type"] ==  'madar':
                            inventory['hus'] = inventory['hus'] + 1
                            inventory['toll'] = inventory['toll'] + 1
                        elif obj["type"] == 'vaserc':
                            inventory['vas'] = inventory['vas'] + 1
                            inventory['rock'] = inventory['rock'] + 1
                        elif obj["type"] == 'allat':
                            inventory['hus'] = inventory['hus'] + random.randint(1,2)
                            inventory['bör'] = inventory['bör'] + 1
                            inventory['bel'] = inventory['bel'] + 1
                        elif obj["type"] == 'bokor':
                            inventory['gyümölcs'] = inventory['gyümölcs'] + random.randint(1,2)
                            inventory["wood"] = inventory["wood"] + 1
                        else:
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
    for b in bunkers.get_bunkers():
        # kamerához igazított pozíció:
        sx = b["x"] - cam_x
        sy = b["y"] - cam_y
        pygame.draw.rect(
            screen,
            bunkers.BUNKER_COLOR,
            (sx, sy, bunkers.BUNKER_SIZE_TILES*TILE_SIZE, bunkers.BUNKER_SIZE_TILES*TILE_SIZE)
        )
        # dísz keret
        pygame.draw.rect(
            screen,
            (90,70,50),
            (sx, sy, bunkers.BUNKER_SIZE_TILES*TILE_SIZE, bunkers.BUNKER_SIZE_TILES*TILE_SIZE),
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
        for b in bunkers.get_bunkers():
            rel_x = (b["x"]//TILE_SIZE) - (player_x//TILE_SIZE)
            rel_y = (b["y"]//TILE_SIZE) - (player_y//TILE_SIZE)
            px = MINIMAP_SIZE // 2 + int(rel_x * MINIMAP_SCALE *TILE_SIZE)
            py = MINIMAP_SIZE // 2 + int(rel_y * MINIMAP_SCALE *TILE_SIZE)
            pygame.draw.rect(minimap_surface, (200,160,100), (px,py,3,3))

        pygame.draw.circle(minimap_surface, PLAYER_COLOR, (MINIMAP_SIZE //2,MINIMAP_SIZE//2), 3)

    # Játékos
    pygame.draw.rect(screen, PLAYER_COLOR,(WIDTH//2, HEIGHT//2, TILE_SIZE,TILE_SIZE) )

    # HUD: inventory
    
    if inventory_visible:
        line_height = 18
        starty = HEIGHT-30
        for i, (key, value) in enumerate(inventory.items()):
            label = item_names.get(key, key.capitalize())
            line = f"{label}:{value}"
            text_surface = font.render(line,True,TEXT1)
            screen.blit(text_surface,(10, starty - i*line_height ))


    

    # HUD: bunker help / storage, ha közelben vagy
    near_bunker, near_rect = bunkers.player_near_bunker_rect(player_x, player_y, TILE_SIZE)
    if near_bunker:
        help1 = "[1] Letét (összes), [2] Felvét (összes)"
        screen.blit(font.render(help1, True, (0,0,0)), (10, 10))

        stor = near_bunker["storage"]
        bunkers.render_bunker_hud(screen, font, stor,item_names,get_item_capacity, x=10, y = 28, row_h=18)

         

    else:
        # építés súgó
        build_help = "Bunker epites: [B] (kell 5 fa)"
        screen.blit(font.render(build_help, True, (0,0,0)), (10, 10))

    craft.render(screen, font, inventory)
        


    if map_visible:
        screen.blit(minimap_surface, (WIDTH-MINIMAP_SIZE-10 , 10 ))

    bunkers.render_bunker_menu(screen,font,item_names, inventory, get_item_capacity)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()