"""
Approach 8: Check if e1, e2 are actually d1, d2 (private exponents)
What if the problem gives us DECRYPTION exponents but we need to find
the corresponding ENCRYPTION exponents first?

Or: What if we misunderstood and need to compute pow(c1, 1, N) / pow(c1, e1_inv, N)?
"""
import re
from math import gcd

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

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

print("Approach 8: Wiener-like / Continued Fractions Analysis")
print("=" * 60)

# Check if e1/N or e2/N have interesting continued fraction expansions
# This is relevant for Wiener's attack

print("Checking ratios:")
print(f"e1 / N = {e1 / N}")
print(f"e2 / N = {e2 / N}")
print()

# If d is the private exponent and e*d ≡ 1 (mod phi(N))
# Then e*d = 1 + k*phi(N) for some k
# If we have e1 and e2, maybe they're related to phi(N)?

# Let's check if e1 + e2, e1 * e2, or other combinations reveal structure
print("Checking combinations of e1 and e2:")
print(f"e1 + e2 = {e1 + e2}")
print(f"e1 - e2 = {e1 - e2}")
print(f"abs(e1 - e2) = {abs(e1 - e2)}")
print()

# Check if the difference or sum is related to N
e_sum = e1 + e2
e_diff = abs(e1 - e2)

print(f"gcd(e1 + e2, N) = {gcd(e_sum, N)}")
print(f"gcd(e1 - e2, N) = {gcd(e_diff, N)}")
print()

# Maybe e1, e2 are close to sqrt(N)?
import math
sqrt_n = int(math.isqrt(N))
print(f"sqrt(N) ≈ {sqrt_n}")
print(f"e1 / sqrt(N) = {e1 / sqrt_n}")
print(f"e2 / sqrt(N) = {e2 / sqrt_n}")
print()

# New idea: what if the exponents encode p and q somehow?
# Or what if we need: m = c^(e mod phi(N)) ?

# Try: maybe e1 and e2 are inverses modulo a smaller number
for test_mod in [2**16, 2**32, 2**64, 2**128, 2**256]:
    e1_mod = e1 % test_mod
    e2_mod = e2 % test_mod
    prod = (e1_mod * e2_mod) % test_mod
    
    if prod == 1:
        print(f"!!! e1 * e2 ≡ 1 (mod 2^{test_mod.bit_length()-1})")
        print(f"e1 mod 2^{test_mod.bit_length()-1} = {e1_mod}")
        print(f"e2 mod 2^{test_mod.bit_length()-1} = {e2_mod}")
        break

print("\n" + "=" * 60)
print("Trying to find small values that might be the real exponents...")

# Maybe the REAL encryption exponent is small, and e1/e2 are decryption keys
# Try: if e_real is small, then e_real * e1 ≡ 1 (mod phi(N))
# We don't know phi(N), but phi(N) ≈ N for large primes

for e_test in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 65537]:
    # Check if e_test * e1 ≡ 1 (mod something close to N)
    prod = e_test * e1
    
    # If prod = 1 + k*phi(N), then k = (prod - 1) / phi(N) ≈ (prod - 1) / N
    k_approx = prod // N
    
    if k_approx > 0 and k_approx < 100:  # Small k is promising
        phi_candidate = (prod - 1) // k_approx
        
        # Check if this makes sense: phi(N) = N - p - q + 1, so phi < N
        if phi_candidate < N and phi_candidate > N // 2:
            print(f"\nTesting e = {e_test}:")
            print(f"  k ≈ {k_approx}")
            print(f"  phi(N) ≈ {phi_candidate}")
            
            # Try decrypting
            m1_test = pow(c1, e1, N)
            m2_test = pow(c2, e2, N)
            
            # Solve system
            p_test = 3 * m2_test - 7 * m1_test
            q_test = 5 * m1_test - 2 * m2_test
            
            if p_test * q_test == N:
                print(f"  SUCCESS!")
                print(f"  p = {p_test}")
                print(f"  q = {q_test}")
                break
