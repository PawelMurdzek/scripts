"""
Approach 4: Check if e1, e2 are related to small values
Maybe the problem is: c1 = (2p+3q)^e1 mod N where e1 is small
Try computing e-th roots for small e values
"""
import re

def iroot_newton(n, k):
    """Compute integer k-th root using Newton's method"""
    if n < 0:
        return None
    if n == 0:
        return 0
    if n == 1:
        return 1
    if k == 1:
        return n
    
    # Newton's method
    bit_length = n.bit_length()
    x = 1 << ((bit_length + k - 1) // k)
    
    while True:
        x_k_minus_1 = pow(x, k - 1)
        x_new = ((k - 1) * x + n // x_k_minus_1) // k
        
        if x_new >= x:
            break
        x = x_new
    
    # Check if exact
    if pow(x, k) == n:
        return x
    if pow(x + 1, k) == n:
        return x + 1
    
    return None

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

print("Approach 4: Testing small exponent roots")
print("=" * 60)
print("Checking if c1 = m1^k for small k (ignoring e1)...")

# Try small exponents
for k in range(2, 100):
    m1 = iroot_newton(c1, k)
    if m1 is not None:
        print(f"\nFound: c1 = m1^{k}")
        print(f"m1 = {m1}")
        
        # Now try c2
        m2 = iroot_newton(c2, k)
        if m2 is not None:
            print(f"Found: c2 = m2^{k}")
            print(f"m2 = {m2}")
            
            # Try to solve system
            p = 3 * m2 - 7 * m1
            q = 5 * m1 - 2 * m2
            
            print(f"\nSolving system:")
            print(f"p = {p}")
            print(f"q = {q}")
            print(f"p * q = {p * q}")
            print(f"N     = {N}")
            print(f"Match: {p * q == N}")
            
            if p * q == N:
                print("\n" + "=" * 60)
                print("SUCCESS!")
                print("=" * 60)
                break
        else:
            print(f"But c2 is not a perfect {k}-th power")

print("\nApproach 4 complete.")
