from sympy import primerange

def is_primitive_root(g, p):
    for q in primerange(2, p):
        if (p - 1) % q == 0 and pow(g, (p - 1) // q, p) == 1:
            return False
    return True

p = 28151

for g in range(2, p):
    if is_primitive_root(g, p):
        print(g)
        break
