def clean_text(text):
    # Kisbetű, ékezetek nélkül, szóközök eltávolítása
    import unicodedata
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    return text.replace(" ", "").replace("\n", "")

def generate_distance_code(key_text, secret_message):
    key_text = clean_text(key_text)
    secret_message = clean_text(secret_message)

    distances = []
    current_index = -1

    for char in secret_message:
        next_index = key_text.find(char, current_index + 1)
        if next_index == -1:
            raise ValueError(f"A karakter '{char}' nem található a kulcsszövegben.")
        distances.append(next_index - current_index)
        current_index = next_index

    return distances

# 1. Kulcsszöveg beolvasása fájlból
with open("kulcs.txt", "r", encoding="utf-8") as file:
    key_text = file.read()

# 2. Titkosítandó szöveg bekérése
#secret_message = input("Add meg a titkosítandó szöveget: ")

try:
    secret_message = 'Palánta Tündér'
    code = generate_distance_code(key_text, secret_message)
    print(secret_message)
    print("\nTitkosított számsor:")
    print(code)

    secret_message = 'Scriptantia'
    code = generate_distance_code(key_text, secret_message)
    print(secret_message)
    print("\nTitkosított számsor:")
    print(code)

    secret_message = 'A siker első lépése, hogy elhidd: képes vagy rá!'
    code = generate_distance_code(key_text, secret_message)
    print(secret_message)
    print("\nTitkosított számsor:")
    print(code)

    secret_message = 'gratulálok nyertél egy kupont'
    code = generate_distance_code(key_text, secret_message)
    print(secret_message)    
    print("\nTitkosított számsor:")
    print(code)

except ValueError as e:
    print("Hiba:", e)
