import base64
import binascii

def base64_decode(encoded_string):
    """
    Decodes a Base64 encoded string.

    Args:
        encoded_string (str): The Base64 string to decode.

    Returns:
        str: The decoded string, or an error message if decoding fails.
    """
    try:
        # The encoded string must be bytes, so we encode it to ASCII
        encoded_bytes = encoded_string.encode('ascii')
        
        # Decode the Base64 bytes
        decoded_bytes = base64.b64decode(encoded_bytes)
        
        # Decode the result back to a string (using UTF-8 which is common)
        decoded_string = decoded_bytes.decode('utf-8')
        
        return decoded_string
    except (binascii.Error, UnicodeDecodeError) as e:
        return f"An error occurred: {e}. Make sure the input is valid Base64."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    print("--- Base64 Decoder ---")
    encoded_message = input("Enter the Base64 encoded message: ")
    
    decoded_message = base64_decode(encoded_message)
    
    print("\nDecoded message:")
    print(decoded_message)