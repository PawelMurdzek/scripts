#!/usr/bin/env python3
"""
7-bit ASCII Encryption Tool
Converts readable text to ASCII decimal values.
"""

def encrypt_to_ascii_array(text):
    """
    Encrypt text to an array of ASCII decimal values.
    
    Args:
        text (str): Text to encrypt
    
    Returns:
        list: List of ASCII decimal values
    """
    try:
        # Convert each character to its ASCII value
        ascii_array = [ord(char) for char in text if ord(char) <= 127]
        return ascii_array
    except (ValueError, TypeError) as e:
        return f"Error: {e}"

def encrypt_to_ascii_string(text, separator=', '):
    """
    Encrypt text to a string of comma-separated ASCII values.
    
    Args:
        text (str): Text to encrypt
        separator (str): Separator between ASCII values (default: ', ')
    
    Returns:
        str: Comma-separated ASCII values
    """
    try:
        ascii_array = encrypt_to_ascii_array(text)
        if isinstance(ascii_array, list):
            return separator.join(map(str, ascii_array))
        return ascii_array  # Error message
    except Exception as e:
        return f"Error: {e}"

def validate_ascii_7bit(text):
    """
    Check if all characters in text are valid 7-bit ASCII (0-127).
    
    Args:
        text (str): Text to validate
    
    Returns:
        tuple: (is_valid, invalid_chars)
    """
    invalid_chars = []
    for char in text:
        if ord(char) > 127:
            invalid_chars.append(char)
    
    return len(invalid_chars) == 0, invalid_chars

def main():
    print("7-bit ASCII Encryption Tool")
    print("=" * 30)
    
    # Example encryption
    example_text = "crypto{ASCII_pr1nt4bl3}"
    print(f"Example text: '{example_text}'")
    example_result = encrypt_to_ascii_array(example_text)
    print(f"Encrypted array: {example_result}")
    print(f"Encrypted string: {encrypt_to_ascii_string(example_text)}")
    print()
    
    while True:
        print("\nChoose an option:")
        print("1. Encrypt text to ASCII array")
        print("2. Encrypt text to comma-separated ASCII values")
        print("3. Check if text is valid 7-bit ASCII")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            user_input = input("Enter text to encrypt: ")
            
            # Validate 7-bit ASCII
            is_valid, invalid_chars = validate_ascii_7bit(user_input)
            if not is_valid:
                print(f"Warning: The following characters are not 7-bit ASCII: {invalid_chars}")
                print("Only 7-bit ASCII characters will be encrypted.")
            
            result = encrypt_to_ascii_array(user_input)
            print(f"Encrypted array: {result}")
        
        elif choice == '2':
            user_input = input("Enter text to encrypt: ")
            separator = input("Enter separator (default is ', '): ").strip()
            if not separator:
                separator = ', '
            
            # Validate 7-bit ASCII
            is_valid, invalid_chars = validate_ascii_7bit(user_input)
            if not is_valid:
                print(f"Warning: The following characters are not 7-bit ASCII: {invalid_chars}")
                print("Only 7-bit ASCII characters will be encrypted.")
            
            result = encrypt_to_ascii_string(user_input, separator)
            print(f"Encrypted string: {result}")
        
        elif choice == '3':
            user_input = input("Enter text to validate: ")
            is_valid, invalid_chars = validate_ascii_7bit(user_input)
            
            if is_valid:
                print("✓ All characters are valid 7-bit ASCII")
            else:
                print(f"✗ Invalid 7-bit ASCII characters found: {invalid_chars}")
                print(f"Character codes: {[ord(char) for char in invalid_chars]}")
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()