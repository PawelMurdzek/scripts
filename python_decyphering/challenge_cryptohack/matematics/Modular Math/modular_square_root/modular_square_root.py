import re

def tonelli_shanks(a, p):
    """Tonelli-Shanks algorithm for finding modular square root when p % 4 == 1."""
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    
    # Factor p - 1 as Q * 2^S
    Q, S = p - 1, 0
    while Q % 2 == 0:
        Q //= 2
        S += 1
    
    # Find quadratic non-residue
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1
    
    # Initialize
    c = pow(z, Q, p)
    R = pow(a, (Q + 1) // 2, p)
    t = pow(a, Q, p)
    M = S
    
    while t != 1:
        # Find smallest i where t^(2^i) == 1
        i, temp_t = 0, t
        while temp_t != 1:
            temp_t = pow(temp_t, 2, p)
            i += 1
        
        # Update values
        b = pow(c, 1 << (M - i - 1), p)
        R = (R * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        M = i
    
    return R

def find_modular_sqrt(a, p):
    """Find modular square root. Returns the smaller of the two roots."""
    a = a % p
    if a == 0:
        return 0
    
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
    elif p % 4 == 1:
        r = tonelli_shanks(a, p)
    else:
        return None
    
    return min(r, p - r) if r else None

def main():
    with open('output.txt', 'r') as f:
        content = f.read()
    
    # Parse a and p from file
    a = int(re.search(r'a\s*=\s*(\d+)', content).group(1))
    p = int(re.search(r'p\s*=\s*(\d+)', content).group(1))
    
    print(f"a = {str(a)[:60]}...")
    print(f"p = {str(p)[:60]}...")
    print(f"p % 4 = {p % 4} ({'Tonelli-Shanks' if p % 4 == 1 else 'Simple formula'})\n")
    
    # Calculate modular square root
    result = find_modular_sqrt(a, p)
    
    if result is None:
        print("No square root exists")
    else:
        print(f"The smaller of the two roots is: {result}")
        print(f"\nVerification: {result}^2 % p == a ? {pow(result, 2, p) == a % p}")

if __name__ == "__main__":
    main()