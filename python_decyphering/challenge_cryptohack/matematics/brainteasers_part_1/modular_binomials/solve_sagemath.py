"""
FINAL SOLUTION using SageMath
This requires SageMath to be installed
Run with: sage solve_sagemath.py
"""

# Parse data
import re

values = {}
with open('data.txt', 'r') as f:
    content = f.read()
matches = re.findall(r'(\w+)\s*=\s*(\d+)', content)
for key, value in matches:
    values[key] = int(value)

N = Integer(values['N'])
e1 = Integer(values['e1'])
e2 = Integer(values['e2'])
c1 = Integer(values['c1'])
c2 = Integer(values['c2'])

print("SageMath Solution for Modular Binomials")
print("=" * 60)
print(f"N = {N}")
print(f"e1 = {e1}")
print(f"e2 = {e2}")
print(f"c1 = {c1}")
print(f"c2 = {c2}")
print()

# Create polynomial ring
print("Setting up polynomial ring...")
R = Zmod(N)
P.<p, q> = PolynomialRing(R)

# Define the polynomials
# m1 = 2*p + 3*q
# m2 = 5*p + 7*q
# c1 = m1^e1 mod N
# c2 = m2^e2 mod N

m1 = 2*p + 3*q
m2 = 5*p + 7*q

# Create the polynomial equations
f1 = m1^e1 - c1
f2 = m2^e2 - c2

print("Polynomial equations created:")
print(f"f1 = (2p + 3q)^e1 - c1")
print(f"f2 = (5p + 7q)^e2 - c2")
print()

print("Computing Groebner basis...")
print("(This may take a while...)")

try:
    I = ideal([f1, f2, p*q - N])
    G = I.groebner_basis()
    
    print(f"Groebner basis has {len(G)} elements")
    print()
    
    # Try to extract p and q from the Groebner basis
    for g in G:
        print(f"Basis element: {g}")
        
    # Look for univariate polynomials in the basis
    for g in G:
        if g.degree(q) == 0 and g.degree(p) > 0:
            print(f"\nFound univariate in p: {g}")
            # Solve for p
            roots_p = g.univariate_polynomial().roots()
            if roots_p:
                p_val = roots_p[0][0]
                q_val = N / p_val
                print(f"p = {p_val}")
                print(f"q = {q_val}")
                print(f"Verification: p*q = {p_val * q_val}")
                
        elif g.degree(p) == 0 and g.degree(q) > 0:
            print(f"\nFound univariate in q: {g}")
            roots_q = g.univariate_polynomial().roots()
            if roots_q:
                q_val = roots_q[0][0]
                p_val = N / q_val
                print(f"p = {p_val}")
                print(f"q = {q_val}")
                print(f"Verification: p*q = {p_val * q_val}")
                
except Exception as e:
    print(f"Error computing Groebner basis: {e}")
    print()
    print("Alternative: Use resultants...")
    
    try:
        # Compute resultant to eliminate one variable
        print("Computing resultant of f1 and f2 with respect to q...")
        res_q = f1.resultant(f2, q)
        print(f"Resultant (eliminating q): {res_q}")
        
        # Solve the resultant for p
        print("Solving resultant for p...")
        # This gives a univariate polynomial in p
        
    except Exception as e2:
        print(f"Resultant method also failed: {e2}")

print("\n" + "=" * 60)
print("If SageMath solution works, you should see p and q above.")
