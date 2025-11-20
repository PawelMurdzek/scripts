from pwn import *
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import inverse

r = remote('socket.cryptohack.org', 13380)

# Pobieramy p, g oraz A
line = r.recvline().decode('utf-8')
print(line)
line = line.split("Alice: ")[1]
json_Alice = json.loads(line)
p_hex = json_Alice['p']
g_hex = json_Alice['g']
A_hex = json_Alice['A']
p = int(p_hex,16)
g = int(g_hex,16)
A = int(A_hex,16)

# Pobieramy B
line = r.recvline().decode('utf-8')
print(line)
line = line.split("Bob: ")[1]
json_Bob = json.loads(line)
B_hex = json_Bob['B']
B = int(B_hex,16)

# Pobieramy wiadomość i wektor
line = r.recvline().decode('utf-8')
print(line)
line = line.split("Alice: ")[1]
json_Alice2 = json.loads(line)
print(line)
iv = json_Alice2["iv"]
encrypted = json_Alice2["encrypted"]
# iv = bytes.fromhex(iv_hex)
# encrypted = bytes.fromhex(encrypted_hex)

a = A*inverse(g,p)%p
key = B*a%p

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

print(decrypt_flag(key, iv, encrypted))