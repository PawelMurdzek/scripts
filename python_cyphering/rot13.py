def rot13(text):
    """
    Applies the ROT13 substitution cipher to a given text.
    Each letter is 'rotated' by 13 places in the alphabet.
    Applying ROT13 twice restores the original text.

    Args:
        text (str): The input string.

    Returns:
        str: The text after applying ROT13.
    """
    result = ""
    for char in text:
        if 'a' <= char <= 'z':
            # Rotate lowercase letters
            result += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            # Rotate uppercase letters
            result += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
        else:
            # Keep non-alphabetic characters unchanged
            result += char
    return result

if __name__ == "__main__":
    print("--- ROT13 Cipher Encrypter ---")
    print("Note: ROT13 is symmetric - encoding and decoding use the same process")
    message = input("Enter the message to apply ROT13 to: ")
    processed_message = rot13(message)
    print("\nROT13 encoded message:")
    print(processed_message)