import random
import time


CHUNK_SIZE = 16

MOB_TYPES = {"allat", "madar"}


def _spawn_mob_fields(obj):
    """Mozgó entitásokhoz state mezők."""
    now = time.time()
    obj["mob"] = True
    obj["next_move_at"] = now + random.uniform(0.2, 1.0)  # mikor lép legközelebb
    return obj


def generate_chunk(cx, cy):
    random.seed(f"{cx},{cy}")
    tiles = []
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            if random.random() < 0.005:
                tiles.append({"type":"wood","x":x,"y":y})
            if random.random() < 0.005:
                tiles.append({"type":"bokor","x":x,"y":y})                
            if random.random() < 0.0015:
                tiles.append({"type":"rock","x":x,"y":y})
            if random.random() < 0.0013:
                tiles.append({"type":"mushroom","x":x,"y":y})
            if random.random() < 0.002:
                tiles.append({"type":"crystal","x":x,"y":y})
            if random.random()< 0.0002:
                tiles.append({'type':'varazskristaly','x':x,'y':y})
            if random.random()< 0.0016:
                tiles.append(_spawn_mob_fields({"type": "allat", "x": x, "y": y}))
            if random.random()< 0.0014:
                tiles.append(_spawn_mob_fields({"type": "madar", "x": x, "y": y}))
            if random.random() < 0.001:
                tiles.append({"type":"vaserc","x":x,"y":y})                               
    return tiles

chunk_cache = {}

def get_chunk(cx,cy):
    key = (cx,cy)
    if key not in chunk_cache:
        chunk_cache[key] = generate_chunk(cx,cy)
    return chunk_cache[key]

def update_chunk_mobs(cx, cy, now=None):
    """
    Frissíti egy chunk mobjait (allat/madar): random lép 1-et a chunkon belül.
    """
    if now is None:
        now = time.time()

    tiles = get_chunk(cx, cy)

    # gyors index, hogy ne lépjenek egymásra (opcionális, de hasznos)
    occupied = {(o["x"], o["y"]) for o in tiles}

    for obj in tiles:
        if obj.get("type") not in MOB_TYPES:
            continue

        # ha valamiért régi chunkból jött mob és nincs mező
        if "next_move_at" not in obj:
            _spawn_mob_fields(obj)

        if now < obj["next_move_at"]:
            continue

        # köv lépés ideje
        obj["next_move_at"] = now + random.uniform(0.2, 1.0)

        # néha ne mozduljon (természetesebb)
        if random.random() < 0.25:
            continue

        # 4 irány (vagy bővítsd 8-ra)
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(dirs)

        ox, oy = obj["x"], obj["y"]

        for dx, dy in dirs:
            nx, ny = ox + dx, oy + dy
            if 0 <= nx < CHUNK_SIZE and 0 <= ny < CHUNK_SIZE:
                # ne lépjen rá fix tárgyra / másik mobra
                if (nx, ny) in occupied:
                    continue

                # foglaltság frissítés
                occupied.remove((ox, oy))
                occupied.add((nx, ny))

                obj["x"], obj["y"] = nx, ny
                break