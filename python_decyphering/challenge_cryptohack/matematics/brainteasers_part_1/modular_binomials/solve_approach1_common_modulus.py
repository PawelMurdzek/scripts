"""
Approach 1: Common Modulus Attack with Bezout's Identity
If gcd(e1, e2) = 1, we can compute: c1^a * c2^b = m1^(a*e1) * m2^(b*e2) mod N
where a*e1 + b*e2 = 1
"""
import re

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

def mod_inverse(a, m):
    """Compute modular inverse of a mod m"""
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

print("Approach 1: Common Modulus Attack")
print("=" * 60)

# Find gcd and Bezout coefficients
g, a, b = extended_gcd(e1, e2)
print(f"gcd(e1, e2) = {g}")

if g == 1:
    print(f"Found: {a}*e1 + {b}*e2 = 1")
    
    # Problem: We have TWO different messages m1 and m2
    # Standard common modulus attack won't work directly
    # We need m1 and m2 to recover p and q
    
    # Let's try computing combinations anyway
    if b < 0:
        # Need to invert c2
        c2_inv = mod_inverse(c2, N)
        if c2_inv:
            result = (pow(c1, a, N) * pow(c2_inv, -b, N)) % N
            print(f"c1^{a} * c2^{b} mod N = {result}")
    else:
        result = (pow(c1, a, N) * pow(c2, b, N)) % N
        print(f"c1^{a} * c2^{b} mod N = {result}")
    
    print("\nNote: This gives us a combination of m1 and m2, not the individual messages.")
    print("We need both m1 AND m2 to solve for p and q.")

print("\nConclusion: Standard common modulus attack insufficient for this problem.")
