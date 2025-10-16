#!/usr/bin/env python3
"""
Hexadecimal String Encryption Tool
Converts ASCII text to hexadecimal string representation.
"""

def encrypt_to_hex_string(text):
    """
    Encrypt text to a continuous hexadecimal string.
    
    Args:
        text (str): Text to encrypt
    
    Returns:
        str: Hexadecimal string representation
    """
    try:
        hex_string = ''
        for char in text:
            ascii_value = ord(char)
            # Convert to hexadecimal (without 0x prefix) and ensure 2 digits
            hex_value = format(ascii_value, '02x')
            hex_string += hex_value
        
        return hex_string
    
    except Exception as e:
        return f"Error: {e}"

def encrypt_to_hex_with_spaces(text):
    """
    Encrypt text to space-separated hexadecimal values.
    
    Args:
        text (str): Text to encrypt
    
    Returns:
        str: Space-separated hexadecimal values
    """
    try:
        hex_values = []
        for char in text:
            ascii_value = ord(char)
            # Convert to hexadecimal (without 0x prefix) and ensure 2 digits
            hex_value = format(ascii_value, '02x')
            hex_values.append(hex_value)
        
        return ' '.join(hex_values)
    
    except Exception as e:
        return f"Error: {e}"

def encrypt_to_hex_with_prefix(text):
    """
    Encrypt text to space-separated hexadecimal values with 0x prefix.
    
    Args:
        text (str): Text to encrypt
    
    Returns:
        str: Space-separated hexadecimal values with 0x prefix
    """
    try:
        hex_values = []
        for char in text:
            ascii_value = ord(char)
            # Convert to hexadecimal with 0x prefix and ensure 2 digits
            hex_value = f"0x{format(ascii_value, '02x')}"
            hex_values.append(hex_value)
        
        return ' '.join(hex_values)
    
    except Exception as e:
        return f"Error: {e}"

def validate_ascii_characters(text):
    """
    Check if all characters in text are valid ASCII (0-127).
    
    Args:
        text (str): Text to validate
    
    Returns:
        tuple: (is_valid, invalid_chars_info)
    """
    invalid_chars = []
    for char in text:
        ascii_value = ord(char)
        if ascii_value > 127:
            invalid_chars.append((char, ascii_value))
    
    return len(invalid_chars) == 0, invalid_chars

def main():
    print("Hexadecimal String Encryption Tool")
    print("=" * 35)
    
    # Example encryption
    example_text = "crypto{You_will_be_working_with_hex_strings_a_lot}"
    print(f"Example text: '{example_text}'")
    example_result = encrypt_to_hex_string(example_text)
    print(f"Encrypted hex string: {example_result}")
    print(f"Encrypted with spaces: {encrypt_to_hex_with_spaces(example_text)}")
    print(f"Encrypted with 0x prefix: {encrypt_to_hex_with_prefix(example_text)}")
    print()
    
    while True:
        print("\nChoose an option:")
        print("1. Encrypt to continuous hex string")
        print("2. Encrypt to space-separated hex values")
        print("3. Encrypt to hex values with 0x prefix")
        print("4. Check ASCII compatibility")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            user_input = input("Enter text to encrypt: ")
            
            # Validate ASCII compatibility
            is_valid, invalid_chars = validate_ascii_characters(user_input)
            if not is_valid:
                print(f"Warning: Non-ASCII characters found: {invalid_chars}")
                print("Only ASCII characters (0-127) will be properly encrypted.")
            
            result = encrypt_to_hex_string(user_input)
            print(f"Encrypted hex string: {result}")
        
        elif choice == '2':
            user_input = input("Enter text to encrypt: ")
            
            # Validate ASCII compatibility
            is_valid, invalid_chars = validate_ascii_characters(user_input)
            if not is_valid:
                print(f"Warning: Non-ASCII characters found: {invalid_chars}")
                print("Only ASCII characters (0-127) will be properly encrypted.")
            
            result = encrypt_to_hex_with_spaces(user_input)
            print(f"Encrypted hex values: {result}")
        
        elif choice == '3':
            user_input = input("Enter text to encrypt: ")
            
            # Validate ASCII compatibility
            is_valid, invalid_chars = validate_ascii_characters(user_input)
            if not is_valid:
                print(f"Warning: Non-ASCII characters found: {invalid_chars}")
                print("Only ASCII characters (0-127) will be properly encrypted.")
            
            result = encrypt_to_hex_with_prefix(user_input)
            print(f"Encrypted hex values with prefix: {result}")
        
        elif choice == '4':
            user_input = input("Enter text to validate: ")
            is_valid, invalid_chars = validate_ascii_characters(user_input)
            
            if is_valid:
                print("✓ All characters are valid ASCII")
            else:
                print(f"✗ Non-ASCII characters found:")
                for char, code in invalid_chars:
                    print(f"  '{char}' (code: {code})")
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()