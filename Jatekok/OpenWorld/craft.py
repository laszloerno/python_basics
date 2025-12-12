import pygame
import time
from parameters import  OBJECT_TYPES, RECIPES, item_names, CRAFT_TEXT_COLOR, CRAFT_NOT_POSSIBLE_COLOR, get_item_capacity


craft_message = ""
craft_message_time = 0
CRAFT_MSG_DURATION = 2.0  # másodperc

craft_menu_open = False
craft_selected = 0
craft_scroll = 0
CRAFT_ROWS = 10

def is_open() -> bool:
    return craft_menu_open

def can_craft(inventory, cost:dict) -> bool:
    for resource, need in cost.items():
        if inventory.get(resource,0) < need:
            return False
    return True

def try_craft(item_key, inventory):
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


def craft_menu_display(surface,font , inventory):
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

    recept_lista = list(RECIPES.items())
    osszees_recept = len(recept_lista)

    fejlec = font.render("Tárgy                         Költség", True, CRAFT_TEXT_COLOR)
    surface.blit(fejlec, (panel_x+150, panel_y+25))


    start = craft_scroll
    end = min(craft_scroll+CRAFT_ROWS,osszees_recept)

    row_y = panel_y + 80
    row_h = 28

    for idx in range(start,end):
        key, data = recept_lista[idx]
        name = data.get("name",key.capitalize())
        cost = data.get("cost", {})

        if craft_selected ==idx:
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


def render(surface, font, inventory):
    if not craft_menu_open:
        return
    
    craft_menu_display(surface, font, inventory)

    if craft_message and (time.time() - craft_message_time) <= CRAFT_MSG_DURATION:
        surface.blit(font.render(craft_message, True, (20, 20, 20)), (10, 35))


def handle_keydown(event: pygame.event.Event, inventory):
    global craft_menu_open, craft_selected, craft_scroll

    if event.key == pygame.K_c:
        craft_menu_open = not craft_menu_open
        return True
    
    if not craft_menu_open:
        return False
    
    recept_lista = list(RECIPES.items())
    total = len(recept_lista)

    if event.key == pygame.K_ESCAPE:
        craft_menu_open = False
        return True

    elif event.key == pygame.K_UP:
        if total > 0:
            craft_selected = (craft_selected-1) % total
            if craft_selected < craft_scroll:
                craft_scroll = craft_selected
        return True
    elif event.key == pygame.K_DOWN:
        if total > 0:
            craft_selected = (craft_selected+1) % total
            if craft_selected >= craft_scroll + CRAFT_ROWS:
                craft_scroll = craft_selected - CRAFT_ROWS + 1
        return True
    elif event.key == pygame.K_RETURN:
        if 0 <= craft_selected < total:
            item_key, data = recept_lista[craft_selected]
            try_craft(item_key,inventory)
        return True

    return False