"""
Approach 3: Check if exponents are actually inverses (decryption exponents)
Maybe e1 and e2 are actually private exponents that decrypt the ciphertexts
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

print("Approach 3: Testing if e1, e2 are decryption keys")
print("=" * 60)

# Try: maybe we need to decrypt with these exponents
print("Testing: m1 = c1^e1 mod N")
m1_candidate = pow(c1, e1, N)
print(f"m1_candidate = {m1_candidate}")
print(f"m1_candidate (hex) = {hex(m1_candidate)}")
print(f"m1_candidate bit length = {m1_candidate.bit_length()}")

print("\nTesting: m2 = c2^e2 mod N")
m2_candidate = pow(c2, e2, N)
print(f"m2_candidate = {m2_candidate}")
print(f"m2_candidate (hex) = {hex(m2_candidate)}")
print(f"m2_candidate bit length = {m2_candidate.bit_length()}")

# Now try to solve for p and q
print("\n" + "=" * 60)
print("Attempting to solve system of equations:")
print("m1 = 2*p + 3*q")
print("m2 = 5*p + 7*q")
print()

m1 = m1_candidate
m2 = m2_candidate

# Solving:
# m1 = 2p + 3q
# m2 = 5p + 7q
# 
# Multiply first by 7: 7m1 = 14p + 21q
# Multiply second by 3: 3m2 = 15p + 21q
# Subtract: 7m1 - 3m2 = -p
# So: p = 3m2 - 7m1

# Multiply first by 5: 5m1 = 10p + 15q
# Multiply second by 2: 2m2 = 10p + 14q
# Subtract: 5m1 - 2m2 = q

p = 3 * m2 - 7 * m1
q = 5 * m1 - 2 * m2

print(f"p = {p}")
print(f"q = {q}")
print(f"\nVerification: p * q = {p * q}")
print(f"N =                  {N}")
print(f"Match: {p * q == N}")

if p * q == N:
    print("\n" + "=" * 60)
    print("SUCCESS! Found p and q!")
    print("=" * 60)
    
    # Compute the flag
    flag_value = p * q
    print(f"\nFlag value: {flag_value}")
    
    # Try to convert to bytes/text if it makes sense
    if p < 2**1024:  # Reasonable size
        try:
            flag_bytes = p.to_bytes((p.bit_length() + 7) // 8, 'big')
            print(f"p as bytes: {flag_bytes}")
        except:
            pass
else:
    print("\nDid not find correct p and q with this approach.")
