import base64

def base64_encode(message):
    """
    Encodes a string to Base64 format.

    Args:
        message (str): The string to encode.

    Returns:
        str: The Base64 encoded string, or an error message if encoding fails.
    """
    try:
        # Convert the string to bytes using UTF-8 encoding
        message_bytes = message.encode('utf-8')
        
        # Encode the bytes to Base64
        encoded_bytes = base64.b64encode(message_bytes)
        
        # Convert back to string for display
        encoded_string = encoded_bytes.decode('ascii')
        
        return encoded_string
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print("--- Base64 Encoder ---")
    plain_message = input("Enter the message to encode: ")
    
    encoded_message = base64_encode(plain_message)
    
    print("\nEncoded message:")
    print(encoded_message)