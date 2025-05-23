import random

def encode_hungarian_text_with_word_length_shift(text):
    """
    Encodes the given text by shifting each character in the Hungarian alphabet by the length of the word.
    The shift value is displayed at the beginning of each word.

    :param text: The input text to encode.
    :return: The encoded text with shift values at the beginning of each word.
    """
    hungarian_alphabet = "aábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz"
    encoded_text = ""
    current_word = ""

    for char in text:
        if char == " ":
            # Process the current word
            if current_word:
                shift = len(current_word)  # Shift equals the length of the word
                encoded_text += f"[{shift}]"
                for word_char in current_word:
                    is_upper = word_char.isupper()
                    index = hungarian_alphabet.index(word_char.lower())
                    new_index = (index + shift) % len(hungarian_alphabet)
                    new_char = hungarian_alphabet[new_index]
                    encoded_text += new_char.upper() if is_upper else new_char
                current_word = ""
            encoded_text += char  # Add the space
        elif char.lower() in hungarian_alphabet:
            current_word += char  # Build the current word
        else:
            # Process non-alphabetic characters
            if current_word:
                shift = len(current_word)
                encoded_text += f"[{shift}]"
                for word_char in current_word:
                    is_upper = word_char.isupper()
                    index = hungarian_alphabet.index(word_char.lower())
                    new_index = (index + shift) % len(hungarian_alphabet)
                    new_char = hungarian_alphabet[new_index]
                    encoded_text += new_char.upper() if is_upper else new_char
                current_word = ""
            encoded_text += char  # Add the non-alphabetic character

    # Process the last word if any
    if current_word:
        shift = len(current_word)
        encoded_text += f"[{shift}]"
        for word_char in current_word:
            is_upper = word_char.isupper()
            index = hungarian_alphabet.index(word_char.lower())
            new_index = (index + shift) % len(hungarian_alphabet)
            new_char = hungarian_alphabet[new_index]
            encoded_text += new_char.upper() if is_upper else new_char

    return encoded_text


if __name__ == "__main__":
    input_text = input("Adja meg a szöveget: ")
    result = encode_hungarian_text_with_word_length_shift(input_text)
    print("Átkódolt szöveg:", result)