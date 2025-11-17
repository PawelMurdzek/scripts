from Crypto.Cipher import AES
import hashlib

with open("C:/Users/nkoll/Desktop/words.txt", encoding='utf-8') as f:
    words = [w.strip() for w in f.readlines()]


ciphertext = 'c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66'


ciphertext = bytes.fromhex(ciphertext)
for k in words:
    key = hashlib.md5(k.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    if decrypted.startswith(b'crypto{'):
        print("plaintext", decrypted)