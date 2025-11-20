import numpy as np
#Cocalc.com

P = 2
N = 50
E = 31337

def bits2bytes(bits):
    byte_array = []
    for i in range(0, len(bits), 8):
        byte_array.append(int(bits[i:i + 8], 2))
    return bytes(byte_array)

def matrix2bytes(matrix):
    bit_sequence = []
    for col_index in range(N):
        bit_sequence.extend([str(matrix[row][col_index]) for row in range(N)])
    return bits2bytes("".join(bit_sequence)[:272]) 

def load_matrix(file):
    data = open(file, 'r').read().strip()
    rows = [list(map(int, row)) for row in data.splitlines()]
    return np.array(rows, dtype=int)

def matrix_mult_gf2(A, B):
    """Matrix multiplication in GF(2)"""
    result = np.dot(A, B) % 2
    return result

def matrix_power_gf2(matrix, exp):
    """Compute matrix^exp in GF(2)"""
    if exp == 0:
        return np.eye(len(matrix), dtype=int)
    if exp == 1:
        return matrix.copy()
    
    result = np.eye(len(matrix), dtype=int)
    base = matrix.copy()
    
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mult_gf2(result, base)
        base = matrix_mult_gf2(base, base)
        exp //= 2
    
    return result

def multiplicative_order_gf2(matrix, max_order=2**25):
    """Find the multiplicative order of a matrix in GF(2) using baby-step giant-step approach"""
    identity = np.eye(len(matrix), dtype=int)
    
    # Try powers of 2 and common divisors first
    for exp in [2**i for i in range(1, 26)]:
        if np.array_equal(matrix_power_gf2(matrix, exp), identity):
            # Found a candidate, now find the actual order
            for divisor in range(1, min(1000, exp)):
                if exp % divisor == 0:
                    test_exp = exp // divisor
                    if np.array_equal(matrix_power_gf2(matrix, test_exp), identity):
                        exp = test_exp
            return exp
    
    # Fallback to iterative search with limited range
    current = matrix.copy()
    for order in range(1, min(max_order, 10**6)):
        if np.array_equal(current, identity):
            return order
        current = matrix_mult_gf2(current, matrix)
    
    raise ValueError("Order too large or matrix not invertible")

matrix = load_matrix("flag.enc")
print("Finding multiplicative order...")
order = multiplicative_order_gf2(matrix)
print(f"Multiplicative order: {order}")

#C = M^E => M = C^(1/E % k)
# Obliczam odwrotnośc macierzy E, z równania: E*x ≡ 1 %k więc x = E^-1% k, gdzie k to rząd multiplikatywny macierzy
dec_exponent = pow(E, -1, order)
print(f"Decryption exponent: {dec_exponent}")
print("Computing decryption matrix...")
dec_matrix = matrix_power_gf2(matrix, dec_exponent)

flag = matrix2bytes(dec_matrix).decode('utf-8')
print(flag)
