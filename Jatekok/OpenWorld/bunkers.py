import pygame
from parameters import item_names, get_item_capacity

BUNKER_COLOR = (150, 120, 80)  # egyszerű barna
BUNKER_SIZE_TILES = 2          # 2x2 csempe


bunkers = []  

def get_bunkers():
    """A bunker lista lekérdezése (rajzoláshoz, minimaphez)."""
    return bunkers

def build_bunker_at(px, py, tile_size: int):
    bx = (px // tile_size) * tile_size
    by = (py // tile_size) * tile_size
    bunkers.append({
        "x": bx,
        "y": by,
        "storage": {key : 0 for key in item_names}
    })

def player_near_bunker_rect(player_x, player_y, tile_size: int):
    """Visszaadja a bunker dict-et és pygame.Rect-et, ha a játékos hozzáér valamelyik bunkerhez, különben (None, None)."""
    player_rect = pygame.Rect(player_x, player_y, tile_size, tile_size)
    for b in bunkers:
        rect = pygame.Rect(b["x"], b["y"], BUNKER_SIZE_TILES*tile_size, BUNKER_SIZE_TILES*tile_size)
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

def is_menu_open() -> bool:
    return bunker_menu_open

def bunker_menu_max_for_item(mode, key, storage, inventory):
    if mode == "deposit":
        have = inventory.get(key, 0)
        cap = get_item_capacity(key)
        cur = storage.get(key,0)
        free = max(0 , cap-cur)
        return min(have, free)
    elif mode == "withdraw":
        return storage.get(key,0)
    return 0

def open_bunker_menu(mode, bunker, inventory, item_names):
    global bunker_menu_open,bunker_menu_mode,bunker_menu_idx,bunker_menu_scroll,bunker_menu_qty,bunker_menu_target
    bunker_menu_open = True
    bunker_menu_mode = mode
    bunker_menu_idx = 0
    bunker_menu_scroll = 0
    bunker_menu_qty = {}
    bunker_menu_target = bunker

    storage = bunker["storage"]
    for key in item_names:
        max_move = bunker_menu_max_for_item(mode,key,storage,inventory)
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

        max_move = bunker_menu_max_for_item(bunker_menu_mode, key,storage,inventory)
        chosen = bunker_menu_qty.get(key,0)

        surface.blit(font.render(label,True,(10,10,20)) , (panel_x+20,y))
        surface.blit(font.render(f"{zsak}/{bunk}",True,(10,10,20)) , (panel_x+120,y))
        surface.blit(font.render(str(max_move),True,(10,10,20)) , (panel_x+350,y))
        col = (160,30,30) if chosen > max_move else (20,20,20)
        surface.blit(font.render(str(chosen),True,col) , (panel_x+460,y))
        y += row_h

def handle_keydown(event: pygame.event.Event, inventory: dict) -> bool:
    """
    A bunker menü billentyűkezelése.
    True: az eseményt a bunker menü elnyelte (ne menjen tovább a főprogramnak).
    False: a főprogram még használhatja.
    """
    global bunker_menu_idx, bunker_menu_scroll

    if not bunker_menu_open or bunker_menu_target is None:
        return False

    keys = list(bunker_menu_qty.keys())
    total = len(keys)
    if total == 0:
        # Üres menü -> Esc zárja
        if event.key == pygame.K_ESCAPE:
            close_bunker_menu()
            return True
        return True  # menü nyitva, de nincs mit csinálni

    if event.key == pygame.K_ESCAPE:
        close_bunker_menu()
        return True

    if event.key == pygame.K_UP:
        bunker_menu_idx = (bunker_menu_idx - 1) % total
        if bunker_menu_idx < bunker_menu_scroll:
            bunker_menu_scroll = bunker_menu_idx
        return True

    if event.key == pygame.K_DOWN:
        bunker_menu_idx = (bunker_menu_idx + 1) % total
        if bunker_menu_idx >= bunker_menu_scroll + BUNKER_MENU_ROWS:
            bunker_menu_scroll = bunker_menu_idx - BUNKER_MENU_ROWS + 1
        return True

    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_0, pygame.K_9):
        key = keys[bunker_menu_idx]
        storage = bunker_menu_target['storage']
        max_move = bunker_menu_max_for_item(
            bunker_menu_mode, key, storage, inventory
        )
        cur = bunker_menu_qty.get(key, 0)

        # Itt picit pontosítottam a SHIFT ellenőrzést
        mods = pygame.key.get_mods()
        step = 10 if (mods & pygame.KMOD_SHIFT) else 1

        if event.key == pygame.K_LEFT:
            cur = max(0, cur - step)
        elif event.key == pygame.K_RIGHT:
            cur = min(max_move, cur + step)
        elif event.key == pygame.K_0:
            cur = 0
        elif event.key == pygame.K_9:
            cur = max_move

        bunker_menu_qty[key] = cur
        return True

    if event.key == pygame.K_RETURN:
        storage = bunker_menu_target['storage']
        for key, chosen in bunker_menu_qty.items():
            max_move = bunker_menu_max_for_item(
                bunker_menu_mode, key, storage, inventory
            )
            chosen = min(chosen, max_move)
            if chosen <= 0:
                continue

            if bunker_menu_mode == "deposit":
                inventory[key] -= chosen
                storage[key] = storage.get(key, 0) + chosen
            else:
                storage[key] -= chosen
                inventory[key] = inventory.get(key, 0) + chosen

        close_bunker_menu()
        return True

    # Más gomb – menü nyitva van, de nem használtuk
    return False