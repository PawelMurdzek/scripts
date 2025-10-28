"""
Approach 6: Low Public Exponent Attack / Small message attack
Check if the actual encryption exponent used is small (like 3, 65537)
and if so, try Hastad's broadcast attack or simple root extraction
"""
import re

def iroot_binary_search(n, k, tolerance=10**50):
    """Binary search for integer k-th root, optimized for large numbers"""
    if n == 0:
        return 0, True
    if n == 1:
        return 1, True
    if k == 1:
        return n, True
    
    # Better bounds using bit length
    low = 1 << ((n.bit_length() - 1) // k)
    high = 1 << ((n.bit_length() + k - 1) // k)
    
    iterations = 0
    max_iterations = 10000
    
    while low <= high and iterations < max_iterations:
        mid = (low + high) // 2
        mid_pow = pow(mid, k)
        
        if mid_pow == n:
            return mid, True
        elif mid_pow < n:
            low = mid + 1
        else:
            high = mid - 1
        
        iterations += 1
        if iterations % 1000 == 0:
            print(f"    Binary search iteration {iterations}...")
    
    # Check the boundaries
    if pow(low, k) == n:
        return low, True
    if pow(high, k) == n:
        return high, True
    
    return None, False

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

print("Approach 6: Low Public Exponent Attack")
print("=" * 60)

# Common public exponents
common_exponents = [3, 5, 7, 11, 13, 17, 65537]

print("Testing common public exponents for c1...")
for e in common_exponents:
    print(f"\nTrying e = {e}:")
    
    # Check if c1 < N^e (no modular reduction happened)
    if c1 < pow(N, e):
        print(f"  c1 < N^{e}, trying integer root...")
        m1, exact = iroot_binary_search(c1, e)
        
        if exact and m1:
            print(f"  SUCCESS! Found m1 = {m1}")
            
            # Now try same exponent for c2
            if c2 < pow(N, e):
                m2, exact2 = iroot_binary_search(c2, e)
                if exact2 and m2:
                    print(f"  SUCCESS! Found m2 = {m2}")
                    
                    # Solve system
                    p = 3 * m2 - 7 * m1
                    q = 5 * m1 - 2 * m2
                    
                    print(f"\n  Solving system:")
                    print(f"  p = {p}")
                    print(f"  q = {q}")
                    print(f"  p * q == N: {p * q == N}")
                    
                    if p * q == N:
                        print("\n" + "=" * 60)
                        print("SOLUTION FOUND!")
                        print("=" * 60)
                        print(f"p = {p}")
                        print(f"q = {q}")
                        exit(0)
    else:
        print(f"  c1 >= N^{e}, modular reduction likely happened")

print("\nNo solution found with common small exponents.")
