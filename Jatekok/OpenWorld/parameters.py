import pygame
pygame.init()

CRAFT_TEXT_COLOR = (20,20,40)
CRAFT_NOT_POSSIBLE_COLOR = (240,20,20)

item_names = {"wood":"Fa", 
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

OBJECT_TYPES = {
    "wood":(34,139,34),
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


RECIPES = {
    "balta": {
        "name": "Balta",
        "cost": {"wood": 1, "rock": 1},   # 1 fa + 1 kő
        "key": pygame.K_b
    },
    "csakany": {
        "name": "Csákány",
        "cost": {"wood": 1, "rock": 2},   # példa: 1 fa + 2 kő
        "key": pygame.K_c
    },
    "vas": {
        "name": "Vas",
        # példa recept: kristályból olvasztasz "vas"-at (csak demó)
        "cost": {"crystal": 2},
        "key": pygame.K_v
    },
      "varazspalca": {
        "name": "Varázspálca",
        # példa recept: kristályból olvasztasz "vas"-at (csak demó)
        "cost": {"crystal": 1, "wood":3},
        "key": pygame.K_0
    },
      "ij": {
        "name": "Íj",
        # példa recept: kristályból olvasztasz "vas"-at (csak demó)
        "cost": {"wood": 2, "bel":1},
        "key": pygame.K_p
    },
}


# ---- BUNKER CAPACITY ----
BUNKER_MAX_PER_ITEM = 50  # alapértelmezett max / item

# (opcionális) egyedi limitek itemenként:
BUNKER_CAPACITY = {
    # "wood": 100,
    # "rock": 80,
    # "mushroom": 60,
    # "crystal": 30,
    # ...
}
def get_item_capacity(key: str) -> int:
    return BUNKER_CAPACITY.get(key, BUNKER_MAX_PER_ITEM)