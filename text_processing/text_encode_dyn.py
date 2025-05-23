import random

def encode_hungarian_text_with_random_shift(text):
    """
    Encodes the given text by shifting each character in the Hungarian alphabet by a random amount (1-7).
    The encoded character is followed by the shift value.

    :param text: The input text to encode.
    :return: The encoded text with shift values.
    """
    hungarian_alphabet = "aábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz"
    encoded_text = ""

    for char in text:
        if char.lower() in hungarian_alphabet:
            is_upper = char.isupper()
            index = hungarian_alphabet.index(char.lower())
            shift = random.randint(1, 7)  # Random shift between 1 and 7
            new_index = (index + shift) % len(hungarian_alphabet)
            new_char = hungarian_alphabet[new_index]
            encoded_text += (new_char.upper() if is_upper else new_char) + str(shift)
        else:
            # Keep non-alphabetic characters unchanged
            encoded_text += char

    return encoded_text


if __name__ == "__main__":
    input_text = input("Adja meg a szöveget: ")
    result = encode_hungarian_text_with_random_shift(input_text)
    print("Átkódolt szöveg:", result)