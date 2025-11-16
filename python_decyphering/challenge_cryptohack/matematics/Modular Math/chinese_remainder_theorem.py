from functools import reduce
from operator import mul

def solve_crt(remainders, moduli):
    """Solves system of congruences using Chinese Remainder Theorem."""
    N = reduce(mul, moduli)
    return sum(a * (N_i := N // n) * pow(N_i, -1, n) for a, n in zip(remainders, moduli)) % N

remainders = [2, 3, 5]
moduli = [5, 11, 17]

result = solve_crt(remainders, moduli)

print(f"System: z ≡ {remainders[0]} (mod {moduli[0]}), z ≡ {remainders[1]} (mod {moduli[1]}), z ≡ {remainders[2]} (mod {moduli[2]})")
print(f"Solution: {result}\n")
print(f"Verification: {result} % {moduli[0]} = {result % moduli[0]}, {result} % {moduli[1]} = {result % moduli[1]}, {result} % {moduli[2]} = {result % moduli[2]}")