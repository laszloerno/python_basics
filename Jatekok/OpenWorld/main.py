import pygame
import random
import time
from chunk import get_chunk
from parameters import  OBJECT_TYPES, RECIPES, item_names, CRAFT_TEXT_COLOR, CRAFT_NOT_POSSIBLE_COLOR, get_item_capacity
import craft

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

 




def render_bunker_hud(surface,font, storage:dict,item_names:dict, get_item_capacity,x=10, y=28, row_h=18):
    items = [(item_names.get(k, k.capitalize()), k, v) for k, v in storage.items() if v > 0]
    #items.sort(key=lambda t: t[0].lower())
    if not items:
        surface.blit(font.render("Bunker üres.", True, (80, 80, 80)), (x, y))
        return
    for i, (label, key, val) in enumerate(items):
        cap = get_item_capacity(key)
        color = (160,30,30) if val >=cap else (0,0,0)
        surface.blit(font.render(f" {label}: {val}/{cap}", True, color ), (x, y+i*row_h  ) )    



bunker_menu_open = False
bunker_menu_mode = None # deposit | withdraw
bunker_menu_idx = 0
bunker_menu_scroll = 0
BUNKER_MENU_ROWS = 12

bunker_menu_qty = {}
bunker_menu_target = None

def bunker_menu_max_for_item(mode, key, storage, inventory, get_item_capacity):
    if mode == "deposit":
        have = inventory.get(key, 0)
        cap = get_item_capacity(key)
        cur = storage.get(key,0)
        free = max(0 , cap-cur)
        return min(have, free)
    elif mode == "withdraw":
        return storage.get(key,0)
    return 0

def open_bunker_menu(mode, bunker, inventory, item_names, get_item_capacity):
    global bunker_menu_open,bunker_menu_mode,bunker_menu_idx,bunker_menu_scroll,bunker_menu_qty,bunker_menu_target
    bunker_menu_open = True
    bunker_menu_mode = mode
    bunker_menu_idx = 0
    bunker_menu_scroll = 0
    bunker_menu_qty = {}
    bunker_menu_target = bunker

    storage = bunker["storage"]
    for key in item_names:
        max_move = bunker_menu_max_for_item(mode,key,storage,inventory,get_item_capacity)
        if max_move > 0:
            bunker_menu_qty[key] = 0

def close_bunker_menu():
    global bunker_menu_open,bunker_menu_mode,bunker_menu_idx,bunker_menu_scroll,bunker_menu_qty,bunker_menu_target
    bunker_menu_open = False
    bunker_menu_mode = None
    bunker_menu_idx = 0
    bunker_menu_scroll = 0
    bunker_menu_qty = {}
    bunker_menu_target = None
 

