#!/usr/bin/env python3
"""
Hexadecimal String Encryption Tool

This script provides functions to convert ASCII text to hexadecimal string representations.
"""

def text_to_hex(text):
    """
    Convert text to a continuous hexadecimal string.

    Args:
        text (str): Text to convert.

    Returns:
        str: Hexadecimal string representation.
    """
    try:
        return ''.join(format(ord(char), '02x') for char in text)
    except Exception as e:
        return f"Error: {e}"

def text_to_hex_with_spaces(text):
    """
    Convert text to space-separated hexadecimal values.

    Args:
        text (str): Text to convert.

    Returns:
        str: Space-separated hexadecimal values.
    """
    try:
        return ' '.join(format(ord(char), '02x') for char in text)
    except Exception as e:
        return f"Error: {e}"

def text_to_hex_with_prefix(text):
    """
    Convert text to space-separated hexadecimal values with 0x prefix.

    Args:
        text (str): Text to convert.

    Returns:
        str: Space-separated hexadecimal values with 0x prefix.
    """
    try:
        return ' '.join(f"0x{format(ord(char), '02x')}" for char in text)
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

def base64_to_hex(base64_string):
    """
    Convert a Base64 string to a hexadecimal string.

    Args:
        base64_string (str): Base64 encoded string to convert.

    Returns:
        str: Hexadecimal string representation.
    """
    import base64
    try:
        # Decode Base64 to bytes
        byte_data = base64.b64decode(base64_string)
        # Convert bytes to hexadecimal string
        hex_string = byte_data.hex()
        return hex_string
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Hexadecimal String Encryption Tool")
    print("=" * 35)
    
    # Example encryption
    example_text = "crypto{You_will_be_working_with_hex_strings_a_lot}"
    print(f"Example text: '{example_text}'")
    example_result = text_to_hex(example_text)
    print(f"Encrypted hex string: {example_result}")
    print(f"Encrypted with spaces: {text_to_hex_with_spaces(example_text)}")
    print(f"Encrypted with 0x prefix: {text_to_hex_with_prefix(example_text)}")
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
            
            result = text_to_hex(user_input)
            print(f"Encrypted hex string: {result}")
        
        elif choice == '2':
            user_input = input("Enter text to encrypt: ")
            
            # Validate ASCII compatibility
            is_valid, invalid_chars = validate_ascii_characters(user_input)
            if not is_valid:
                print(f"Warning: Non-ASCII characters found: {invalid_chars}")
                print("Only ASCII characters (0-127) will be properly encrypted.")
            
            result = text_to_hex_with_spaces(user_input)
            print(f"Encrypted hex values: {result}")
        
        elif choice == '3':
            user_input = input("Enter text to encrypt: ")
            
            # Validate ASCII compatibility
            is_valid, invalid_chars = validate_ascii_characters(user_input)
            if not is_valid:
                print(f"Warning: Non-ASCII characters found: {invalid_chars}")
                print("Only ASCII characters (0-127) will be properly encrypted.")
            
            result = text_to_hex_with_prefix(user_input)
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