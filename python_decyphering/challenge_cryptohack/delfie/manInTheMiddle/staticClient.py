from pwn import remote
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_flag(shared_secret, iv, ciphertext):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    
    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext))
    return unpad(plaintext, 16).decode('ascii')

r = remote('socket.cryptohack.org', 13373)

# Get DH parameters from Alice
data = json.loads(r.recvline().decode().split("Alice: ")[1])
p_hex = data['p']
g_hex = data['g']
A_hex = data['A']

r.recvline()  # Bob's message

# Get iv and encrypted message
data = json.loads(r.recvline().decode().split("Alice: ")[1])
iv = data["iv"]
encrypted = data["encrypted"]

# Send manipulated parameters: swap g and A
# Bob will compute B = A^b mod p, and we can intercept it
r.sendline(json.dumps({"p": p_hex, "g": A_hex, "A": g_hex}).encode())

# Get B which is actually the shared secret
shared_secret = int(json.loads(r.recvline().decode().split("you: ")[1])["B"], 16)

print(decrypt_flag(shared_secret, iv, encrypted))