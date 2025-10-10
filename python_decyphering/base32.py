import base64

def base32_decode(encoded_string):
    """
    Decodes a Base32 encoded string.

    Args:
        encoded_string (str): The Base32 string to decode.

    Returns:
        str: The decoded string, or an error message if decoding fails.
    """
    try:
        # The encoded string must be bytes
        encoded_bytes = encoded_string.encode('ascii')
        
        # Decode the Base32 bytes
        decoded_bytes = base64.b32decode(encoded_bytes)
        
        # Decode the result back to a string
        decoded_string = decoded_bytes.decode('utf-8')
        
        return decoded_string
    except (base64.binascii.Error, UnicodeDecodeError) as e:
        return f"An error occurred: {e}. Make sure the input is valid Base32."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    print("--- Base32 Decoder ---")
    encoded_message = input("Enter the Base32 encoded message: ")
    
    decoded_message = base32_decode(encoded_message)
    
    print("\nDecoded message:")
    print(decoded_message)
