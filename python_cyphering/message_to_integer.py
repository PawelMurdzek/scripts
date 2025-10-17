"""
Convert Message to Integer

This script demonstrates how to convert a readable message into a large integer using the PyCryptodome library.
"""
from Crypto.Util.number import bytes_to_long

def message_to_integer(message):
    """
    Convert a readable message into a large integer.

    Args:
        message (str): The message to convert.

    Returns:
        int: The converted integer.
    """
    try:
        # Encode the message to bytes
        message_bytes = message.encode('utf-8')
        # Convert bytes to a large integer
        return bytes_to_long(message_bytes)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Example message
    message = "HELLO"
    print("Message:", message)
    integer_value = message_to_integer(message)
    print("Integer Value:", integer_value)