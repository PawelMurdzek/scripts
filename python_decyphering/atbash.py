def atbash_cipher(text):
    """
    Encrypts or decrypts text using the Atbash cipher.
    The Atbash cipher is a substitution cipher with a specific key where the
    letters of the alphabet are reversed. A becomes Z, B becomes Y, etc.

    Args:
        text (str): The input text to be processed.

    Returns:
        str: The processed text after applying the Atbash cipher.
    """
    result = ""
    for char in text:
        if 'a' <= char <= 'z':
            # Reverse the lowercase alphabet
            result += chr(ord('a') + (ord('z') - ord(char)))
        elif 'A' <= char <= 'Z':
            # Reverse the uppercase alphabet
            result += chr(ord('A') + (ord('Z') - ord(char)))
        else:
            # Keep non-alphabetic characters as they are
            result += char
    return result

if __name__ == "__main__":
    print("--- Atbash Cipher Decrypter ---")
    message = input("Enter the message to decrypt: ")
    decrypted_message = atbash_cipher(message)
    print("\nDecrypted message:")
    print(decrypted_message)
