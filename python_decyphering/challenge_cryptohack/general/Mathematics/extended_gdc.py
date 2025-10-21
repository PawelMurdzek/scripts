def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor of a and b using Euclid's algorithm."""
    while b:
        a, b = b, a % b
    return abs(a)

print(gcd(12,8))
print(gcd(66528,52920))

# p*u+q*v=gcd(p,q)
# p*u = gcd(p,q) - q*v
# u = (gcd(p,q) - q*v)/p
# v = (gcd(p,q) - p*u)/q
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Compute the extended greatest common divisor of a and b.
    
    Returns a tuple (g, x, y) such that g = gcd(a, b) and g = a*x + b*y.
    """
    if a == 0:
        return b, 0, 1
    else:
        g, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y
    
result = extended_gcd(26513, 32321)
print(result)