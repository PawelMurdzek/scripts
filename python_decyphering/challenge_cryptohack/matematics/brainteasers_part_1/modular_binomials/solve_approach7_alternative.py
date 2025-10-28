"""
Approach 7: Inverse exponent hypothesis
What if e1 and e2 are MODULAR inverses of small values modulo some number?
Or what if the problem setup is different than we think?

Let's check: what if c1 and c2 are NOT ciphertexts but something else?
"""
import re
from math import gcd

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

print("Approach 7: Alternative Interpretations")
print("=" * 60)

# Check relationships between values
print("Checking GCDs between values:")
print(f"gcd(e1, N) = {gcd(e1, N)}")
print(f"gcd(e2, N) = {gcd(e2, N)}")
print(f"gcd(c1, N) = {gcd(c1, N)}")
print(f"gcd(c2, N) = {gcd(c2, N)}")
print(f"gcd(e1, e2) = {gcd(e1, e2)}")

# If any gcd is not 1, we might have a factor!
if gcd(c1, N) > 1 and gcd(c1, N) < N:
    print(f"\n!!! Found factor from gcd(c1, N) = {gcd(c1, N)}")
    p = gcd(c1, N)
    q = N // p
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"Verification: p*q == N: {p*q == N}")

if gcd(c2, N) > 1 and gcd(c2, N) < N:
    print(f"\n!!! Found factor from gcd(c2, N) = {gcd(c2, N)}")
    p = gcd(c2, N)
    q = N // p
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"Verification: p*q == N: {p*q == N}")

print("\n" + "=" * 60)
print("Checking if c1, c2 are already related to p, q directly:")
print()

# What if c1 = m1 and c2 = m2 directly? (e1, e2 are red herrings)
print("Hypothesis: c1 and c2 ARE the messages m1 and m2")
m1 = c1
m2 = c2
p = 3 * m2 - 7 * m1
q = 5 * m1 - 2 * m2
print(f"If m1 = c1, m2 = c2:")
print(f"p * q mod N = {(p * q) % N}")
print(f"Match: {(p * q) % N == 0}")

print("\n" + "=" * 60)
print("Checking if e1, e2 might be factoring hints:")
print(f"e1 mod 1000000 = {e1 % 1000000}")
print(f"e2 mod 1000000 = {e2 % 1000000}")
print(f"e1 // e2 = {e1 // e2}")
print(f"e2 // e1 = {e2 // e1}")

# Check if e1 or e2 divides something useful
print(f"\nN % e1 = {N % e1}")
print(f"N % e2 = {N % e2}")
