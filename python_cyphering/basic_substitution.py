import random
import string

def generate_substitution_key():
    """
    Generates a random substitution key by shuffling the alphabet.
    
    Returns:
        dict: A dictionary mapping each letter to its substitute.
    """
    alphabet = list(string.ascii_uppercase)
    shuffled = alphabet.copy()
    random.shuffle(shuffled)
    
    substitution_key = {}
    for i, letter in enumerate(alphabet):
        substitution_key[letter] = shuffled[i]
    
    return substitution_key

def create_custom_substitution_key():
    """
    Allows the user to create a custom substitution key.
    
    Returns:
        dict: A dictionary mapping each letter to its substitute.
    """
    print("Create a custom substitution key.")
    print("Enter the substitute alphabet (26 unique letters):")
    print("Standard alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    while True:
        substitute_alphabet = input("Your substitute alphabet: ").upper().replace(" ", "")
        
        if len(substitute_alphabet) != 26:
            print("Error: Please enter exactly 26 letters.")
            continue
        
        if len(set(substitute_alphabet)) != 26:
            print("Error: All letters must be unique.")
            continue
        
        if not all(c.isalpha() for c in substitute_alphabet):
            print("Error: Only alphabetic characters are allowed.")
            continue
        
        break
    
    alphabet = string.ascii_uppercase
    substitution_key = {}
    for i, letter in enumerate(alphabet):
        substitution_key[letter] = substitute_alphabet[i]
    
    return substitution_key

def encrypt_with_substitution(plaintext, substitution_key):
    """
    Encrypts a message using a substitution cipher.
    
    Args:
        plaintext (str): The message to encrypt.
        substitution_key (dict): The substitution mapping.
        
    Returns:
        str: The encrypted message.
    """
    encrypted_text = ""
    for char in plaintext:
        upper_char = char.upper()
        
        if upper_char in substitution_key:
            encrypted_char = substitution_key[upper_char]
            # Preserve original case
            encrypted_text += encrypted_char if char.isupper() else encrypted_char.lower()
        else:
            # If it's not a letter (e.g., punctuation), keep it as is
            encrypted_text += char
            
    return encrypted_text

def display_key(substitution_key):
    """
    Displays the substitution key in a readable format.
    
    Args:
        substitution_key (dict): The substitution mapping.
    """
    alphabet = string.ascii_uppercase
    print("\nSubstitution Key:")
    print("Plain:  " + " ".join(alphabet))
    print("Cipher: " + " ".join([substitution_key[letter] for letter in alphabet]))

if __name__ == "__main__":
    print("--- Simple Substitution Cipher Encrypter ---")
    
    # Get the message to encrypt
    message = input("Enter the message to encrypt: ")
    
    # Choose key generation method
    print("\nChoose key generation method:")
    print("1. Generate random key")
    print("2. Create custom key")
    
    while True:
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            substitution_key = generate_substitution_key()
            break
        elif choice == "2":
            substitution_key = create_custom_substitution_key()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    # Display the key
    display_key(substitution_key)
    
    # Encrypt the message
    encrypted_message = encrypt_with_substitution(message, substitution_key)
    
    print("\nEncrypted message:")
    print(encrypted_message)
    
    # Save the key for decryption
    print("\n" + "="*50)
    print("IMPORTANT: Save this key for decryption!")
    key_string = "".join([substitution_key[letter] for letter in string.ascii_uppercase])
    print(f"Key string: {key_string}")
    print("="*50)