def render_bunker_menu(surface, font, item_names, inventory, get_item_capacity):
    if not bunker_menu_open or bunker_menu_target is None:
        return
    W,H = surface.get_size()
    overlay = pygame.Surface((W,H), pygame.SRCALPHA)
    overlay.fill((0,0,0,160))
    surface.blit(overlay,(0,0))

    panel_w, panel_h = 600,600
    panel_x = (W-panel_w) // 2
    panel_y = (H-panel_h) // 2

    pygame.draw.rect(surface, (235,235,240), (panel_x, panel_y, panel_w, panel_h), border_radius=12)
    pygame.draw.rect(surface, (40,40,60), (panel_x, panel_y, panel_w, panel_h),2, border_radius=12)

    title_text = ""
    if bunker_menu_mode == "deposit":
        title_text = "Bunker - lerakodás (válassz mennyiséget!)" 
    else:
        title_text = "Bunker - felvétel (válassz mennyiséget!)" 

    surface.blit(font.render(title_text, True, (20,20,30)), (panel_x+16, panel_y+16))
    help_text = "FEL/LE sor | JOBB/BAL ±1 | Shift+JOBB/BAL ±10 | Home/End 0/max | Enter OK | Esc mégse"
    surface.blit(font.render(help_text, True, (20,20,30)), (panel_x+16, panel_y+34))
    
    keys = list(bunker_menu_qty.keys())
    
    y = panel_y + 65
    surface.blit(font.render("Tárgy", True, (40,40,60)) , (panel_x+20, y) )
    surface.blit(font.render("Készlet (zsák/bunker)", True, (40,40,60)) , (panel_x+120, y) )
    surface.blit(font.render("Max mozgatható", True, (40,40,60)) , (panel_x+350, y) )
    surface.blit(font.render("Kiválasztott", True, (40,40,60)) , (panel_x+460, y) )

    y += 6
    start = bunker_menu_scroll
    end = min(start+BUNKER_MENU_ROWS, len(keys))
    row_h = 28
    y = panel_y + 90

    storage = bunker_menu_target["storage"]
    for idx in range(start,end):
        key = keys[idx]
        sel = idx == bunker_menu_idx
        if sel:
            pygame.draw.rect(surface, (210,225,255), (panel_x+12, y-4, panel_w-24, row_h), border_radius=6)
        label = item_names.get(key, key.capitalize())

        zsak = inventory.get(key,0)
        bunk = storage.get(key,0)

        max_move = bunker_menu_max_for_item(bunker_menu_mode, key,storage,inventory, get_item_capacity)
        chosen = bunker_menu_qty.get(key,0)

        surface.blit(font.render(label,True,(10,10,20)) , (panel_x+20,y))
        surface.blit(font.render(f"{zsak}/{bunk}",True,(10,10,20)) , (panel_x+120,y))
        surface.blit(font.render(str(max_move),True,(10,10,20)) , (panel_x+350,y))
        col = (160,30,30) if chosen > max_move else (20,20,20)
        surface.blit(font.render(str(chosen),True,col) , (panel_x+460,y))
        y += row_h



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
                    build_bunker_at(player_x, player_y)

            elif event.key in (pygame.K_1, pygame.K_2):
                b, _ = player_near_bunker_rect()
                if b is not None:
                    if event.key == pygame.K_1:
                        open_bunker_menu("deposit", b, inventory, item_names, get_item_capacity)
                    elif event.key == pygame.K_2:
                        open_bunker_menu("withdraw", b, inventory, item_names, get_item_capacity)
  

            if bunker_menu_open:
                keys = list(bunker_menu_qty.keys())
                total = len(keys)

                if event.key == pygame.K_ESCAPE:
                    close_bunker_menu()
                    continue
                
                if event.key == pygame.K_UP:
                    bunker_menu_idx = (bunker_menu_idx-1) % total
                    if bunker_menu_idx < bunker_menu_scroll:
                        bunker_menu_scroll = bunker_menu_idx
                
                elif event.key == pygame.K_DOWN:
                    bunker_menu_idx = (bunker_menu_idx +1) % total
                    if bunker_menu_idx >= bunker_menu_scroll+BUNKER_MENU_ROWS:
                        bunker_menu_scroll = bunker_menu_scroll+BUNKER_MENU_ROWS+1
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_0, pygame.K_9):
                    key = keys[bunker_menu_idx]
                    storage = bunker_menu_target['storage']
                    max_move = bunker_menu_max_for_item(bunker_menu_mode, key, storage, inventory, get_item_capacity)
                    cur = bunker_menu_qty.get(key,0)
                    
                    step = 10 if (pygame.key.get_mods() and pygame.KMOD_SHIFT) else 1

                    if event.key == pygame.K_LEFT:
                        cur = max(0, cur-step)
                    elif event.key == pygame.K_RIGHT:
                        cur = min(max_move, cur + step)
                    elif event.key == pygame.K_0:
                        cur = 0
                    elif event.key == pygame.K_9:
                        cur = max_move
                    bunker_menu_qty[key] = cur
                elif event.key == pygame.K_RETURN:
                    storage = bunker_menu_target['storage']
                    for key,chosen in bunker_menu_qty.items():
                        max_move = bunker_menu_max_for_item(bunker_menu_mode, key, storage, inventory, get_item_capacity)
                        chosen = min(chosen, max_move)
                        if chosen <= 0:
                            continue
                        if bunker_menu_mode == "deposit":
                            inventory[key] -= chosen
                            storage[key] = storage.get(key,0) + chosen
                        else:
                            storage[key] -= chosen
                            inventory[key] = inventory.get(key,0) + chosen
                    close_bunker_menu()
            if craft.handle_keydown(event,inventory):
                continue

    # Mozgás
    keys = pygame.key.get_pressed()
    if not craft.is_open() and not bunker_menu_open:
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
                if not craft.is_open() and not bunker_menu_open and player_obj.colliderect(tile_obj):
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
        help1 = "[1] Letét (összes), [2] Felvét (összes)"
        screen.blit(font.render(help1, True, (0,0,0)), (10, 10))

        stor = near_bunker["storage"]
        render_bunker_hud(screen, font, stor,item_names,get_item_capacity, x=10, y = 28, row_h=18)

         

    else:
        # építés súgó
        build_help = "Bunker epites: [B] (kell 5 fa)"
        screen.blit(font.render(build_help, True, (0,0,0)), (10, 10))

    craft.render(screen, font, inventory)
        


    if map_visible:
        screen.blit(minimap_surface, (WIDTH-MINIMAP_SIZE-10 , 10 ))

    render_bunker_menu(screen,font,item_names, inventory, get_item_capacity)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()