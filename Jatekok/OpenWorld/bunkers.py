import pygame
import random
import time
from chunk import get_chunk
from parameters import  OBJECT_TYPES, RECIPES, item_names, CRAFT_TEXT_COLOR, CRAFT_NOT_POSSIBLE_COLOR, get_item_capacity

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


def can_craft(inventory, cost:dict) -> bool:
    for resource, need in cost.items():
        if inventory.get(resource,0) < need:
            return False
    return True


def craft_menu_display(surface,inventory,receptek,item_names, selected_idx, scroll, rows=16):
    W,H = surface.get_size()
    overlay = pygame.Surface((W,H), pygame.SRCALPHA)
    overlay.fill((0,0,0,140))
    surface.blit(overlay, (0,0))

    panel_w, panel_h = 520, 360
    panel_x = (W-panel_w) //2
    panel_y = (H-panel_h) //2

    pygame.draw.rect(surface, (235,235,240), (panel_x,panel_y,panel_w, panel_h), border_radius=10)
    pygame.draw.rect(surface, (40, 40, 60), (panel_x, panel_y, panel_w, panel_h), width=2, border_radius=10)

    title = font.render("CRAFT Menü (UP/DOWN választ, Enter craft, Esc/C bezár)", True, CRAFT_TEXT_COLOR)
    surface.blit(title, (panel_x+10, panel_y+10))

    recept_lista = [(k,v) for k,v in receptek.items()]
    osszees_recept = len(recept_lista)

    fejlec = font.render("Tárgy                         Költség", True, CRAFT_TEXT_COLOR)
    surface.blit(fejlec, (panel_x+150, panel_y+25))


    start = scroll
    end = min(scroll+rows,osszees_recept)

    row_y = panel_y + 80
    row_h = 28

    for idx in range(start,end):
        key, data = recept_lista[idx]
        name = data.get("name",key.capitalize())
        cost = data.get("cost", {})

        if selected_idx ==idx:
            pygame.draw.rect(surface, (210, 225, 255), (panel_x + 10, row_y - 2, panel_w - 20, row_h), border_radius=6)
       
            
        txt_name = font.render(name,True,CRAFT_TEXT_COLOR )
        surface.blit(txt_name,(panel_x+100,row_y))

        parts = []
        for resource, need in cost.items():
            label = item_names.get(resource,resource)
            have = inventory.get(resource,0)
            parts.append(f"{label} {have}/{need}")
        cost_str = " | ".join(parts)

        gyarthato = can_craft(inventory, cost)
        
        if gyarthato:
            cost_txt = font.render(cost_str, True, CRAFT_TEXT_COLOR)
        else:
            cost_txt = font.render(cost_str, True, CRAFT_NOT_POSSIBLE_COLOR)
        
        surface.blit(cost_txt, (panel_x+300,row_y))

        row_y += row_h
      #  if osszees_recept > rows:





MINIMAP_SIZE = 150
MINIMAP_SCALE = 0.1
minimap_surface = pygame.Surface((MINIMAP_SIZE,MINIMAP_SIZE))

map_visible = False
craft_menu = False
craft_selected = 0
craft_scroll = 0
CRAFT_ROWS = 10

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
            if event.key == pygame.K_c:
                craft_menu = not craft_menu
                continue

            if craft_menu:
                
                recept_lista = list(RECIPES.items())
                total = len(recept_lista)

                if event.key == pygame.K_ESCAPE:
                    craft_menu = False
                elif event.key == pygame.K_UP:
                    if total > 0:
                        craft_selected = (craft_selected-1) % total
                        if craft_selected < craft_scroll:
                            craft_scroll = craft_selected
                elif event.key == pygame.K_DOWN:
                    if total > 0:
                        craft_selected = (craft_selected+1) % total
                        if craft_selected >= craft_scroll + CRAFT_ROWS:
                            craft_scroll = craft_selected - CRAFT_ROWS + 1
                elif event.key == pygame.K_RETURN:
                    if 0 <= craft_selected < total:
                        item_key, data = recept_lista[craft_selected]
                        try_craft(item_key)


            if event.key == pygame.K_m:
                map_visible = not map_visible
            elif event.key == pygame.K_i:
                inventory_visible = not inventory_visible                     
            # Bunker építés: 5 fa
            elif event.key == pygame.K_b:
                if inventory["wood"] >= 5:
                    inventory["wood"] -= 5
                    build_bunker_at(player_x, player_y)

            elif event.key in (pygame.K_1, pygame.K_2):
                b, _ = player_near_bunker_rect()
                if b is not None:
                    if event.key == pygame.K_1:
                        # deposit all
                        stor = b["storage"]
                        for key in item_names:
                            amt = inventory.get(key,0)
                            cap = get_item_capacity(key)
                            have = inventory.get(key, 0)
                            current = stor.get(key, 0)
                            free = max(0, cap - current)
                            move = min(amt, free)

                            if move > 0:
                                stor[key] = current + move
                                inventory[key] = have - move
                            
                    elif event.key == pygame.K_2:
                        # withdraw all
                        for key in item_names:
                            amt = b["storage"].get(key,0)
                            if amt > 0:
                                inventory[key] += amt
                                b["storage"][key] = 0
                    

    # Mozgás
    keys = pygame.key.get_pressed()
    if not craft_menu:
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
                if not craft_menu and  player_obj.colliderect(tile_obj):
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
    
    if inventory_visible:
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
        stext = f"Bunker: Wood {stor['wood']}  Rock {stor['rock']}  Food {stor['mushroom']}  Crystal {stor['crystal']}"
        screen.blit(font.render(stext, True, (0,0,0)), (10, 28))
    else:
        # építés súgó
        build_help = "Bunker epites: [B] (kell 5 fa)"
        screen.blit(font.render(build_help, True, (0,0,0)), (10, 10))

    if craft_menu:
        craft_menu_display(screen, inventory,RECIPES,item_names,craft_selected,craft_scroll, CRAFT_ROWS)
     
        if craft_message and (now - craft_message_time) <= CRAFT_MSG_DURATION:
            screen.blit(font.render(craft_message, True, (20, 20, 20)), (10, 35))


    if map_visible:
        screen.blit(minimap_surface, (WIDTH-MINIMAP_SIZE-10 , 10 ))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()