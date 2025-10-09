from collections import Counter

# Standard English letter frequencies
ENGLISH_FREQUENCIES = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

def vigenere_decrypt(ciphertext, key):
    """
    Decrypts a Vigenère-encrypted message with a known key.

    Args:
        ciphertext (str): The encrypted message.
        key (str): The keyword for decryption.

    Returns:
        str: The decrypted plaintext.
    """
    decrypted_text = ""
    key_index = 0
    key = key.upper()
    
    for char in ciphertext:
        if char.isalpha():
            # Get the shift value from the key (A=0, B=1, ...)
            shift = ord(key[key_index % len(key)]) - ord('A')
            
            # Determine the base (A or a)
            start = ord('A') if char.isupper() else ord('a')
            
            # Decrypt the character
            decrypted_char_code = (ord(char) - start - shift + 26) % 26
            decrypted_text += chr(start + decrypted_char_code)
            
            # Move to the next letter in the key
            key_index += 1
        else:
            # Keep non-alphabetic characters
            decrypted_text += char
            
    return decrypted_text

def analyze_ciphertext(ciphertext, key_length):
    """
    Performs frequency analysis on columns of the ciphertext to guess the key.
    """
    key_guess = ""
    ciphertext_upper = "".join(filter(str.isalpha, ciphertext.upper()))

    for i in range(key_length):
        # Create a column of text based on the key length
        column = ciphertext_upper[i::key_length]
        
        if not column:
            continue
            
        # Count letter frequencies in the column
        freq = Counter(column)
        best_shift = 0
        max_correlation = -1

        # Try all 26 possible shifts (for each letter of the alphabet)
        for shift in range(26):
            correlation = 0
            for char_code in range(26):
                char = chr(ord('A') + char_code)
                shifted_char = chr(ord('A') + (char_code - shift + 26) % 26)
                
                # Compare the shifted frequency with standard English frequencies
                correlation += (freq[char] / len(column)) * (ENGLISH_FREQUENCIES.get(shifted_char, 0.0) / 100)
            
            if correlation > max_correlation:
                max_correlation = correlation
                best_shift = shift
        
        key_guess += chr(ord('A') + best_shift)
        
    return key_guess


if __name__ == "__main__":
    print("--- Vigenère Cipher Decrypter ---")
    encrypted_message = input("Enter the message to decrypt: ")
    
    choice = input("Do you know the key? (yes/no): ").lower()
    
    if choice in ['yes', 'y']:
        key = input("Enter the keyword: ")
        decrypted_message = vigenere_decrypt(encrypted_message, key)
        print("\nDecrypted message:")
        print(decrypted_message)
    else:
        print("\nAttempting to analyze the ciphertext...")
        try:
            max_key_length = int(input("Enter maximum key length to test (e.g., 10): "))
            for length in range(2, max_key_length + 1):
                guessed_key = analyze_ciphertext(encrypted_message, length)
                print(f"Guessed key for length {length}: {guessed_key}")
                decrypted_attempt = vigenere_decrypt(encrypted_message, guessed_key)
                print(f"Decryption attempt: {decrypted_attempt[:80]}...") # Show a snippet
        except ValueError:
            print("Invalid input. Please enter a number.")
