# KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
# KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
# KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
# FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf

from pwn import *

def xor_bytes(bytes1, bytes2):
    """
    XOR two byte arrays and return the result.

    Args:
        bytes1 (bytes): The first byte array.
        bytes2 (bytes): The second byte array.

    Returns:
        bytearray: The XORed result as a bytearray.
    """
    return bytearray(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))

# Given values
KEY1 = bytes.fromhex('a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313')
MASK1 = bytes.fromhex('37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e')
MASK2 = bytes.fromhex('c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1')
MASK3 = bytes.fromhex('04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf')

# Calculate keys
KEY2 = xor_bytes(KEY1, MASK1)
KEY3 = xor_bytes(KEY2, MASK2)

# Calculate FLAG
FLAG = xor_bytes(KEY1, xor_bytes(KEY2, xor_bytes(KEY3, MASK3)))

# Print results
print("KEY1:", KEY1.hex())
print("KEY2:", KEY2.hex())
print("KEY3:", KEY3.hex())
print("FLAG:", "".join(chr(b) for b in FLAG))