"""
Convert Integer to Message

This script demonstrates how to convert a large integer back into a readable message using the PyCryptodome library.
"""
from Crypto.Util.number import long_to_bytes

def integer_to_message(integer_value):
    """
    Convert a large integer into a readable message.

    Args:
        integer_value (int): The integer to convert.

    Returns:
        str: The decoded message.
    """
    try:
        # Convert the integer to bytes
        message_bytes = long_to_bytes(integer_value)
        # Decode the bytes to a string
        return message_bytes.decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Example integer
    integer_value = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
    print("Integer:", integer_value)
    message = integer_to_message(integer_value)
    print("Decoded Message:", message)