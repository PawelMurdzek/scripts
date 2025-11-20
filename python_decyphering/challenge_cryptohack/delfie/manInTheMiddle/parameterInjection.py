from pwn import *
import json
from Crypto.Cipher import AES
import hashlib

r = remote('socket.cryptohack.org', 13371)
    
def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

line = r.recvline()
recv_json = json.loads(line.decode('utf-8')[24:])

# Odbieramy od serwera p, g oraz A (klucz publiczny)
p = recv_json['p']
g = recv_json['g']
A = recv_json['A']
g = int(g,16)
p = int(p,16)
A = int(A,16) 

# Wysyłamy do serwera wartości, ale nie poprawne dla A
json_send({"p": f"{hex(p)}", "g": f"{hex(g)}", "A": f"{hex(p)}"})

line = r.recvline()
recv_json_Bob = json.loads(line.decode()[35:])

# Odbieramy od serwera B, czyli klucz publiczny
B = recv_json_Bob["B"]
B = int(B,16)

# Wysyłamy B jako p
json_send({"B": f"{hex(p)}"})

line = r.recvline()
recv_json_Alice = json.loads(line.decode('utf-8')[39:])

# Odbieramy wektor i flagę 
iv = recv_json_Alice["iv"]
flag = recv_json_Alice["encrypted_flag"]

# Manipulowaliśmy A i B
secret = 0

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

print(decrypt_flag(secret, iv, flag))