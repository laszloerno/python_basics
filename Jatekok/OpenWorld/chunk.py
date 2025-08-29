import random

CHUNK_SIZE = 16

def generate_chunk(cx, cy):
    random.seed(f"{cx},{cy}")
    tiles = []
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            if random.random() < 0.001:
                tiles.append({"type":"tree","x":x,"y":y})
            if random.random() < 0.0015:
                tiles.append({"type":"rock","x":x,"y":y})
            if random.random() < 0.0018:
                tiles.append({"type":"mushroom","x":x,"y":y})
            if random.random() < 0.002:
                tiles.append({"type":"crystal","x":x,"y":y})
    return tiles

chunk_cache = {}

def get_chunk(cx,cy):
    key = (cx,cy)
    if key not in chunk_cache:
        chunk_cache[key] = generate_chunk(cx,cy)
    return chunk_cache[key]