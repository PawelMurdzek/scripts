"""
Approach 9: Direct computation assuming textbook RSA with e1, e2 as private keys
Key insight: If e1 and e2 are DECRYPTION exponents, then:
- m1 = pow(c1, e1, N)
- m2 = pow(c2, e2, N)

But we tried this in approach 3 and it didn't work.
However, maybe we need to check if the SIGNATURES match, not the products.

Or: What if e1, e2 need to be reduced modulo lambda(N) first?
"""
import re

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

print("Approach 9: Systematic checking of all possibilities")
print("=" * 60)

test_cases = [
    ("c1^e1 mod N, c2^e2 mod N", lambda: (pow(c1, e1, N), pow(c2, e2, N))),
    ("c1^e2 mod N, c2^e1 mod N", lambda: (pow(c1, e2, N), pow(c2, e1, N))),
    ("c1^(1/e1) mod N, c2^(1/e2) mod N - needs inverse", None),  # Skip, too complex
    ("c1, c2 directly", lambda: (c1, c2)),
    ("e1, e2 as messages", lambda: (e1, e2)),
]

for desc, func in test_cases:
    if func is None:
        continue
        
    print(f"\nTesting: {desc}")
    try:
        m1, m2 = func()
        
        # Solve system: m1 = 2p + 3q, m2 = 5p + 7q
        p = 3 * m2 - 7 * m1
        q = 5 * m1 - 2 * m2
        
        # Check
        if p > 0 and q > 0 and p * q == N:
            print(f"  ✓ SUCCESS!")
            print(f"  m1 = {m1}")
            print(f"  m2 = {m2}")
            print(f"  p = {p}")
            print(f"  q = {q}")
            print(f"  Verification: p * q == N: {p * q == N}")
            print("\n" + "=" * 60)
            print("SOLUTION FOUND!")
            print("=" * 60)
            exit(0)
        else:
            result_prod = p * q if p > 0 and q > 0 else None
            match_str = "Match" if result_prod == N else "No match"
            print(f"  ✗ {match_str}")
            if p > 0 and q > 0:
                print(f"    p*q = {result_prod}")
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "=" * 60)
print("No solution found in systematic check.")
