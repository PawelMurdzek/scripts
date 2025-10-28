"""
Approach 10: Check if e1*e2 reveals phi(N) or if there's a multiplicative relationship

Key insight: For RSA, if we have e*d ≡ 1 (mod phi(N)), then e*d = 1 + k*phi(N)
If e1 and e2 are BOTH related to phi(N), maybe their product or sum gives us info.
"""
import re
from math import gcd, isqrt

# Parse data
values = {}
with open('data.txt', 'r') as f:
    content = f.read()
matches = re.findall(r'(\w+)\s*=\s*(\d+)', content)
for key, value in matches:
    values[key] = int(value)

N = values['N']
e1 = values['e1']
e2 = values['e2']
c1 = values['c1']
c2 = values['c2']

print("Approach 10: Extracting phi(N) from exponent relationships")
print("=" * 60)

# If e1 * something = 1 + k * phi(N), we might extract phi
# Also: phi(N) = N - p - q + 1
# So if we can find phi(N), we can find p + q, and with N = p*q we can solve

# Try: maybe e1 * e2 ≡ 1 (mod phi(N))
# Then e1 * e2 = 1 + k * phi(N)
product = e1 * e2
print(f"e1 * e2 = {product}")
print(f"(e1 * e2) bit length = {product.bit_length()}")
print()

# Try different k values to see if we can extract phi(N)
print("Testing if e1 * e2 = 1 + k * phi(N) for small k...")
for k in range(1, 1000):
    phi_candidate = (product - 1) // k
    
    if phi_candidate >= N:
        continue
    if phi_candidate < N // 2:
        break
        
    # phi(N) = N - p - q + 1
    # So: p + q = N - phi(N) + 1
    p_plus_q = N - phi_candidate + 1
    
    # We have: p + q and p * q = N
    # Solve: x^2 - (p+q)*x + N = 0
    # x = ((p+q) ± sqrt((p+q)^2 - 4N)) / 2
    
    discriminant = p_plus_q * p_plus_q - 4 * N
    
    if discriminant >= 0:
        sqrt_disc = isqrt(discriminant)
        
        # Check if perfect square
        if sqrt_disc * sqrt_disc == discriminant:
            p = (p_plus_q + sqrt_disc) // 2
            q = (p_plus_q - sqrt_disc) // 2
            
            if p * q == N:
                print(f"\n!!! FOUND IT with k = {k} !!!")
                print(f"phi(N) = {phi_candidate}")
                print(f"p + q = {p_plus_q}")
                print(f"p = {p}")
                print(f"q = {q}")
                print(f"Verification: p * q = {p * q}")
                print(f"N = {N}")
                print(f"Match: {p * q == N}")
                print("\n" + "=" * 60)
                print("SOLUTION FOUND!")
                print("=" * 60)
                exit(0)
    
    if k % 100 == 0:
        print(f"  Tested k up to {k}...")

print("\nNo solution found with small k values.")

# Try another approach: maybe e1 + e2 or e1 - e2 is related to phi
print("\n" + "=" * 60)
print("Testing if e1 ± e2 reveals phi(N)...")

for operation, value in [("e1 + e2", e1 + e2), ("abs(e1 - e2)", abs(e1 - e2))]:
    print(f"\nTesting {operation} = {value}")
    
    for k in range(1, 1000):
        phi_candidate = value // k
        
        if phi_candidate >= N or phi_candidate < N // 2:
            continue
            
        p_plus_q = N - phi_candidate + 1
        discriminant = p_plus_q * p_plus_q - 4 * N
        
        if discriminant >= 0:
            sqrt_disc = isqrt(discriminant)
            
            if sqrt_disc * sqrt_disc == discriminant:
                p = (p_plus_q + sqrt_disc) // 2
                q = (p_plus_q - sqrt_disc) // 2
                
                if p * q == N:
                    print(f"\n!!! FOUND IT !!!")
                    print(f"k = {k}")
                    print(f"phi(N) = {phi_candidate}")
                    print(f"p = {p}")
                    print(f"q = {q}")
                    exit(0)
