from sympy import  primerange

p = 28151

def is_primitive_root(g, p):
    prime_divisors = []
    for q in primerange(1, p):
        if (p-1) % q == 0:
            prime_divisors.append(q)
    
    for q in prime_divisors:
        if pow(g, (p-1)//q, p) == 1:
            return False
    return True

for g in range(2, p):  
    if is_primitive_root(g, p):
        print(g)
        break
