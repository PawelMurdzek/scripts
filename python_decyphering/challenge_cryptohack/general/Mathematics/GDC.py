def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor of a and b using Euclid's algorithm."""
    while b:
        a, b = b, a % b
    return abs(a)

print(gcd(12,8))
print(gcd(66528,52920))