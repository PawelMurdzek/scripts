import requests

BASE_URL = "http://aes.cryptohack.org/lazy_cbc"
BLOCKSIZE = 32

def split_blocks(ctxt, blocksize=BLOCKSIZE):
    if len(ctxt) % blocksize != 0:
        raise Exception("!")
    else:
        number_of_blocks = len(ctxt) // blocksize
        return [ctxt[i*blocksize:(i+1)*blocksize] for i in range (number_of_blocks)]

def string_to_hex(txt):
    return txt.encode("utf-8").hex()

def hex_to_ascii(hex):
    bytes_object = bytes.fromhex(hex)
    return bytes_object.decode("ASCII")

def hex_xor(s1, s2):
    a = bytes.fromhex(s1)
    b = bytes.fromhex(s2)
    result = bytes([b1 ^ b2 for b1, b2 in zip(a,b)])
    return result.hex()

def encrypt(plaintext):
    encrypt_request = requests.get(f"{BASE_URL}/encrypt/{plaintext}/")
    return encrypt_request.json()["ciphertext"]

def get_flag(key):
    get_flag_request = requests.get(f"{BASE_URL}/get_flag/{key}/")
    return get_flag_request.json()["plaintext"]

def decrypt(ciphertext):
    decrypt_request = requests.get(f"{BASE_URL}/receive/{ciphertext}/")
    result = decrypt_request.json()

    if result["error"]:
        # get rid of "Invalid plaintext: "
        return result["error"][19:]
    else:
        return result["success"]

plaintext = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
plaintext_hex = string_to_hex(plaintext)
plaintext_blocks = split_blocks(plaintext_hex)

ciphertext = encrypt(plaintext_hex)
ciphertext_blocks = split_blocks(ciphertext)

# D - output from AES before the XOR with ciphertext from previous block
D = hex_xor(plaintext_blocks[1], ciphertext_blocks[0])

# swap C1 with C2 and repeat. D from above will be the same for the first block
ctx = ciphertext_blocks[1] + ciphertext_blocks[0]
plain = decrypt(ctx)
plain_blocks = split_blocks(plain)
# D is known and so new plaintext is, even unprintable.
IV = hex_xor(D, plain_blocks[0])

# As we have IV, we have the key because both are the same.
FLAG_hex = get_flag(IV)
FLAG = hex_to_ascii(FLAG_hex)
print(f"FLAG: {FLAG}")