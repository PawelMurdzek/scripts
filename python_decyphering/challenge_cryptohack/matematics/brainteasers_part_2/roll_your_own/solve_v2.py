from pwn import *
from Crypto.Util.number import long_to_bytes
import json

def solve():
    conn = remote('localhost', 13403)

    # Step 1: Receive q
    conn.recvuntil(b'Prime generated: ')
    q_hex = conn.recvline().strip().decode()
    q = int(q_hex, 16)
    log.info(f"Received q: {q}")

    # Step 2: Choose n and g
    # We need pow(g, q, n) == 1.
    # Let's choose n = q + 1.
    # Then pow(g, q, n) = pow(g, -1, q+1).
    # We need g^-1 = 1 mod (q+1), which means g = 1. But g must be > 1.
    # Let's try a different n.
    # Let n be a prime of the form k*q + 1.
    # Let's try to find a small k for which n is prime.
    # Let's pick n = q+1. This is not prime.
    # Let's pick n = 2*q + 1. This is a safe prime. DLP is hard.
    # The trick is to use Pohlig-Hellman. We need the order of the group to have small prime factors.
    # The order of g is q, which is prime. So Pohlig-Hellman on the subgroup of order q is not useful.
    # We need to solve h = g^x mod n.
    # What if we choose n such that phi(n) has small factors?
    # Let n = p1 * p2 * ...
    # Let's choose n = q + 1. phi(n) might have small factors.
    # Let's try n = q + 1.
    # We need pow(g, q, q+1) == 1.
    # pow(g, q, q+1) == pow(g, -1, q+1) == 1. This implies g=1, which is not allowed.
    #
    # Let's reconsider the problem.
    # We control g and n.
    # The server computes h = g^x mod n. x is in [0, q-1].
    # We need to find x.
    #
    # Let's use Chinese Remainder Theorem.
    # Let n = p1 * p2.
    # h = g^x mod p1
    # h = g^x mod p2
    # We can solve for x mod (p1-1) and x mod (p2-1).
    # Let's choose p1 and p2 to be primes with p1-1 and p2-1 having small factors.
    # And we need pow(g, q, p1*p2) == 1.
    # This means order of g must divide q. So order is q.
    # This means q must divide lambda(n) = lcm(p1-1, p2-1).
    # So let's choose p1 = k1*q + 1 and p2 = k2*q + 1.
    # For simplicity, let's choose k1=2, so p1 = 2*q+1 (if prime).
    # And we need another prime p2.
    # Let's try to find a prime n = k*q + 1, where k is small and smooth.
    # Let k=2. n = 2*q+1. n-1 = 2q. Order of g can be q. DLP is hard.
    # Let k=3. n = 3*q+1. n-1 = 3q.
    # Let k=6. n = 6*q+1. n-1 = 6q = 2*3*q.
    # Let's find a prime n = k*q + 1 where k is smooth.
    # Let's try to find a prime n of the form k*q+1.
    from sympy import isprime
    k = 2
    while True:
        n = k * q + 1
        if isprime(n):
            log.info(f"Found prime n for k={k}")
            break
        k += 1
    
    # Now n-1 = k*q.
    # We need a generator g for the subgroup of order q.
    # Let's find a generator 'a' of (Z/nZ)*.
    # Then g = a^k mod n has order q.
    # pow(g, q, n) = pow(a^k, q, n) = pow(a, k*q, n) = pow(a, n-1, n) = 1.
    # How to find a generator 'a'? Find a primitive root.
    # Let's just try a=2.
    a = 2
    g = pow(a, k, n)

    if pow(g, q, n) != 1:
        log.error("g^q mod n is not 1. Trying a=3")
        a = 3
        g = pow(a, k, n)
        if pow(g, q, n) != 1:
            log.error("g^q mod n is not 1. Aborting.")
            return

    log.info(f"Using n: {n}")
    log.info(f"Using g: {g}")

    # Step 3: Send g and n
    conn.recvuntil(b'Send integers (g,n) such that pow(g,q,n) = 1: ')
    payload = json.dumps({"g": hex(g), "n": hex(n)})
    conn.sendline(payload.encode())
    log.info("Sent g and n")

    # Step 4: Receive h
    conn.recvuntil(b'Generated my public key: ')
    line = conn.recvline().strip().decode()
    h_hex = json.loads(line)['h']
    h = int(h_hex, 16)
    log.info(f"Received h: {h}")

    # Step 5: Solve DLP
    # h = g^x mod n. We need to find x.
    # We are in a subgroup of order q.
    # h_k = h^k mod n = (g^x)^k mod n = (a^k)^x*k mod n = a^(x*k^2) mod n? No.
    # h = g^x mod n
    # h = (a^k)^x mod n
    # We need to find x in [0, q-1].
    # This is still a DLP in a group of order q.
    #
    # Let's rethink. The server code is:
    # self.x = random.randint(0, self.q)
    # self.h = pow(self.g, self.x, self.n)
    #
    # The key is that x is in [0, q]. Not [0, n-1].
    #
    # Let's go back to n = p1 * p2.
    # Let p1 = 2*q+1 and p2 = 3*q+1. (if they are prime)
    # n = p1*p2.
    # lambda(n) = lcm(p1-1, p2-1) = lcm(2q, 3q) = 6q.
    # We need g of order q.
    # Let a be a common primitive root for p1 and p2.
    # g = a^6 mod n. Then g^q = a^(6q) mod n.
    # a^(6q) mod p1 = a^(lcm(2q,3q)) mod p1 = a^(3*(p1-1)) mod p1 = 1.
    # a^(6q) mod p2 = a^(2*(p2-1)) mod p2 = 1.
    # So g^q = 1 mod n.
    #
    # Now we have h = g^x mod n.
    # We can solve h = g^x mod p1 and h = g^x mod p2.
    # This gives x mod ord_p1(g) and x mod ord_p2(g).
    # The order of g mod p1 is q. The order of g mod p2 is q.
    # So we get x mod q. Which is what we need.
    # But DLP over F_p1 with order q is still hard.
    #
    # What if we choose n such that n-1 is smooth?
    # Let's try to find a prime n = k*q+1 where k is small.
    # We found such n. n-1 = k*q.
    # h = g^x mod n.
    # Let's take the k-th power of h.
    # h' = h^k = (g^x)^k = (a^k)^x*k = g^(x*k) mod n. No.
    # h' = h^k = (g^x)^k = (g^k)^x mod n.
    # g = a^k mod n.
    # h = (a^k)^x mod n.
    # h^k = ((a^k)^x)^k = a^(x*k^2) mod n. This doesn't help.
    #
    # Let's try to find x by Pohlig-Hellman on h with base a.
    # h = a^y mod n. We can find y because n-1 = k*q and k is small.
    # y = discrete_log(n, h, a).
    # We have h = g^x = (a^k)^x = a^(k*x) mod n.
    # So y = k*x mod (n-1).
    # y = k*x mod (k*q).
    # This means y is a multiple of k. y = k*x - m*k*q = k*(x-m*q).
    # So y = k*x (mod k*q).
    # This implies y = k*x + m*k*q for some integer m.
    # y/k = x + m*q.
    # x = (y/k) mod q.
    #
    # So the plan is:
    # 1. Find small k such that n=k*q+1 is prime.
    # 2. Find a generator 'a' of (Z/nZ)*. (Try a=2, 3, 5...)
    # 3. Calculate g = a^k mod n.
    # 4. Send g, n. Receive h.
    # 5. Calculate y = discrete_log(n, h, a). This is feasible if k is smooth.
    # 6. Calculate x = (y * k^-1) mod q.
    #
    # How to compute discrete_log for step 5.
    # We need a library for that. `sympy.ntheory.discrete_log` should work if k is smooth.
    # Let's try to implement a simple Pohlig-Hellman.
    
    from sympy.ntheory import discrete_log, factorint
    from sympy.ntheory.residue_ntheory import primitive_root

    # Find k
    k = 2
    while True:
        n = k * q + 1
        if isprime(n):
            log.info(f"Found prime n for k={k}")
            break
        if k > 100000: # safety break
            log.error("Could not find suitable n")
            return
        k += 1

    # Find primitive root 'a'
    a = primitive_root(n)
    log.info(f"Found primitive root a: {a}")

    g = pow(a, k, n)
    log.info(f"Calculated g: {g}")

    # Send g, n
    conn.recvuntil(b'Send integers (g,n) such that pow(g,q,n) = 1: ')
    payload = json.dumps({"g": hex(g), "n": hex(n)})
    conn.sendline(payload.encode())

    # Receive h
    conn.recvuntil(b'Generated my public key: ')
    line = conn.recvline().strip().decode()
    # The response is not a valid json, it's just the hex string.
    # Let's parse it correctly.
    h_hex = line
    h = int(h_hex, 16)
    log.info(f"Received h: {h}")

    # Calculate y = discrete_log_a(h)
    # n-1 = k*q. We need to make sure k is smooth enough for discrete_log.
    log.info(f"Factors of k={k}: {factorint(k)}")
    y = discrete_log(n, h, a)
    log.info(f"Found y = discrete_log_a(h): {y}")

    # Calculate x
    # y = k*x mod (n-1)
    # y = k*x mod (k*q)
    # This means y must be divisible by k.
    if y % k != 0:
        log.error("y is not divisible by k. Something is wrong.")
        return
    
    x = (y // k) % q

    log.info(f"Found x: {x}")

    # Send x
    conn.recvuntil(b'What is my private key: ')
    payload = json.dumps({"x": hex(x)})
    conn.sendline(payload.encode())

    # Receive flag
    response = conn.recvall()
    log.success(f"Received response: {response.decode()}")

if __name__ == "__main__":
    solve()
