def caesar_decrypt(ciphertext, key):
    """
    Decrypts a message using the Caesar cipher with a given key.

    Args:
        ciphertext (str): The encrypted message.
        key (int): The integer key used for the shift (e.g., 3).

    Returns:
        str: The decrypted plaintext message.
    """
    decrypted_message = ""
    for char in ciphertext:
        if char.isalpha():  # Check if the character is an alphabet letter
            # Determine the starting ASCII value based on case
            start = ord('a') if char.islower() else ord('A')
            
            # Find the position of the character (0-25)
            position = ord(char) - start
            
            # Apply the reverse shift
            shifted_position = (position - key) % 26
            
            # Convert back to a character and append
            decrypted_message += chr(start + shifted_position)
        else:
            # If it's not a letter (e.g., space, punctuation), keep it as is
            decrypted_message += char
            
    return decrypted_message

def brute_force_decrypt(ciphertext):
    """
    Attempts to decrypt a Caesar cipher message by trying all possible keys.

    Args:
        ciphertext (str): The encrypted message.
    """
    print("\n--- Brute-Forcing All Possible Keys ---")
    # There are 26 possible keys for the English alphabet
    for key in range(1, 26):
        decrypted_text = caesar_decrypt(ciphertext, key)
        print(f"Key #{key:02d}: {decrypted_text}")
    print("--------------------------------------")


if __name__ == "__main__":
    print("Caesar Cipher Decrypter")
    
    # Get the encrypted message from the user
    encrypted_text = input("Enter the message to decrypt: ")
    
    while True:
        # Ask the user if they know the key
        choice = input("Do you know the key? (yes/no): ").lower()
        
        if choice in ['yes', 'y']:
            try:
                shift_key = int(input("Enter the key (a number from 1 to 25): "))
                if 1 <= shift_key < 26:
                    decrypted_result = caesar_decrypt(encrypted_text, shift_key)
                    print(f"\nDecrypted message: {decrypted_result}")
                    break
                else:
                    print("Invalid key. Please enter a number between 1 and 25.")
            except ValueError:
                print("Invalid input. Please enter a number for the key.")
                
        elif choice in ['no', 'n']:
            brute_force_decrypt(encrypted_text)
            print("\nLook through the list above to find the message that makes sense.")
            break
            
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")
