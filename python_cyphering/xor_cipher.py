import binascii
import random
import string

def repeating_key_xor(plaintext_bytes, key_bytes):
    """
    Applies a repeating key XOR to a byte string.
    
    Args:
        plaintext_bytes (bytes): The raw bytes of the message to encrypt.
        key_bytes (bytes): The raw bytes of the key.
        
    Returns:
        bytes: The resulting encrypted bytes after XORing.
    """
    if not key_bytes:
        return plaintext_bytes
        
    encrypted_bytes = bytearray()
    for i in range(len(plaintext_bytes)):
        encrypted_bytes.append(plaintext_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return bytes(encrypted_bytes)

def single_byte_xor_encrypt(plaintext_bytes, key_byte):
    """
    Encrypts text using a single-byte XOR key.
    
    Args:
        plaintext_bytes (bytes): The raw bytes of the message to encrypt.
        key_byte (int): The single byte key (0-255).
        
    Returns:
        bytes: The encrypted bytes.
    """
    encrypted_bytes = bytearray()
    for byte in plaintext_bytes:
        encrypted_bytes.append(byte ^ key_byte)
    return bytes(encrypted_bytes)

def generate_random_key(length):
    """
    Generates a random key of specified length.
    
    Args:
        length (int): The length of the key in bytes.
        
    Returns:
        bytes: A random key.
    """
    return bytes([random.randint(0, 255) for _ in range(length)])

def generate_random_string_key(length):
    """
    Generates a random string key of specified length.
    
    Args:
        length (int): The length of the key in characters.
        
    Returns:
        str: A random string key.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

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
    print("=" * 50)
    print("--- XOR Encrypter ---")
    print("=" * 50)
    print("1. Single-byte XOR encryption")
    print("2. Repeating key XOR (string key)")
    print("3. Repeating key XOR (random key)")
    print("4. XOR a string with a specific key")
    print("5. XOR two hexadecimal strings")
    print("=" * 50)

    choice = input("Choose an option (1-5): ").strip()

    if choice == "1":
        # Single-byte XOR
        message = input("\nEnter the message to encrypt: ").strip()
        if not message:
            print("Error: Message cannot be empty.")
            return
            
        message_bytes = message.encode('utf-8')
        
        try:
            key_input = input("Enter key (0-255 or leave empty for random): ").strip()
            if key_input == "":
                key_byte = random.randint(1, 255)
                print(f"Generated random key: {key_byte}")
            else:
                key_byte = int(key_input)
                if not (0 <= key_byte <= 255):
                    print("Error: Key must be between 0 and 255.")
                    return

            encrypted = single_byte_xor_encrypt(message_bytes, key_byte)
            print(f"\nOriginal message: {message}")
            print(f"Key used: {key_byte} (0x{key_byte:02x})")
            print(f"Encrypted message (hex): {binascii.hexlify(encrypted).decode()}")
            print(f"\n{'='*50}")
            print("IMPORTANT: Save the key for decryption!")
            print("="*50)
        except ValueError:
            print("Error: Please enter a valid number.")

    elif choice == "2":
        # String key XOR
        message = input("\nEnter the message to encrypt: ").strip()
        if not message:
            print("Error: Message cannot be empty.")
            return
            
        message_bytes = message.encode('utf-8')
        
        key_string = input("Enter the key string: ").strip()
        if not key_string:
            print("Error: Key cannot be empty.")
            return

        key_bytes = key_string.encode('utf-8')
        encrypted = repeating_key_xor(message_bytes, key_bytes)

        print(f"\nOriginal message: {message}")
        print(f"Key used: '{key_string}'")
        print(f"Encrypted message (hex): {binascii.hexlify(encrypted).decode()}")
        print(f"\n{'='*50}")
        print("IMPORTANT: Save the key for decryption!")
        print("="*50)

    elif choice == "3":
        # Random key XOR
        message = input("\nEnter the message to encrypt: ").strip()
        if not message:
            print("Error: Message cannot be empty.")
            return
            
        message_bytes = message.encode('utf-8')
        
        try:
            key_length = int(input("Enter key length (1-20): ").strip())
            if not (1 <= key_length <= 20):
                print("Error: Key length must be between 1 and 20.")
                return

            print("\nChoose key type:")
            print("a. Random string (printable characters)")
            print("b. Random bytes (0-255)")

            key_type = input("Enter choice (a or b): ").strip().lower()

            if key_type == "a":
                key_string = generate_random_string_key(key_length)
                key_bytes = key_string.encode('utf-8')
                print(f"Generated key: '{key_string}'")
            elif key_type == "b":
                key_bytes = generate_random_key(key_length)
                print(f"Generated key (hex): {binascii.hexlify(key_bytes).decode()}")
            else:
                print("Invalid choice.")
                return

            encrypted = repeating_key_xor(message_bytes, key_bytes)
            print(f"\nOriginal message: {message}")
            print(f"Encrypted message (hex): {binascii.hexlify(encrypted).decode()}")
            print(f"\n{'='*50}")
            print("IMPORTANT: Save the key for decryption!")
            print("="*50)
        except ValueError:
            print("Error: Please enter a valid number.")

    elif choice == "4":
        # XOR a string with a specific key
        label = input("\nEnter the string to XOR: ").strip()
        if not label:
            print("Error: String cannot be empty.")
            return
            
        try:
            xor_key = int(input("Enter the XOR key (integer 0-255): ").strip())
            if not 0 <= xor_key <= 255:
                print("Error: Key must be between 0 and 255.")
                return
        except ValueError:
            print("Error: Invalid key. Please provide an integer.")
            return

        result = xor_with_key(label, xor_key)
        print(f"\nOriginal string: {label}")
        print(f"XOR key: {xor_key}")
        print(f"XORed string: {result}")
        print(f"Result in hex: {result.encode('utf-8', errors='ignore').hex()}")

    elif choice == "5":
        # XOR two hexadecimal strings
        hex1 = input("\nEnter the first hex string: ").strip()
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
        print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()
