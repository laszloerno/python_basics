def clean_text(text):
    import unicodedata
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    return text.replace(" ", "").replace("\n", "")

def decode_message(key_text, distance_list):
    key_text = clean_text(key_text)
    message = ''
    index = -1

    for distance in distance_list:
        index += distance
        if index >= len(key_text):
            raise ValueError("A távolság túlmutat a kulcsszöveg végén.")
        message += key_text[index]

    return message

# 1. Kulcsszöveg beolvasása
with open("kulcs.txt", "r", encoding="utf-8") as file:
    key_text = file.read()

# 2. Kód (számsor) bekérése felhasználótól
input_str = input("Add meg a számsort vesszővel elválasztva (pl. 5,6,3,...): ")
try:
    distance_list = [int(x.strip()) for x in input_str.split(',')]
    decoded = decode_message(key_text, distance_list)
    print("\nVisszafejtett üzenet:")
    print(decoded)
except Exception as e:
    print("Hiba:", e)
