import pygame
import random
import time
from chunk import get_chunk

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

item_names = {"tree":"Fa", 
             "rock":"Kő", 
             "mushroom":"Gomba", 
             "crystal":"Kristály",
             "zöldseg":"Zöldség",
             "gyümölcs":"Gyümölcs",
             "hus":"Hús",
             "bör":"Bőr",
             "bel":"Bél",
             "toll":"Toll",
             "vaserc":"Vasérc",
             "varazskristaly":"Varázskristály"          
             }



# ----- INVENTORY -----
inventory = {key : 0 for key in item_names}

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
        "storage": {key : 0 for key in item_names}
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
    "crystal":(0,255,255),
    'bokor':(66, 171, 14),
    'gyumolcs':(150, 44, 44),
    'allat':(77, 51, 11),
    'madar':(140, 93, 65),
    'vaserc':(173, 169, 168),
    'varazskristaly':(165, 58, 176)
}

PATH_STR = 'Jatekok/OpenWorld/'
OBJECT_IMAGES = {
    "tree":pygame.image.load(PATH_STR + "tree.png").convert_alpha(),
    "rock":pygame.image.load(PATH_STR + "rock.png").convert_alpha(),
    "mushroom":pygame.image.load(PATH_STR + "mushroom.png").convert_alpha(),
    "crystal":pygame.image.load(PATH_STR + "crystal.png").convert_alpha(),
    'bokor':pygame.image.load(PATH_STR + 'bokor.png').convert_alpha(),
    'varazskristaly':pygame.image.load(PATH_STR + 'varazskristaly.png').convert_alpha(),
    'allat':pygame.image.load(PATH_STR + 'allat.png').convert_alpha(),
    'madar':pygame.image.load(PATH_STR + 'madar.png').convert_alpha(),
    'vaserc':pygame.image.load(PATH_STR + 'vaserc.png').convert_alpha()
}


RECIPES = {
    "balta": {
        "name": "Balta",
        "cost": {"tree": 1, "rock": 1},   # 1 fa + 1 kő
        "key": pygame.K_b
    },
    "csakany": {
        "name": "Csákány",
        "cost": {"tree": 1, "rock": 2},   # példa: 1 fa + 2 kő
        "key": pygame.K_c
    },
    "vas": {
        "name": "Vas",
        # példa recept: kristályból olvasztasz "vas"-at (csak demó)
        "cost": {"crystal": 2},
        "key": pygame.K_v
    },
}

craft_message = ""
craft_message_time = 0
CRAFT_MSG_DURATION = 2.0  # másodperc

def try_craft(item_key):
    """Megpróbálja legyártani az adott itemet a RECIPES alapján."""
    global craft_message, craft_message_time
    if item_key not in RECIPES:
        craft_message = "Ismeretlen recept."
        craft_message_time = time.time()
        return

    recipe = RECIPES[item_key]
    cost = recipe["cost"]

    # elegendő alapanyag?
    for res, need in cost.items():
        if inventory.get(res, 0) < need:
            craft_message = f"Nincs elég {res} a(z) {recipe['name']} készítéséhez."
            craft_message_time = time.time()
            return

    # vonjuk le a költséget
    for res, need in cost.items():
        inventory[res] -= need

    # adjuk hozzá a terméket
    inventory[item_key] = inventory.get(item_key, 0) + 1

    craft_message = f"Készült: {recipe['name']} (+1)!"
    craft_message_time = time.time()


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
            elif event.key == pygame.K_b:
                if inventory["tree"] >= 5:
                    inventory["tree"] -= 5
                    build_bunker_at(player_x, player_y)
                # (külön UI üzenetet is írhatsz ki, ha kevés a fa)

            # Bunker interakció (ha rajta állsz)
            # Z = deposit all; X = withdraw all
            elif event.key in (pygame.K_z, pygame.K_x):
                b, _ = player_near_bunker_rect()
                if b is not None:
                    if event.key == pygame.K_z:
                        # deposit all
                        for k in ("tree","rock","mushroom","crystal","balta","csakany","vas","varazskristaly"):
                            amt = inventory.get(k,0)
                            if amt > 0:
                                b["storage"][k] += amt
                                inventory[k] = 0
                    elif event.key == pygame.K_x:
                        # withdraw all
                        for k in ("tree","rock","mushroom","crystal","balta","csakany","vas","varazskristaly"):
                            amt = b["storage"].get(k,0)
                            if amt > 0:
                                inventory[k] += amt
                                b["storage"][k] = 0
            else:
                # Végigmegyünk a recepteken, és ha az adott key-hez tartozik craft, csináljuk
                for key_item, data in RECIPES.items():
                    if event.key == data["key"]:
                        try_craft(key_item)                

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
                            inventory['gyumolcs'] = inventory['gyumolcs'] + random.randint(1,2)
                            inventory['tree'] = inventory['tree'] + 1
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
    
    line_height = 18
    starty = HEIGHT-30
    for i, (key, value) in enumerate(inventory.items()):
        label = item_names.get(key, key.capitalize())
        line = f"{label}:{value}"
        text_surface = font.render(line,True,TEXT1)
        screen.blit(text_surface,(10, starty - i*line_height ))


    

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

    help_text = "Craft: [B]=Balta (1 fa + 1 ko), [C]=Csakany (1 fa + 2 ko), [V]=Vas (2 kristaly)"
    screen.blit(font.render(help_text, True, (0, 0, 0)), (10, 30))

  # Craft üzenet (siker/hiba)
    if craft_message and (now - craft_message_time) <= CRAFT_MSG_DURATION:
        screen.blit(font.render(craft_message, True, (20, 20, 20)), (10, 35))

    if map_visible:
        screen.blit(minimap_surface, (WIDTH-MINIMAP_SIZE-10 , 10 ))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()