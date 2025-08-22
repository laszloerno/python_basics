import pygame
import random
import time

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

inventory = {"tree":0, 
             "rock":0, 
             "mushroom":0, 
             "crystal":0,     
             #craftolt targyak
             "balta": 0,
             "csakany": 0,
             "vas": 0
}

respawn_list = []


# KULCSOK: kimeneti tárgy; cost: szükséges alapanyagok, key: melyik billentyű gyártja
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


def generate_chunk(cx, cy):
    random.seed(f"{cx},{cy}")
    tiles = []
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            if random.random() < 0.001:
                tiles.append({"type":"tree",
                                "x":x,
                                 "y":y})
            if random.random() < 0.0015:
                tiles.append({"type":"rock",
                                "x":x,
                                 "y":y})
            if random.random() < 0.0018:
                tiles.append({"type":"mushroom",
                                "x":x,
                                 "y":y})
            if random.random() < 0.002:
                tiles.append({"type":"crystal",
                                "x":x,
                                 "y":y})
    return tiles

chunk_cache = {}

def get_chunk(cx,cy):
    key = (cx,cy)
    if key not in chunk_cache:
        chunk_cache[key] = generate_chunk(cx,cy)
    return chunk_cache[key]



MINIMAP_SIZE = 150
MINIMAP_SCALE = 0.1

minimap_surface = pygame.Surface((MINIMAP_SIZE,MINIMAP_SIZE))


map_visible = False
running = True
while running:
    screen.fill(BACKGROUND)


    now = time.time()
    for resp in respawn_list:
        if now - resp["time"] >= 5:
            cx,cy = resp["chunk"]
            tiles = get_chunk(cx,cy)
            tiles.append({"type":resp["type"],
                            "x":resp["x"],
                            "y":resp["y"]})
            respawn_list.remove(resp)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ====== CRAFT BILLENTYŰK ======
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                time.sleep(0.7)
                map_visible = not map_visible
            else:
                # Végigmegyünk a recepteken, és ha az adott key-hez tartozik craft, csináljuk
                for key_item, data in RECIPES.items():
                    if event.key == data["key"]:
                        try_craft(key_item)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_x -= speed
    if keys[pygame.K_RIGHT]: player_x += speed
    if keys[pygame.K_UP]: player_y -= speed
    if keys[pygame.K_DOWN]: player_y += speed
 


    cam_x = player_x - WIDTH//2
    cam_y = player_y - HEIGHT //2

    player_obj = pygame.Rect(player_x, player_y, TILE_SIZE, TILE_SIZE)

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
        
        pygame.draw.circle(minimap_surface, PLAYER_COLOR, (MINIMAP_SIZE //2,MINIMAP_SIZE//2), 3)


    pygame.draw.rect(screen, PLAYER_COLOR,(WIDTH//2, HEIGHT//2, TILE_SIZE,TILE_SIZE) )

    inv_text = f"Wood: {inventory['tree']} Rock: {inventory['rock']}  Food: {inventory['mushroom']}  Crystal: {inventory['crystal']}"
    text_surface = font.render(inv_text,True,TEXT1)
    screen.blit(text_surface,(10, HEIGHT-30 ))

    item_text = f"Balta: {inventory['balta']} | Csakany: {inventory['csakany']} | Vas: {inventory['vas']}"
    screen.blit(font.render(item_text, True, (0, 0, 0)), (10, HEIGHT - 45))

    help_text = "Craft: [B]=Balta (1 fa + 1 ko), [C]=Csakany (1 fa + 2 ko), [V]=Vas (2 kristaly)"
    screen.blit(font.render(help_text, True, (0, 0, 0)), (10, 10))

  # Craft üzenet (siker/hiba)
    if craft_message and (now - craft_message_time) <= CRAFT_MSG_DURATION:
        screen.blit(font.render(craft_message, True, (20, 20, 20)), (10, 35))
    if map_visible:
        screen.blit(minimap_surface, (WIDTH-MINIMAP_SIZE-10 , 10 ))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()