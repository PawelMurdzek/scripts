from collections import Counter

# Letters in English, ordered by frequency (most to least common)
ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def get_frequency_order(text):
    """
    Returns a string of letters in the text, ordered by frequency.
    
    Args:
        text (str): The input text.
        
    Returns:
        str: A string of uppercase letters, from most to least frequent.
    """
    text = "".join(filter(str.isalpha, text.upper()))
    if not text:
        return ""
    
    # Count frequencies of each letter
    frequencies = Counter(text)
    
    # Sort letters by their frequency in descending order
    sorted_letters = sorted(frequencies, key=frequencies.get, reverse=True)
    
    return "".join(sorted_letters)

def build_decryption_map(cipher_freq_order):
    """
    Builds a decryption map based on letter frequency analysis.
    
    Args:
        cipher_freq_order (str): The frequency order of letters from the ciphertext.
        
    Returns:
        dict: A mapping from ciphertext letters to plaintext letters.
    """
    decryption_map = {}
    
    # Assume the most frequent letter in cipher maps to 'E', second to 'T', etc.
    map_size = min(len(cipher_freq_order), len(ENGLISH_FREQ_ORDER))
    
    for i in range(map_size):
        cipher_char = cipher_freq_order[i]
        plain_char = ENGLISH_FREQ_ORDER[i]
        decryption_map[cipher_char] = plain_char
        
    return decryption_map

def decrypt_with_map(ciphertext, decryption_map):
    """
    Decrypts a message using a provided character map.
    
    Args:
        ciphertext (str): The encrypted message.
        decryption_map (dict): The mapping of cipher chars to plain chars.
        
    Returns:
        str: The partially or fully decrypted message.
    """
    decrypted_text = ""
    for char in ciphertext:
        upper_char = char.upper()
        
        if upper_char in decryption_map:
            decrypted_char = decryption_map[upper_char]
            # Preserve original case
            decrypted_text += decrypted_char if char.isupper() else decrypted_char.lower()
        else:
            # If a character is not in our map (e.g., punctuation), keep it
            decrypted_text += char
            
    return decrypted_text

if __name__ == "__main__":
    print("--- Simple Substitution Cipher Decrypter (Frequency Analysis) ---")
    print("Note: This provides a best-guess based on letter frequencies.")
    print("You may need to manually swap letters to fully solve it.\n")
    
    encrypted_message = input("Enter the message to decrypt: ")
    
    # 1. Get the frequency order of the encrypted message
    cipher_order = get_frequency_order(encrypted_message)
    print(f"\nCiphertext frequency order: {cipher_order}")
    print(f"Standard English order:   {ENGLISH_FREQ_ORDER}")
    
    # 2. Build the initial decryption map
    initial_map = build_decryption_map(cipher_order)
    
    # 3. Perform the initial decryption
    decrypted_attempt = decrypt_with_map(encrypted_message, initial_map)
    
    print("\nInitial decryption attempt:")
    print(decrypted_attempt)
    
    # 4. Allow the user to refine the map
    while True:
        print("\n----------------------------------------------------")
        print("Current Map:", " ".join([f"{k}->{v}" for k, v in sorted(initial_map.items())]))
        choice = input("Swap two letters to refine (e.g., 'A=T'), type 'done' to exit: ").upper()
        
        if choice == 'DONE':
            break
        
        if '=' in choice and len(choice) == 3:
            try:
                cipher_char, plain_char = choice.split('=')
                if cipher_char.isalpha() and plain_char.isalpha():
                    # Find which key currently maps to the desired plain_char
                    current_key_for_plain_char = None
                    for k, v in initial_map.items():
                        if v == plain_char:
                            current_key_for_plain_char = k
                            break
                    
                    # Swap the mappings
                    if current_key_for_plain_char:
                        original_mapping = initial_map[cipher_char]
                        initial_map[cipher_char] = plain_char
                        initial_map[current_key_for_plain_char] = original_mapping
                        print(f"Swapped: {cipher_char} now maps to {plain_char}, and {current_key_for_plain_char} now maps to {original_mapping}.")
                    else: # If the plain_char wasn't in the map, just assign it
                        initial_map[cipher_char] = plain_char
                        print(f"Set mapping: {cipher_char} now maps to {plain_char}.")

                    decrypted_attempt = decrypt_with_map(encrypted_message, initial_map)
                    print("\nUpdated decryption attempt:")
                    print(decrypted_attempt)
                else:
                    print("Invalid format. Both characters must be letters.")
            except ValueError:
                print("Invalid input. Please use the format 'CipherLetter=PlainLetter' (e.g., 'X=A').")
        else:
            print("Invalid command.")
