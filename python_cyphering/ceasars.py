def caesar_encrypt(plaintext, key):
    """
    Encrypts a message using the Caesar cipher with a given key.

    Args:
        plaintext (str): The message to encrypt.
        key (int): The integer key used for the shift (e.g., 3).

    Returns:
        str: The encrypted ciphertext message.
    """
    encrypted_message = ""
    for char in plaintext:
        if char.isalpha():  # Check if the character is an alphabet letter
            # Determine the starting ASCII value based on case
            start = ord('a') if char.islower() else ord('A')
            
            # Find the position of the character (0-25)
            position = ord(char) - start
            
            # Apply the shift
            shifted_position = (position + key) % 26
            
            # Convert back to a character and append
            encrypted_message += chr(start + shifted_position)
        else:
            # If it's not a letter (e.g., space, punctuation), keep it as is
            encrypted_message += char
            
    return encrypted_message

def generate_all_shifts(plaintext):
    """
    Generates all possible Caesar cipher shifts for a given plaintext.

    Args:
        plaintext (str): The message to encrypt.
    """
    print("\n--- All Possible Caesar Cipher Shifts ---")
    # There are 26 possible keys for the English alphabet
    for key in range(1, 26):
        encrypted_text = caesar_encrypt(plaintext, key)
        print(f"Key #{key:02d}: {encrypted_text}")
    print("------------------------------------------")

if __name__ == "__main__":
    print("--- Caesar Cipher Encrypter ---")
    
    # Get the message from the user
    plain_text = input("Enter the message to encrypt: ")
    
    while True:
        print("\nChoose operation:")
        print("1. Encrypt with specific key")
        print("2. Show all possible shifts")
        
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "1":
            try:
                shift_key = int(input("Enter the key (a number from 1 to 25): "))
                if 1 <= shift_key < 26:
                    encrypted_result = caesar_encrypt(plain_text, shift_key)
                    print(f"\nEncrypted message with key {shift_key}:")
                    print(encrypted_result)
                    break
                else:
                    print("Invalid key. Please enter a number between 1 and 25.")
            except ValueError:
                print("Invalid input. Please enter a number for the key.")
                
        elif choice == "2":
            generate_all_shifts(plain_text)
            break
            
        else:
            print("Invalid choice. Please enter 1 or 2.")