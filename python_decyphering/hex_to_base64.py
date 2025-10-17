"""
Hexadecimal to Base64 Converter

This script converts a hexadecimal string to its Base64 representation.
"""

import base64


def hex_to_base64(hex_string):
    """
    Convert a hexadecimal string to Base64.

    Args:
        hex_string (str): Hexadecimal string to convert.

    Returns:
        str: Base64 encoded string.
    """
    try:
        # Convert hex string to bytes
        byte_data = bytes.fromhex(hex_string)
        # Encode bytes to Base64
        base64_data = base64.b64encode(byte_data).decode("utf-8")
        return base64_data
    except ValueError as e:
        return f"Error: Invalid hexadecimal string. {e}"


if __name__ == "__main__":
    # Example hexadecimal string
    hex_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
    print("Hexadecimal String:", hex_string)
    base64_result = hex_to_base64(hex_string)
    print("Base64 Result:", base64_result)