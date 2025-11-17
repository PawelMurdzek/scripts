import requests
from Crypto.Util.strxor import strxor

res = requests.get('https://aes.cryptohack.org/symmetry/encrypt_flag/').json()
ciphertext = bytes.fromhex(res['ciphertext'])

iv = ciphertext[:16]
encrypted_flag = ciphertext[16:]

plaintext = b'\x00' * len(encrypted_flag)
url = f"https://aes.cryptohack.org/symmetry/encrypt/{plaintext.hex()}/{iv.hex()}/"
res = requests.get(url).json()
cipher_keystream = bytes.fromhex(res['ciphertext'])

flag = strxor(cipher_keystream, encrypted_flag)
print(flag.decode())