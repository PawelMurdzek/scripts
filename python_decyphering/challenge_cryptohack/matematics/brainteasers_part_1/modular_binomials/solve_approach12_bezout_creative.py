"""
Approach 12: Using Bezout's identity to create useful combinations
Since gcd(e1, e2) = 1, we have: a*e1 + b*e2 = 1

Key insight: We can use this to create combinations that might help us extract m1 and m2

If c1 = m1^e1 mod N and c2 = m2^e2 mod N, then:
c1^a * c2^b = m1^(a*e1) * m2^(b*e2) = m1^(a*e1) * m2^(1 - a*e1) mod N

But this still mixes m1 and m2...

WAIT! What if the relationship is different?
What if c1, c2 are not RSA ciphertexts but represent something else entirely?
"""
import re
from math import gcd

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
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

print("Approach 12: Creative use of Bezout coefficients")
print("=" * 60)

g, a, b = extended_gcd(e1, e2)
print(f"Extended GCD: {a} * e1 + {b} * e2 = {g}")
print(f"a = {a}")
print(f"b = {b}")
print()

# Since a*e1 + b*e2 = 1, we know that:
# If we have inverses, we might be able to extract something

# Create combinations
print("Computing various combinations using Bezout coefficients...")
print()

# Combination 1: c1^a * c2^b mod N
if b < 0:
    c2_inv = mod_inverse(c2, N)
    if c2_inv:
        combo1 = (pow(c1, a, N) * pow(c2_inv, -b, N)) % N
        print(f"c1^a * c2^(-b) mod N = {combo1}")
        print(f"Bit length: {combo1.bit_length()}")
else:
    combo1 = (pow(c1, a, N) * pow(c2, b, N)) % N
    print(f"c1^a * c2^b mod N = {combo1}")
    print(f"Bit length: {combo1.bit_length()}")

# Try using this as m1 or m2
print("\nTesting if this combination helps...")
candidates = [combo1]

# Also try other useful combinations based on the linear relationships
# We know: 7*m1 - 3*m2 = -p and 5*m1 - 2*m2 = q

# If we could compute m1^7 * m2^(-3), that would give us -p^(e1*7 - e2*3)
# But we need different exponents...

print("\n" + "=" * 60)
print("Trying to use linear algebra on exponents...")
print()

# We need to find x, y such that:
# x*e1 = 7 (mod something) and y*e2 = -3 (mod something)
# This is getting very complex...

# Try a different tactic: since we know the linear relationships between m1, m2
# and p, q, maybe we can express c1 and c2 in terms of p and q directly

print("KEY REALIZATION:")
print("m1 = 2p + 3q")
print("m2 = 5p + 7q")
print("c1 = (2p + 3q)^e1 mod N")
print("c2 = (5p + 7q)^e2 mod N")
print()
print("These are polynomial equations in p and q!")
print("With N = p*q, we have a system that might be solvable with resultants.")
print()
print("This requires SageMath or SymPy with polynomial operations...")

# Try one more thing: check if the exponents themselves encode information
print("\n" + "=" * 60)
print("Final check: Examining bit patterns in exponents...")
print(f"e1 in hex: {hex(e1)}")
print(f"e2 in hex: {hex(e2)}")

# Check if they encode ASCII or other patterns
e1_bytes = e1.to_bytes((e1.bit_length() + 7) // 8, 'big')
e2_bytes = e2.to_bytes((e2.bit_length() + 7) // 8, 'big')

print(f"\ne1 as bytes (first 32): {e1_bytes[:32]}")
print(f"e2 as bytes (first 32): {e2_bytes[:32]}")

# Check if bytes spell something
try:
    e1_str = e1_bytes.decode('ascii', errors='ignore')
    if any(c.isprintable() and c.isalpha() for c in e1_str):
        print(f"e1 contains text: {e1_str}")
except:
    pass

try:
    e2_str = e2_bytes.decode('ascii', errors='ignore')
    if any(c.isprintable() and c.isalpha() for c in e2_str):
        print(f"e2 contains text: {e2_str}")
except:
    pass

print("\n" + "=" * 60)
print("Pure Python approaches exhausted.")
print("This problem requires:")
print("1. SageMath for polynomial resultants/Groebner bases")
print("2. OR Copper smith's method for polynomial roots mod N")
print("3. OR a clever mathematical insight I'm missing")
