def create_polybius_square():
    """Creates the standard 5x5 Polybius Square."""
    square = {}
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # I/J are combined
    k = 0
    for i in range(1, 6):
        for j in range(1, 6):
            # Map the coordinate pair (e.g., "11") to a letter
            square[f"{i}{j}"] = alphabet[k]
            k += 1
    return square

def polybius_decrypt(ciphertext):
    """
    Decrypts a message encrypted with the Polybius Square cipher.

    Args:
        ciphertext (str): The encrypted message (a string of digits).

    Returns:
        str: The decrypted plaintext.
    """
    square = create_polybius_square()
    decrypted_message = ""
    
    # Clean the input to only have digits
    cleaned_text = "".join(filter(str.isdigit, ciphertext))
    
    if len(cleaned_text) % 2 != 0:
        return "Error: The encrypted message must have an even number of digits."

    i = 0
    while i < len(cleaned_text):
        # Read two digits at a time
        coord_pair = cleaned_text[i:i+2]
        
        # Look up the letter in the square
        if coord_pair in square:
            decrypted_message += square[coord_pair]
        else:
            # Add a placeholder for unknown pairs
            decrypted_message += "?"
            
        i += 2
        
    return decrypted_message

if __name__ == "__main__":
    print("--- Polybius Square Decrypter ---")
    print("Note: This assumes a standard 5x5 grid where I and J are merged.")
    encrypted_message = input("Enter the encrypted message (pairs of numbers from 1-5): ")
    
    decrypted_message = polybius_decrypt(encrypted_message)
    
    print("\nDecrypted message:")
    print(decrypted_message)
