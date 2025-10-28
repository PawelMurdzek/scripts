"""
Approach 2: Check if N can be factored using various methods
- Trial division with small primes
- Fermat's factorization (if p and q are close)
- Pollard's rho
"""
import re
import math

def trial_division(n, limit=10**6):
    """Try to find small factors"""
    if n % 2 == 0:
        return 2
    for i in range(3, min(limit, int(math.sqrt(n)) + 1), 2):
        if n % i == 0:
            return i
    return None

def fermat_factorization(n, max_iterations=10**6):
    """Fermat's factorization method - works well if factors are close"""
    a = int(math.isqrt(n)) + 1
    b2 = a*a - n
    
    for _ in range(max_iterations):
        b = int(math.isqrt(b2))
        if b*b == b2:
            p = a - b
            q = a + b
            if p * q == n:
                return p, q
        a += 1
        b2 = a*a - n
    
    return None, None

def pollard_rho(n, max_iterations=10**6):
    """Pollard's rho algorithm"""
    if n % 2 == 0:
        return 2
    
    x = 2
    y = 2
    d = 1
    
    def f(x):
        return (x*x + 1) % n
    
    iterations = 0
    while d == 1 and iterations < max_iterations:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
        iterations += 1
        
        if iterations % 100000 == 0:
            print(f"  Pollard's rho: {iterations} iterations...")
    
    if d != n:
        return d
    return None

# Parse data
values = {}
with open('data.txt', 'r') as f:
    content = f.read()
matches = re.findall(r'(\w+)\s*=\s*(\d+)', content)
for key, value in matches:
    values[key] = int(value)

N = values['N']

print("Approach 2: Factorization Attempts")
print("=" * 60)
print(f"N has {N.bit_length()} bits ({len(str(N))} digits)")

# Try trial division
print("\n1. Trial division with small primes (up to 10^6)...")
factor = trial_division(N)
if factor:
    print(f"   Found factor: {factor}")
    p = factor
    q = N // p
    print(f"   p = {p}")
    print(f"   q = {q}")
    print(f"   Verification: p*q == N: {p*q == N}")
else:
    print("   No small factors found.")

# Try Fermat's factorization
print("\n2. Fermat's factorization (checking if p and q are close)...")
p, q = fermat_factorization(N, max_iterations=10**6)
if p and q:
    print(f"   Found factors!")
    print(f"   p = {p}")
    print(f"   q = {q}")
    print(f"   Verification: p*q == N: {p*q == N}")
else:
    print("   Fermat's method did not find factors in 10^6 iterations.")

# Try Pollard's rho
print("\n3. Pollard's rho algorithm...")
print("   (This may take a while for large numbers...)")
factor = pollard_rho(N, max_iterations=10**5)
if factor and factor != N:
    print(f"   Found factor: {factor}")
    p = factor
    q = N // p
    print(f"   p = {p}")
    print(f"   q = {q}")
    print(f"   Verification: p*q == N: {p*q == N}")
else:
    print("   Pollard's rho did not find factors.")

print("\nConclusion: If no factors found, N is likely a strong RSA modulus.")
