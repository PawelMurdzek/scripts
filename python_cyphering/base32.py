import base64

def base32_encode(message):
    """
    Encodes a string to Base32 format.

    Args:
        message (str): The string to encode.

    Returns:
        str: The Base32 encoded string, or an error message if encoding fails.
    """
    try:
        # Convert the string to bytes
        message_bytes = message.encode('utf-8')
        
        # Encode the bytes to Base32
        encoded_bytes = base64.b32encode(message_bytes)
        
        # Convert back to string for display
        encoded_string = encoded_bytes.decode('ascii')
        
        return encoded_string
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print("--- Base32 Encoder ---")
    plain_message = input("Enter the message to encode: ")
    
    encoded_message = base32_encode(plain_message)
    
    print("\nEncoded message:")
    print(encoded_message)