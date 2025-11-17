"""
ECB-CBC Attack Script
Exploits a vulnerability where a server encrypts with CBC but decrypts with ECB mode.
"""

import requests

BASE_URL = "https://aes.cryptohack.org/ecbcbcwtf"
BLOCK_SIZE = 16


def get_encrypted_flag():
    """Fetch the encrypted flag from the server."""
    response = requests.get(f"{BASE_URL}/encrypt_flag/").json()
    ciphertext_hex = response["ciphertext"]
    return bytes.fromhex(ciphertext_hex)


def decrypt_with_ecb(ciphertext_hex):
    """Request ECB decryption from the server."""
    response = requests.get(f"{BASE_URL}/decrypt/{ciphertext_hex}/").json()
    plaintext_hex = response["plaintext"]
    return bytes.fromhex(plaintext_hex)


def split_into_blocks(data, block_size=BLOCK_SIZE):
    """Split data into blocks of specified size."""
    return [data[i:i + block_size] for i in range(0, len(data), block_size)]


def xor_blocks(block1, block2):
    """XOR two blocks byte by byte."""
    return bytes([b1 ^ b2 for b1, b2 in zip(block1, block2)])


def decrypt_cbc_locally(ciphertext_blocks, ecb_decrypted_blocks):
    """
    Decrypt CBC mode locally using ECB-decrypted blocks.
    
    CBC decryption: P_i = D(C_i) XOR C_(i-1)
    where D is the block cipher decryption (which we got via ECB).
    """
    plaintext = b""
    
    # Start from block 1 (skip IV which is block 0)
    for i in range(1, len(ciphertext_blocks)):
        decrypted_block = ecb_decrypted_blocks[i]
        previous_ciphertext = ciphertext_blocks[i - 1]
        plaintext_block = xor_blocks(decrypted_block, previous_ciphertext)
        plaintext += plaintext_block
    
    return plaintext


def main():
    """Main execution function."""
    print("[*] Fetching encrypted flag...")
    ciphertext = get_encrypted_flag()
    ciphertext_hex = ciphertext.hex()
    
    print("[*] Requesting ECB decryption...")
    ecb_decrypted = decrypt_with_ecb(ciphertext_hex)
    
    print("[*] Splitting into blocks...")
    ciphertext_blocks = split_into_blocks(ciphertext)
    ecb_decrypted_blocks = split_into_blocks(ecb_decrypted)
    
    print("[*] Performing local CBC decryption...")
    plaintext = decrypt_cbc_locally(ciphertext_blocks, ecb_decrypted_blocks)
    
    print("\n[+] Decrypted plaintext:", plaintext)
    print("[+] FLAG:", plaintext.decode(errors="ignore"))


if __name__ == "__main__":
    main()