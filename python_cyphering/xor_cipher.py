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

def main():
    print("--- XOR Encrypter ---")
    print("1. Single-byte XOR")
    print("2. Repeating key XOR (string key)")
    print("3. Repeating key XOR (random key)")

    # Get the message to encrypt
    message = input("\nEnter the message to encrypt: ")
    message_bytes = message.encode('utf-8')

    choice = input("Choose an option (1/2/3): ").strip()

    if choice == "1":
        # Single-byte XOR
        try:
            key_input = input("Enter key (0-255 or leave empty for random): ")
            if key_input == "":
                key_byte = random.randint(1, 255)
                print(f"Generated random key: {key_byte}")
            else:
                key_byte = int(key_input)
                if not (0 <= key_byte <= 255):
                    print("Error: Key must be between 0 and 255.")
                    return

            encrypted = single_byte_xor_encrypt(message_bytes, key_byte)
            print(f"\nKey used: {key_byte} (0x{key_byte:02x})")
            print(f"Encrypted message (hex): {binascii.hexlify(encrypted).decode()}")
        except ValueError:
            print("Error: Please enter a valid number.")

    elif choice == "2":
        # String key XOR
        key_string = input("Enter the key string: ")
        if not key_string:
            print("Error: Key cannot be empty.")
            return

        key_bytes = key_string.encode('utf-8')
        encrypted = repeating_key_xor(message_bytes, key_bytes)

        print(f"\nKey used: '{key_string}'")
        print(f"Encrypted message (hex): {binascii.hexlify(encrypted).decode()}")

    elif choice == "3":
        # Random key XOR
        try:
            key_length = int(input("Enter key length (1-20): "))
            if not (1 <= key_length <= 20):
                print("Error: Key length must be between 1 and 20.")
                return

            print("\nChoose key type:")
            print("a. Random string (printable characters)")
            print("b. Random bytes (0-255)")

            key_type = input("Enter choice (a or b): ").lower()

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
            print(f"\nEncrypted message (hex): {binascii.hexlify(encrypted).decode()}")
        except ValueError:
            print("Error: Please enter a valid number.")

    else:
        print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()

print(f"\n{'='*60}")
print("IMPORTANT: Save the key for decryption!")
print("Use the hex output for decryption with the XOR decrypter.")
print("="*60)