from Crypto.Util.number import *
import itertools
from tqdm import tqdm
import json
from pwn import remote

HOST = "socket.cryptohack.org"
PORT = 13385

def generate_prime_basis(n):
    """Generate all primes up to n using Sieve of Eratosthenes."""
    sieve = [True] * n
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i]:
            sieve[i*i::2*i] = [False] * ((n - i*i - 1) // (2*i) + 1)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


def miller_rabin_test(n, max_base):
    """
    Miller-Rabin primality test using all prime bases < max_base.
    Returns True if n is probably prime, False if definitely composite.
    """
    prime_bases = generate_prime_basis(max_base)
    
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * s
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    
    # Test with each prime base
    for base in prime_bases:
        x = pow(base, s, n)
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def extended_gcd(a, b):
    """Extended Euclidean algorithm. Returns (gcd, s, t) where gcd = a*s + b*t."""
    s, s1 = 0, 1
    t, t1 = 1, 0
    r, r1 = b, a
    
    while r != 0:
        q = r1 // r
        r1, r = r, r1 - q * r
        s1, s = s, s1 - q * s
        t1, t = t, t1 - q * t
    
    return (r1, s1, t1)


def chinese_remainder_theorem(residues, modulos):
    """
    Solve system of congruences: x ≡ residues[i] (mod modulos[i]).
    Returns (solution, combined_modulo) or (-1, -1) if no solution exists.
    """
    result_mod = modulos[0]
    result_res = residues[0]
    
    for residue, modulo in zip(residues[1:], modulos[1:]):
        g = GCD(result_mod, modulo)
        
        # Check if solution exists
        if residue % g != result_res % g:
            return -1, -1
        
        _, s, t = extended_gcd(modulo // g, result_mod // g)
        result_res = result_res * (modulo // g) * s + residue * (result_mod // g) * t
        result_mod *= modulo // g
        result_res %= result_mod
    
    return result_res, result_mod


def legendre_symbol(a, p):
    """Compute Legendre symbol (a/p) = a^((p-1)/2) mod p."""
    return pow(a, (p - 1) // 2, p)


def find_valid_residues(primes, num_factors):
    """
    Find residues that satisfy the Legendre symbol condition for fooling Miller-Rabin.
    """
    valid_residues = []
    ks = [1, 998244353, 233]  # Multipliers for constructing the pseudoprime
    
    for prime in primes:
        residue_set = set()
        larger_primes = generate_prime_basis(200 * prime)[1:]
        
        for q in larger_primes:
            if legendre_symbol(prime, q) == q - 1:
                residue_set.add(q % (4 * prime))
        
        valid_residues.append(list(residue_set))
    
    # Filter residues to work with all factors
    filtered_residues = []
    for idx, residue_list in enumerate(valid_residues):
        prime = primes[idx]
        modulus = prime * 4
        current_set = set(residue_list)
        
        for i in range(1, num_factors):
            new_set = set()
            for res in residue_list:
                transformed = ((res + ks[i] - 1) * inverse(ks[i], modulus)) % modulus
                if transformed % 4 == 3:
                    new_set.add(transformed)
            current_set = current_set.intersection(new_set)
        
        filtered_residues.append(current_set)
    
    return filtered_residues, ks


def generate_strong_pseudoprime(primes, filtered_residues, ks, num_factors, 
                                min_bits=600, max_bits=900):
    """
    Generate a strong pseudoprime that passes Miller-Rabin test.
    Returns (pseudoprime, factors) or (None, None) if not found.
    """
    total_combinations = 1
    for res_set in filtered_residues:
        total_combinations *= len(res_set)
    print(f"Total combinations to try: {total_combinations}")
    
    for residue_tuple in itertools.product(*filtered_residues):
        residues = []
        modulos = []
        
        # Build CRT system from residue tuple
        for i, res in enumerate(residue_tuple):
            residues.append(res)
            modulos.append(primes[i] * 4)
        
        # Add constraints from ks multipliers
        residues.append(ks[1] - inverse(ks[2], ks[1]))
        modulos.append(ks[1])
        residues.append(ks[2] - inverse(ks[1], ks[2]))
        modulos.append(ks[2])
        
        solution, combined_mod = chinese_remainder_theorem(residues, modulos)
        
        if solution == -1:
            continue
        
        # Start search from a large value
        candidate = 2**73 * combined_mod + solution
        
        for _ in tqdm(range(100000)):
            if isPrime(candidate):
                # Build the pseudoprime from candidate and its multiples
                pseudoprime = candidate
                factors = [candidate]
                
                for i in range(1, num_factors):
                    factor = ks[i] * (candidate - 1) + 1
                    factors.append(factor)
                    pseudoprime *= factor
                
                # Check if it passes Miller-Rabin and has correct bit length
                if miller_rabin_test(pseudoprime, 64):
                    bit_len = pseudoprime.bit_length()
                    if min_bits <= bit_len <= max_bits:
                        print(f"Found pseudoprime! isPrime check: {isPrime(pseudoprime)}")
                        print(f"Pseudoprime: {pseudoprime}")
                        print(f"Factors: {factors}")
                        return pseudoprime, factors
            
            candidate += combined_mod
    
    return None, None


# Main execution: Generate strong pseudoprime
NUM_FACTORS = 3
prime_bases = generate_prime_basis(64)
print(f"Number of prime bases: {len(prime_bases)}")
print(f"Prime bases: {prime_bases}")

filtered_residues, ks_multipliers = find_valid_residues(prime_bases, NUM_FACTORS)
print(f"Filtered residue sets: {filtered_residues}")

pseudoprime, factors = generate_strong_pseudoprime(
    prime_bases, filtered_residues, ks_multipliers, NUM_FACTORS
)
found = (pseudoprime is not None)

def solve(p, facs):
    """
    This function will connect to the server and send the payload.
    Uses the generated strong pseudoprime and its factors.
    p = product of facs, where p is composite but passes Miller-Rabin
    
    The key: since p is composite, we can choose 'a' such that gcd(a, p) > 1
    or such that a^(p-1) is NOT 1 mod p.
    """
    
    # Strategy: Make 'a' share a factor with p
    # If a = k * facs[0] for some k, then gcd(a, p) = facs[0] > 1
    # The server checks a < p, so we need a to be smaller than p but share a factor
    
    # Try using one of the factors directly or a small multiple
    for i, fac in enumerate(facs):
        print(f"\nTrying with factor {i}: {fac}")
        
        # Try small multiples of this factor
        for k in range(2, 10):
            a = k * fac
            if a >= p:
                break
                
            print(f"Trying a = {k} * factor = {a}")
            
            # Check what we get locally
            result = pow(a, p-1, p)
            print(f"Local test: pow(a, p-1, p) = {result}")
            
            r = remote(HOST, PORT)
            r.recvuntil(b"primes!\n")

            payload = json.dumps({"base": a, "prime": p})
            r.sendline(payload.encode())

            response = r.recvline().decode()
            try:
                data = json.loads(response)
                if "Response" in data:
                    print(data["Response"])
                    if "crypto{" in data["Response"]:
                        print(f"\n*** FOUND FLAG! ***")
                        r.close()
                        return
                else:
                    print(data)
            except json.JSONDecodeError:
                print(response)

            r.close()

if __name__ == "__main__":
    if found:
        print(f"Generated pseudoprime with bit length: {pseudoprime.bit_length()}")
        print(f"Factors: {factors}")
        solve(pseudoprime, factors)
    else:
        print("Failed to generate suitable pseudoprime")
