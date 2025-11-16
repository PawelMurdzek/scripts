from random import randint

a = 288260533169915
p = 1007621497415251

FLAG = b'crypto{????????????????????}'


def encrypt_flag(flag):
    ciphertext = []
    plaintext = ''.join([bin(i)[2:].zfill(8) for i in flag])
    for b in plaintext:
        e = randint(1, p)
        n = pow(a, e, p)
        if b == '1':
            ciphertext.append(n)
        else:
            n = -n % p
            ciphertext.append(n)
    return ciphertext


# Legendre symbol function
def legendre(a, p):
    """Compute the Legendre symbol (a/p)"""
    return pow(a, (p - 1) // 2, p)


def decrypt_flag(ciphertext, p):
    """Decrypt the ciphertext using Legendre symbol"""
    binary_string = ''
    for n in ciphertext:
        # Check if n is a quadratic residue using Legendre symbol
        leg = legendre(n, p)
        if leg == 1:
            # Quadratic residue -> bit is '1'
            binary_string += '1'
        else:
            # Not a quadratic residue -> bit is '0'
            binary_string += '0'
    
    # Convert binary string to bytes
    flag = ''
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        flag += chr(int(byte, 2))
    
    return flag


# Read ciphertext from output.txt
with open('output.txt', 'r') as f:
    content = f.read().strip()
    ciphertext = eval(content)

decrypted_flag = decrypt_flag(ciphertext, p)
print(f"Decrypted flag: {decrypted_flag}")

