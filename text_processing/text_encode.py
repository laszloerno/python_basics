def encode_hungarian_text(text, shift):
    """
    Encodes the given text by shifting each character in the Hungarian alphabet by the specified amount.
    
    :param text: The input text to encode.
    :param shift: The number of positions to shift each character.
    :return: The encoded text.
    """
    hungarian_alphabet = "aábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz."
    encoded_text = ""

    for char in text:
        if char.lower() in hungarian_alphabet:
            is_upper = char.isupper()
            index = hungarian_alphabet.index(char.lower())
            new_index = (index + shift) % len(hungarian_alphabet)
            new_char = hungarian_alphabet[new_index]
            encoded_text += new_char.upper() if is_upper else new_char
        else:
            # Keep non-alphabetic characters unchanged
            encoded_text += char

    return encoded_text


if __name__ == "__main__":
    input_text = input("Adja meg a szöveget: ")
    shift = int(input("Adja meg az eltolás mértékét: "))
    result = encode_hungarian_text(input_text, shift)
    print("Átkódolt szöveg:", result)