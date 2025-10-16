#!/usr/bin/env python3
"""
7-bit ASCII Decryption Tool
Converts ASCII decimal values to readable text.
"""

def decrypt_ascii_array(ascii_array):
    """
    Decrypt an array of ASCII decimal values to readable text.
    
    Args:
        ascii_array (list): List of ASCII decimal values (0-127)
    
    Returns:
        str: Decrypted text
    """
    try:
        # Convert each ASCII value to its corresponding character
        decrypted_text = ''.join(chr(value) for value in ascii_array if 0 <= value <= 127)
        return decrypted_text
    except (ValueError, TypeError) as e:
        return f"Error: {e}"

def decrypt_ascii_string(ascii_string):
    """
    Decrypt a string of comma-separated ASCII values to readable text.
    
    Args:
        ascii_string (str): Comma-separated ASCII values
    
    Returns:
        str: Decrypted text
    """
    try:
        # Parse the string to extract ASCII values
        ascii_values = [int(x.strip()) for x in ascii_string.split(',')]
        return decrypt_ascii_array(ascii_values)
    except (ValueError, TypeError) as e:
        return f"Error: {e}"

def main():
    print("7-bit ASCII Decryption Tool")
    print("=" * 30)
    
    # Example with the provided array
    provided_array = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]
    
    print(f"Provided array: {provided_array}")
    decrypted_result = decrypt_ascii_array(provided_array)
    print(f"Decrypted text: {decrypted_result}")
    print()
    
    while True:
        print("\nChoose an option:")
        print("1. Decrypt ASCII array (Python list format)")
        print("2. Decrypt comma-separated ASCII values")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            try:
                user_input = input("Enter ASCII array (e.g., [72, 101, 108, 108, 111]): ").strip()
                # Safe evaluation of list input
                ascii_array = eval(user_input) if user_input.startswith('[') and user_input.endswith(']') else []
                
                if not isinstance(ascii_array, list):
                    print("Error: Please enter a valid list format")
                    continue
                
                result = decrypt_ascii_array(ascii_array)
                print(f"Decrypted text: {result}")
                
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            user_input = input("Enter comma-separated ASCII values (e.g., 72, 101, 108, 108, 111): ").strip()
            result = decrypt_ascii_string(user_input)
            print(f"Decrypted text: {result}")
        
        elif choice == '3':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()