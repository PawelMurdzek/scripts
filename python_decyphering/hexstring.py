#!/usr/bin/env python3
"""
Hexadecimal String Decryption Tool
Converts hexadecimal strings to readable ASCII text.
"""

def decrypt_hex_string(hex_string):
    """
    Decrypt a hexadecimal string to readable ASCII text.
    
    Args:
        hex_string (str): Hexadecimal string (without 0x prefix)
    
    Returns:
        str: Decrypted ASCII text
    """
    try:
        # Remove any whitespace and convert to lowercase
        hex_string = hex_string.replace(' ', '').replace('\n', '').lower()
        
        # Remove 0x prefix if present
        if hex_string.startswith('0x'):
            hex_string = hex_string[2:]
        
        # Check if hex string has even length
        if len(hex_string) % 2 != 0:
            return "Error: Hexadecimal string must have even length"
        
        # Convert hex pairs to ASCII characters
        decrypted_text = ''
        for i in range(0, len(hex_string), 2):
            hex_pair = hex_string[i:i+2]
            ascii_value = int(hex_pair, 16)
            
            # Check if it's a valid ASCII character (0-127)
            if 0 <= ascii_value <= 127:
                decrypted_text += chr(ascii_value)
            else:
                decrypted_text += f'[{ascii_value}]'  # Non-ASCII values in brackets
        
        return decrypted_text
    
    except ValueError as e:
        return f"Error: Invalid hexadecimal string - {e}"
    except Exception as e:
        return f"Error: {e}"

def decrypt_hex_with_spaces(hex_string):
    """
    Decrypt a space-separated hexadecimal string to readable ASCII text.
    
    Args:
        hex_string (str): Space-separated hexadecimal values
    
    Returns:
        str: Decrypted ASCII text
    """
    try:
        # Split by spaces and process each hex value
        hex_values = hex_string.strip().split()
        decrypted_text = ''
        
        for hex_val in hex_values:
            # Remove 0x prefix if present
            if hex_val.startswith('0x'):
                hex_val = hex_val[2:]
            
            ascii_value = int(hex_val, 16)
            
            # Check if it's a valid ASCII character (0-127)
            if 0 <= ascii_value <= 127:
                decrypted_text += chr(ascii_value)
            else:
                decrypted_text += f'[{ascii_value}]'  # Non-ASCII values in brackets
        
        return decrypted_text
    
    except ValueError as e:
        return f"Error: Invalid hexadecimal value - {e}"
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Hexadecimal String Decryption Tool")
    print("=" * 35)
    
    # Example with the provided hex string
    provided_hex = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
    
    print(f"Provided hex string: {provided_hex}")
    decrypted_result = decrypt_hex_string(provided_hex)
    print(f"Decrypted text: {decrypted_result}")
    print()
    
    while True:
        print("\nChoose an option:")
        print("1. Decrypt continuous hex string")
        print("2. Decrypt space-separated hex values")
        print("3. Decrypt hex string with 0x prefix")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            user_input = input("Enter continuous hex string: ").strip()
            result = decrypt_hex_string(user_input)
            print(f"Decrypted text: {result}")
        
        elif choice == '2':
            user_input = input("Enter space-separated hex values (e.g., 48 65 6c 6c 6f): ").strip()
            result = decrypt_hex_with_spaces(user_input)
            print(f"Decrypted text: {result}")
        
        elif choice == '3':
            user_input = input("Enter hex string with 0x prefix: ").strip()
            result = decrypt_hex_string(user_input)
            print(f"Decrypted text: {result}")
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()