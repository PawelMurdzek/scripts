def create_polybius_square():
    """Creates the standard 5x5 Polybius Square for encoding."""
    square = {}
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # I/J are combined
    k = 0
    for i in range(1, 6):
        for j in range(1, 6):
            # Map each letter to its coordinate pair (e.g., A -> "11")
            square[alphabet[k]] = f"{i}{j}"
            k += 1
    return square

def polybius_encrypt(plaintext):
    """
    Encrypts a message using the Polybius Square cipher.

    Args:
        plaintext (str): The message to encrypt.

    Returns:
        str: The encrypted message (a string of coordinate pairs).
    """
    square = create_polybius_square()
    encrypted_message = ""
    
    for char in plaintext.upper():
        if char.isalpha():
            # Handle the I/J combination
            if char == 'J':
                char = 'I'
            
            if char in square:
                encrypted_message += square[char] + " "
            else:
                # This shouldn't happen with our alphabet
                encrypted_message += "?? "
        elif char == ' ':
            # Optionally separate words with a special marker
            encrypted_message += "/ "
        else:
            # Skip non-alphabetic characters or handle them differently
            continue
            
    return encrypted_message.strip()

def display_polybius_square():
    """Displays the Polybius Square for reference."""
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    print("\nPolybius Square Reference:")
    print("   1  2  3  4  5")
    k = 0
    for i in range(1, 6):
        row = f"{i} "
        for j in range(1, 6):
            row += f" {alphabet[k]} "
            k += 1
        print(row)
    print("\nNote: I and J share the same position (24)")

if __name__ == "__main__":
    print("--- Polybius Square Encrypter ---")
    print("This cipher converts each letter to coordinate pairs (1-5, 1-5)")
    
    # Show the square for reference
    display_polybius_square()
    
    message = input("\nEnter the message to encrypt: ")
    
    encrypted_message = polybius_encrypt(message)
    
    print("\nEncrypted message:")
    print(encrypted_message)
    
    print("\nFormat: Each pair of numbers represents one letter")
    print("Spaces separate letters, '/' separates words")