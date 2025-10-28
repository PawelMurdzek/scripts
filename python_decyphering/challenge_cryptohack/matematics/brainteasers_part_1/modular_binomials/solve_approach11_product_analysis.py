"""
Approach 11: e1 * e2 relationship - CRITICAL INSIGHT
e1 * e2 has 1024 bits, N has 2048 bits
This means e1 * e2 ≈ sqrt(N) * some_constant

Maybe: e1 = p + something, e2 = q + something?
Or: e1 * e2 is related to (p-1)(q-1)?
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

print("Approach 11: Analyzing the e1*e2 ≈ sqrt(N) relationship")
print("=" * 60)

product = e1 * e2
sqrt_N = isqrt(N)

print(f"e1 * e2 = {product}")
print(f"sqrt(N) = {sqrt_N}")
print(f"Ratio: (e1*e2) / sqrt(N) = {product / sqrt_N}")
print()

# Check if e1 * e2 is close to any interesting value
ratios_to_check = [
    ("sqrt(N)", sqrt_N),
    ("sqrt(N)/2", sqrt_N // 2),
    ("sqrt(N)/4", sqrt_N // 4),
    ("N/4", N // 4),
    ("phi(N) assuming p≈q≈sqrt(N)", sqrt_N * sqrt_N - 2 * sqrt_N + 1),
]

for name, value in ratios_to_check:
    diff = abs(product - value)
    print(f"|(e1*e2) - {name}| = {diff}")
    print(f"  Relative difference: {diff / value if value > 0 else 'inf'}")

print("\n" + "=" * 60)
print("KEY INSIGHT: Maybe e1 and e2 ARE p and q (or related to them)!")
print()

# Test if e1, e2 are close to p, q
print("Testing: What if e1 and e2 are the primes themselves?")
if e1 * e2 == N:
    print("  e1 * e2 == N: YES!")
    print(f"  p = {e1}")
    print(f"  q = {e2}")
else:
    print(f"  e1 * e2 = {e1 * e2}")
    print(f"  N       = {N}")
    print("  Not equal.")

# Test if e1, e2 are ALMOST p, q (off by small amount)
print("\nTesting: e1 ± small_offset might be p or q...")
for offset in range(-100, 101):
    p_test = e1 + offset
    if N % p_test == 0:
        q_test = N // p_test
        print(f"\n!!! FOUND: N = (e1 + {offset}) * q !!!")
        print(f"p = e1 + {offset} = {p_test}")
        print(f"q = {q_test}")
        print(f"Verification: p * q = {p_test * q_test}")
        print(f"N = {N}")
        print(f"Match: {p_test * q_test == N}")
        exit(0)

for offset in range(-100, 101):
    q_test = e2 + offset
    if N % q_test == 0:
        p_test = N // q_test
        print(f"\n!!! FOUND: N = p * (e2 + {offset}) !!!")
        print(f"p = {p_test}")
        print(f"q = e2 + {offset} = {q_test}")
        print(f"Verification: p * q = {p_test * q_test}")
        exit(0)

print("\n" + "=" * 60)
print("Testing: Maybe e1, e2 encode p, q via linear combinations...")

# What if: e1 = a*p + b, e2 = c*q + d for small a, b, c, d?
# Or: what if e1 and e2 are themselves linear combinations of p and q?

# Try: e1 = 2p + 3q (same as m1!)
print("\nHypothesis: e1 and e2 might BE the messages m1 and m2!")
m1 = e1
m2 = e2

p = 3 * m2 - 7 * m1
q = 5 * m1 - 2 * m2

print(f"If m1 = e1, m2 = e2:")
print(f"p = {p}")
print(f"q = {q}")
print(f"p * q = {p * q}")
print(f"N = {N}")
print(f"Match: {p * q == N}")

if p * q == N:
    print("\n" + "=" * 60)
    print("SUCCESS! The exponents ARE the messages!")
    print("=" * 60)
    exit(0)
