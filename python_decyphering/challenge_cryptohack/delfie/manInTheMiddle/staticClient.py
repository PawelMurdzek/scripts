from pwn import *
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

r = remote('socket.cryptohack.org', 13373)

def json_recv():
    line = r.recvline()
    print(f"Received: {line.decode()}")
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh)
    print(f"Sending: {request}")
    r.sendline(request.encode())

# Pobieramy paramtrey p, g oraz A
line = r.recvline().decode('utf-8')
print(line)
line = line.split("Alice: ")[1]

json_Alice = json.loads(line)
p_hex = json_Alice['p']
g_hex = json_Alice['g']
A_hex = json_Alice['A']

line = r.recvline().decode('utf-8')
print(line)

# Pobieramy B
json_Bob = json.loads(line.split("Bob: ")[1])
B_hex = json_Bob['B']

# Pobieramy wektor i flage
line = r.recvline().decode('utf-8')
json_Alice2 = json.loads(line.split("Alice: ")[1])
iv = json_Alice2["iv"]
encrypted_hex = json_Alice2["encrypted"]

# Wysyłamy zmanipulowane parametry 
json_send({"p": p_hex, "g": A_hex, "A": g_hex})

# Odpowiada secret
line = r.recvline().decode('utf-8')
print(line)
json_Bob2 = json.loads(line.split("you: ")[1])
secret = int(json_Bob2["B"],16)

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

print(decrypt_flag(secret, iv, encrypted_hex))