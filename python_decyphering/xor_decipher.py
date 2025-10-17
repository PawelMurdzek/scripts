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

def brute_force_single_byte_xor_from_hex(hex_string):
    """
    Brute-force single-byte XOR decryption for a given hex string.

    Args:
        hex_string (str): The hex string to decrypt.

    Returns:
        list: Top 10 possible decryptions as tuples (score, key, text).
    """
    ciphertext = bytes.fromhex(hex_string)
    return single_byte_xor_brute_force(ciphertext)

def brute_force_single_byte_xor_from_input(hex_string=None):
    """
    Brute-force single-byte XOR decryption for a user-provided hex string.
    
    Args:
        hex_string (str, optional): The hex string to decrypt. If None, prompts user for input.
    """
    if hex_string is None:
        hex_string = input("Enter the encrypted message (in hex format): ").strip()
    
    try:
        ciphertext = bytes.fromhex(hex_string)
    except ValueError:
        print("Invalid hex input. Please provide a valid hex string.")
        return

    print("\n--- Brute-forcing single-byte XOR keys ---")
    brute_force_results = single_byte_xor_brute_force(ciphertext)

    print("Top 100 possible decryptions:")
    for i, (score, key, text) in enumerate(brute_force_results):#(brute_force_results[:100]):
        print(f"#{i+1}: Score={score}, Key=0x{key:02x} ('{chr(key) if 32<=key<=126 else '.'}'), Text='{text}'")

def main():
    print("=" * 50)
    print("--- XOR Decrypter ---")
    print("=" * 50)
    print("1. Decrypt with known key (hex input)")
    print("2. Brute-force single-byte XOR (hex input)")
    print("3. XOR a string with a specific key")
    print("4. XOR two hexadecimal strings")
    print("=" * 50)

    choice = input("Choose an option (1-4): ").strip()

    if choice == "1":
        # Decrypt with known key
        encrypted_hex = input("Enter the encrypted message (in hex format): ").strip()
        try:
            ciphertext = binascii.unhexlify(encrypted_hex)
        except (binascii.Error, ValueError):
            print("Invalid hex input. Please provide a valid hex string.")
            return

        key_str = input("Enter the key (as a string): ").strip()
        if not key_str:
            print("Key cannot be empty.")
            return
            
        key = key_str.encode('utf-8')
        decrypted = repeating_key_xor(ciphertext, key)
        print(f"\nDecrypted message (in hex): {binascii.hexlify(decrypted).decode()}")
        print(f"Decrypted message (as text): {decrypted.decode('utf-8', errors='ignore')}")

    elif choice == "2":
        # Brute-force single-byte XOR
        brute_force_single_byte_xor_from_input()

    elif choice == "3":
        # XOR a string with a specific key
        label = input("Enter the string to XOR: ").strip()
        if not label:
            print("String cannot be empty.")
            return
            
        try:
            xor_key = int(input("Enter the XOR key (integer 0-255): ").strip())
            if not 0 <= xor_key <= 255:
                print("Key must be between 0 and 255.")
                return
        except ValueError:
            print("Invalid key. Please provide an integer.")
            return

        result = xor_with_key(label, xor_key)
        print(f"\nOriginal string: {label}")
        print(f"XORed string with key {xor_key}: {result}")
        print(f"Result in hex: {result.encode('utf-8', errors='ignore').hex()}")

    elif choice == "4":
        # XOR two hexadecimal strings
        hex1 = input("Enter the first hex string: ").strip()
        hex2 = input("Enter the second hex string: ").strip()

        try:
            # Validate hex strings
            bytes.fromhex(hex1)
            bytes.fromhex(hex2)
        except ValueError:
            print("Error: Invalid hex string format.")
            return

        if len(hex1) != len(hex2):
            print("Error: Hex strings must be of the same length.")
            print(f"Length of first: {len(hex1)}, Length of second: {len(hex2)}")
        else:
            xor_result = xor_hex_strings(hex1, hex2)
            print(f"\nXOR Result (hex): {xor_result}")
            try:
                print(f"XOR Result (text): {bytes.fromhex(xor_result).decode('utf-8', errors='ignore')}")
            except:
                pass

    else:
        print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
