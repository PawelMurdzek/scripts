import os
import sys

# Zero-width characters for steganography
ZERO_WIDTH_SPACE = '\u200B'      # Zero Width Space
ZERO_WIDTH_JOINER = '\u200D'     # Zero Width Joiner
ZERO_WIDTH_NON_JOINER = '\u200C' # Zero Width Non-Joiner
WORD_JOINER = '\u2060'           # Word Joiner

# Binary to zero-width character mapping
BINARY_TO_INVISIBLE = {
    '00': ZERO_WIDTH_SPACE,
    '01': ZERO_WIDTH_JOINER,
    '10': ZERO_WIDTH_NON_JOINER,
    '11': WORD_JOINER
}

# Reverse mapping for decoding
INVISIBLE_TO_BINARY = {v: k for k, v in BINARY_TO_INVISIBLE.items()}

def text_to_binary(text):
    """
    Converts text to binary representation.
    
    Args:
        text (str): The input text to convert.
        
    Returns:
        str: Binary representation of the text.
    """
    binary = ''
    for char in text:
        # Convert each character to 8-bit binary
        binary += format(ord(char), '08b')
    return binary

def binary_to_invisible(binary_str):
    """
    Converts binary string to invisible characters.
    
    Args:
        binary_str (str): Binary string to convert.
        
    Returns:
        str: String of invisible characters.
    """
    # Pad binary string to make it divisible by 2
    if len(binary_str) % 2 != 0:
        binary_str += '0'
    
    invisible_text = ''
    for i in range(0, len(binary_str), 2):
        pair = binary_str[i:i+2]
        invisible_text += BINARY_TO_INVISIBLE[pair]
    
    return invisible_text

def invisible_to_binary(invisible_text):
    """
    Converts invisible characters back to binary.
    
    Args:
        invisible_text (str): String of invisible characters.
        
    Returns:
        str: Binary representation.
    """
    binary = ''
    for char in invisible_text:
        if char in INVISIBLE_TO_BINARY:
            binary += INVISIBLE_TO_BINARY[char]
    return binary

def binary_to_text(binary_str):
    """
    Converts binary string back to text.
    
    Args:
        binary_str (str): Binary string to convert.
        
    Returns:
        str: Decoded text.
    """
    text = ''
    # Process 8 bits at a time
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) == 8:  # Only process complete bytes
            text += chr(int(byte, 2))
    return text

def encode_file_to_invisible(input_file, output_file):
    """
    Encodes a text file to invisible characters and saves to output file.
    
    Args:
        input_file (str): Path to input file.
        output_file (str): Path to output file.
    """
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Input file size: {len(content)} characters")
        
        # Convert to binary
        binary = text_to_binary(content)
        print(f"Binary representation: {len(binary)} bits")
        
        # Convert to invisible characters
        invisible_content = binary_to_invisible(binary)
        print(f"Invisible characters: {len(invisible_content)} characters")
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(invisible_content)
        
        print(f"Successfully encoded '{input_file}' to '{output_file}'")
        print("The output file contains invisible characters!")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return False
    except Exception as e:
        print(f"Error encoding file: {e}")
        return False

def decode_invisible_file(input_file, output_file):
    """
    Decodes a file with invisible characters back to normal text.
    
    Args:
        input_file (str): Path to file with invisible characters.
        output_file (str): Path to output file for decoded text.
    """
    try:
        # Read invisible characters file
        with open(input_file, 'r', encoding='utf-8') as f:
            invisible_content = f.read()
        
        print(f"Invisible file size: {len(invisible_content)} characters")
        
        # Convert invisible characters to binary
        binary = invisible_to_binary(invisible_content)
        print(f"Recovered binary: {len(binary)} bits")
        
        # Convert binary to text
        decoded_text = binary_to_text(binary)
        print(f"Decoded text: {len(decoded_text)} characters")
        
        # Write decoded text to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decoded_text)
        
        print(f"Successfully decoded '{input_file}' to '{output_file}'")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return False
    except Exception as e:
        print(f"Error decoding file: {e}")
        return False

def display_invisible_chars_info():
    """Displays information about the invisible characters used."""
    print("\nInvisible Characters Used:")
    print(f"00 -> U+200B (Zero Width Space)")
    print(f"01 -> U+200D (Zero Width Joiner)")
    print(f"10 -> U+200C (Zero Width Non-Joiner)")
    print(f"11 -> U+2060 (Word Joiner)")
    print("\nThese characters are invisible when displayed but can be copied and pasted.")

def main():
    print("--- Invisible Character File Encoder/Decoder ---")
    print("Converts text files to invisible Unicode characters for steganography")
    
    while True:
        print("\nOptions:")
        print("1. Encode file to invisible characters")
        print("2. Decode invisible characters file")
        print("3. Show invisible characters info")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            input_file = input("Enter input file path: ").strip()
            output_file = input("Enter output file path: ").strip()
            
            if not input_file or not output_file:
                print("Error: Both file paths are required.")
                continue
            
            encode_file_to_invisible(input_file, output_file)
            
        elif choice == "2":
            input_file = input("Enter invisible characters file path: ").strip()
            output_file = input("Enter output file path for decoded text: ").strip()
            
            if not input_file or not output_file:
                print("Error: Both file paths are required.")
                continue
            
            decode_invisible_file(input_file, output_file)
            
        elif choice == "3":
            display_invisible_chars_info()
            
        elif choice == "4":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()