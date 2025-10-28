import re
from math import gcd

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm
    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b)
    """
    if b == 0:
        return a, 1, 0
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return g, x, y

# Dictionary to store the parsed values
values = {}

try:
    # Read the data.txt file
    with open('data.txt', 'r') as f:
        content = f.read()

    # Use regex to find all 'key = value' pairs
    matches = re.findall(r'(\w+)\s*=\s*(\d+)', content)
    
    if not matches:
        print("Could not find any 'key = value' pairs in data.txt.")
        print("File content:")
        print(content)
    else:
        for key, value in matches:
            values[key] = int(value)
        
        print("Parsed values:")
        print(values)

        # Extract values
        N = values.get('N')
        e1 = values.get('e1')
        e2 = values.get('e2')
        c1 = values.get('c1')
        c2 = values.get('c2')

        if not all([N, e1, e2, c1, c2]):
            print("Error: File is missing one or more required values (N, e1, e2, c1, c2).")
        else:
            # --- Start of the solution ---
            
            # Let m1 = 2*p + 3*q
            # Let m2 = 5*p + 7*q
            # We have: c1 = m1^e1 mod N, c2 = m2^e2 mod N
            
            print(f"\nAnalyzing problem:")
            print(f"e1 bit length: {e1.bit_length()} bits")
            print(f"e2 bit length: {e2.bit_length()} bits")
            print(f"N bit length:  {N.bit_length()} bits")
            
            # Use the Common Modulus Attack / Bezout's identity
            # If gcd(e1, e2) = 1, we can find a and b such that:
            # a*e1 + b*e2 = 1
            # Then: c1^a * c2^b = (m1^e1)^a * (m2^e2)^b = m1^(a*e1) * m2^(b*e2) mod N
            
            g, a, b = extended_gcd(e1, e2)
            print(f"\ngcd(e1, e2) = {g}")
            
            if g != 1:
                print(f"ERROR: gcd(e1, e2) = {g}, not 1. Common modulus attack won't work directly.")
                print("This problem may require a different approach.")
            else:
                print(f"a*e1 + b*e2 = 1, where a = {a}, b = {b}")
                
                # Now we can compute linear combinations
                # But wait - we have TWO different messages (m1 and m2), not the same message
                # So we can't directly use common modulus attack
                
                # Instead, let's use the fact that m1 and m2 are linear combinations:
                # m1 = 2*p + 3*q
                # m2 = 5*p + 7*q
                
                # We can create linear combinations of c1 and c2 to get information about p and q
                # Let's compute: 7*m1 - 3*m2 = 7*(2p+3q) - 3*(5p+7q) = 14p + 21q - 15p - 21q = -p
                # And: 5*m1 - 2*m2 = 5*(2p+3q) - 2*(5p+7q) = 10p + 15q - 10p - 14q = q
                
                # So we need: (7*m1 - 3*m2) = -p and (5*m1 - 2*m2) = q
                # In terms of ciphertexts, we need to compute:
                # m1^7 * m2^(-3) mod N and m1^5 * m2^(-2) mod N
                
                # But we have c1 = m1^e1 and c2 = m2^e2
                # We need to "extract" m1 and m2 from these exponentiations
                
                # Actually, let me try a different approach using resultants or lattices
                # For now, let's try if the messages are small enough for Coppersmith
                
                print("\nThis problem requires advanced techniques (Coppersmith, lattices, or resultants).")
                print("The messages are likely related by known linear combinations,")
                print("and we need to exploit the structure more cleverly.")
                
                # Let me try a simpler check: are the exponents e1, e2 related to N?
                # Sometimes in challenges, e1 = d1 mod phi(N) where d1 is small
                
                # Or perhaps we can use the fact that we know the relationship between m1 and m2
                # and try to construct a polynomial relation
                
                print("\nAttempting alternative: checking if exponents reveal structure...")
                print(f"e1 mod N = {e1 % N}")
                print(f"e2 mod N = {e2 % N}")
                
                # Try checking if c1 or c2 when raised to small powers reveal anything
                # This is a heuristic approach
                for small_e in [1, 2, 3, 5, 7, 11, 13, 17, 19, 23]:
                    test = pow(c1, small_e, N)
                    if test < 10**20:  # If it's small, it might be meaningful
                        print(f"c1^{small_e} mod N = {test}")
                    test = pow(c2, small_e, N)
                    if test < 10**20:
                        print(f"c2^{small_e} mod N = {test}")
                
                print("\n=== Unable to solve with current simple methods ===")
                print("This challenge requires SageMath or advanced number theory libraries.")
                print("Consider using Coppersmith's attack or lattice-based methods.")

except FileNotFoundError:
    print("Error: data.txt not found. Please place data.txt in the same directory as this script.")
except Exception as e:
    print(f"An error occurred: {e}")