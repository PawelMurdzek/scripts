def vigenere_encrypt(plaintext, key):
    """
    Encrypts a message using the Vigenère cipher with a given key.

    Args:
        plaintext (str): The message to encrypt.
        key (str): The keyword for encryption.

    Returns:
        str: The encrypted ciphertext.
    """
    encrypted_text = ""
    key_index = 0
    key = key.upper()
    
    for char in plaintext:
        if char.isalpha():
            # Get the shift value from the key (A=0, B=1, ...)
            shift = ord(key[key_index % len(key)]) - ord('A')
            
            # Determine the base (A or a)
            start = ord('A') if char.isupper() else ord('a')
            
            # Encrypt the character
            encrypted_char_code = (ord(char) - start + shift) % 26
            encrypted_text += chr(start + encrypted_char_code)
            
            # Move to the next letter in the key
            key_index += 1
        else:
            # Keep non-alphabetic characters
            encrypted_text += char
            
    return encrypted_text

def generate_random_key(length):
    """
    Generates a random key of specified length.
    
    Args:
        length (int): The length of the key to generate.
        
    Returns:
        str: A random key consisting of uppercase letters.
    """
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def display_vigenere_table():
    """
    Displays a portion of the Vigenère table for reference.
    """
    print("\nVigenère Square (first 6 rows for reference):")
    print("Key\\Plain: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")
    
    for i in range(6):
        key_char = chr(ord('A') + i)
        row = f"    {key_char}:    "
        for j in range(26):
            encrypted_char = chr((i + j) % 26 + ord('A'))
            row += encrypted_char + " "
        print(row)
    print("...")

if __name__ == "__main__":
    print("--- Vigenère Cipher Encrypter ---")
    print("The Vigenère cipher uses a repeating keyword to encrypt text.")
    
    # Get the message to encrypt
    message = input("\nEnter the message to encrypt: ")
    
    # Get the key
    print("\nChoose key option:")
    print("1. Enter your own key")
    print("2. Generate a random key")
    
    while True:
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            keyword = input("Enter the keyword (letters only): ").upper()
            if keyword.isalpha():
                break
            else:
                print("Error: Please enter only alphabetic characters.")
        elif choice == "2":
            try:
                length = int(input("Enter key length (1-20): "))
                if 1 <= length <= 20:
                    keyword = generate_random_key(length)
                    print(f"Generated key: {keyword}")
                    break
                else:
                    print("Error: Please enter a length between 1 and 20.")
            except ValueError:
                print("Error: Please enter a valid number.")
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    # Show the Vigenère table reference
    display_vigenere_table()
    
    # Encrypt the message
    encrypted_message = vigenere_encrypt(message, keyword)
    
    print(f"\nKey used: {keyword}")
    print("Encrypted message:")
    print(encrypted_message)
    
    print(f"\n{'='*50}")
    print("IMPORTANT: Save the key for decryption!")
    print(f"Key: {keyword}")
    print("="*50)