from pwn import remote
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import inverse

def decrypt_flag(shared_secret, iv, ciphertext):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext))
    return unpad(plaintext, 16).decode('ascii')

r = remote('socket.cryptohack.org', 13380)

# Get p, g, A from Alice
data = json.loads(r.recvline().decode().split("Alice: ")[1])
p = int(data['p'], 16)
g = int(data['g'], 16)
A = int(data['A'], 16)

# Get B from Bob
B = int(json.loads(r.recvline().decode().split("Bob: ")[1])['B'], 16)

# Get iv and encrypted message from Alice
data = json.loads(r.recvline().decode().split("Alice: ")[1])
iv = data["iv"]
encrypted = data["encrypted"]

# Calculate shared secret
a = A * inverse(g, p) % p
shared_secret = B * a % p

print(decrypt_flag(shared_secret, iv, encrypted))