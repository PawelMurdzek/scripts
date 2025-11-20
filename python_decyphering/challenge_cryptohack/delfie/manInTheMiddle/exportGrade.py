from pwn import *
import json
from Crypto.Cipher import AES
import hashlib
from sympy.ntheory import discrete_log

r = remote('socket.cryptohack.org', 13379)

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

# Lista obsługiwanych parametrów
line = r.recvline().decode('utf-8')
print(line)
line = line.split("Alice: ")[1]
json_1 = json.loads(line)
supported = json_1["supported"]

# Wybieramy i wysyłamy ostatni
json_send({"supported":[f"{supported[-1]}"]})
line = r.recvline().decode('utf-8')
print(line)
json_send({"chosen":supported[-1]})

# Otrzymujemy parametry DH
line = r.recvline().decode('utf-8')
print(line)
line = line.split("Alice: ")[2]
json_2 = json.loads(line)
p_hex = json_2["p"]
g_hex = json_2["g"]
A_hex = json_2["A"]
p = int(p_hex,16)
g = int(g_hex,16)
A = int(A_hex,16)

# Wysyłamy p, g i A do serwera
json_send({"p":p_hex,"g":g_hex,"A":A_hex})
line = r.recvline().decode('utf-8')
print(line)

# Dostajemy B
line = line.split("Bob: ")[1]
json_3 = json.loads(line)
B = int(json_3["B"],16)

# Odsyłamy B do serwera
json_send({"B":f"{hex(B)}"})
line = r.recvline().decode('utf-8')
print(line)

# Dostajemy wektro i flage
line = line.split("Alice: ")[1]
json_4 = json.loads(line)
iv = json_4["iv"]
flag = json_4["encrypted_flag"]

# Obliczamy klucz prywatny a
a = discrete_log(p,A,g)

# Obliczamy wspólny sekret
secret = pow(B, a, p)

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
