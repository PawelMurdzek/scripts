import binascii

def repeating_key_xor(ciphertext_bytes, key_bytes):
    """
    Applies a repeating key XOR to a byte string.
    
    Args:
        ciphertext_bytes (bytes): The raw bytes of the encrypted message.
        key_bytes (bytes): The raw bytes of the key.
        
    Returns:
        bytes: The resulting bytes after XORing.
    """
    if not key_bytes:
        return ciphertext_bytes
        
    decrypted_bytes = bytearray()
    for i in range(len(ciphertext_bytes)):
        decrypted_bytes.append(ciphertext_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return bytes(decrypted_bytes)

def score_text(text_bytes):
    """
    Scores a byte string based on the frequency of English characters.
    A higher score indicates a higher probability of being valid English text.
    """
    score = 0
    # A simple scoring mechanism: prioritize common English letters
    common_chars = b"ETAOIN SHRDLUetaoinshrdlu"
    for byte in text_bytes:
        if 32 <= byte <= 126: # Check for printable ASCII
            score += 1
        if bytes([byte]) in common_chars:
            score += 2 # Give extra points for very common characters
    return score

def single_byte_xor_brute_force(ciphertext_bytes):
    """
    Tries every possible single-byte key (0-255) to decrypt the ciphertext.
    
    Args:
        ciphertext_bytes (bytes): The raw bytes of the encrypted message.
        
    Returns:
        A list of tuples (score, key, decrypted_text) sorted by score.
    """
    results = []
    for key_val in range(256):
        key_byte = bytes([key_val])
        decrypted = repeating_key_xor(ciphertext_bytes, key_byte)
        score = score_text(decrypted)
        
        try:
            # Attempt to decode for display purposes
            decrypted_str = decrypted.decode('utf-8', errors='ignore')
            results.append((score, key_val, decrypted_str))
        except UnicodeDecodeError:
            continue
            
    # Sort results by score in descending order
    results.sort(key=lambda x: x[0], reverse=True)
    return results

def xor_with_key(input_string, key):
    """
    XOR each character in the input string with the given key.

    Args:
        input_string (str): The string to XOR.
        key (int): The integer key to XOR with.

    Returns:
        str: The resulting XORed string.
    """
    return ''.join(chr(ord(char) ^ key) for char in input_string)

def xor_hex_strings(hex1, hex2):
    """
    XOR two hexadecimal strings and return the result as a hexadecimal string.

    Args:
        hex1 (str): The first hexadecimal string.
        hex2 (str): The second hexadecimal string.

    Returns:
        str: The resulting XORed hexadecimal string.
    """
    bytes1 = bytes.fromhex(hex1)
    bytes2 = bytes.fromhex(hex2)
    result = bytes(a ^ b for a, b in zip(bytes1, bytes2))
    return result.hex()

def main():
    print("--- XOR Decrypter ---")
    print("1. Decrypt with known key")
    print("2. Brute-force single-byte XOR keys")
    print("3. XOR a string with a specific key")
    print("4. XOR two hexadecimal strings")

    choice = input("Choose an option (1/2/3/4): ").strip()

    if choice == "1":
        try:
            encrypted_hex = input("Enter the encrypted message (in hex format): ")
            ciphertext = binascii.unhexlify(encrypted_hex)
        except (binascii.Error, ValueError):
            print("Invalid hex input. Please provide a valid hex string.")
            return

        key_str = input("Enter the key (as a string): ")
        key = key_str.encode('utf-8')
        decrypted = repeating_key_xor(ciphertext, key)
        print(f"\nDecrypted message (in hex): {binascii.hexlify(decrypted).decode()}")
        print(f"Decrypted message (as text): {decrypted.decode('utf-8', errors='ignore')}")

    elif choice == "2":
        try:
            encrypted_hex = input("Enter the encrypted message (in hex format): ")
            ciphertext = binascii.unhexlify(encrypted_hex)
        except (binascii.Error, ValueError):
            print("Invalid hex input. Please provide a valid hex string.")
            return

        print("\n--- Brute-forcing single-byte XOR keys ---")
        brute_force_results = single_byte_xor_brute_force(ciphertext)

        print("Top 10 possible decryptions:")
        for i, (score, key, text) in enumerate(brute_force_results[:10]):
            print(f"#{i+1}: Score={score}, Key=0x{key:02x} ('{chr(key) if 32<=key<=126 else '.'}'), Text='{text}'")

    elif choice == "3":
        label = input("Enter the string to XOR: ")
        try:
            xor_key = int(input("Enter the XOR key (integer): "))
        except ValueError:
            print("Invalid key. Please provide an integer.")
            return

        result = xor_with_key(label, xor_key)
        print(f"\nOriginal Label: {label}")
        print(f"XORed Label with key {xor_key}: {result}")

    elif choice == "4":
        hex1 = input("Enter the first hex string: ")
        hex2 = input("Enter the second hex string: ")

        if len(hex1) != len(hex2):
            print("Error: Hex strings must be of the same length.")
        else:
            xor_result = xor_hex_strings(hex1, hex2)
            print(f"XOR Result: {xor_result}")

    else:
        print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
