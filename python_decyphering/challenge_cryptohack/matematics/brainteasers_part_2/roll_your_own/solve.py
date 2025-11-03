from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime, isPrime
from sympy.ntheory import discrete_log
def solve():
    conn = remote('127.0.0.1', 13403)

    # Receive q
    conn.recvuntil(b'Prime generated: ')
    q_hex = conn.recvline().strip().decode()
    q = int(q_hex, 16)
    log.info(f"Received q: {q}")

    # Find n = 2*q + 1, which is a safe prime, so it is prime.
    n = 2 * q + 1
    log.info(f"Calculated n: {n}")

    # Find a generator g of order q.
    # Let's try g=2. The order of 2 is a divisor of n-1 = 2q.
    # The order can be 1, 2, q, 2q.
    # Order is not 1 as 2 != 1.
    # Order is not 2 as 2^2 = 4 != 1 mod n.
    # pow(2, q, n) is -1 mod n by Euler's criterion, so not 1.
    # So order is 2q.
    # The challenge requires pow(g,q,n) == 1.
    # Let's use g = 4. pow(4,q,n) = pow(2^2, q, n) = pow(2^(2q), 1, n) = 1.
    g = 4
    log.info(f"Using g: {g}")

    # Send g and n
    conn.recvuntil(b'Send integers (g,n) such that pow(g,q,n) = 1: ')
    payload = f'{{"g": "{hex(g)}", "n": "{hex(n)}"}}'
    conn.sendline(payload.encode())
    log.info("Sent g and n")

    # Receive h
    conn.recvuntil(b'Generated my public key: ')
    h_hex = conn.recvline().strip().decode()
    h = int(h_hex, 16)
    log.info(f"Received h: {h}")

    # We need to find x such that h = g^x mod n.
    # This is a discrete logarithm problem.
    # Since we chose n and g, we can solve this.
    # h = 4^x mod n = (2^2)^x mod n = 2^(2x) mod n
    # We can use Pohlig-Hellman, but the group order is q, which is large.
    # However, the problem is that x is chosen from range(0, q).
    # h = g^x mod n.
    # The order of g=4 is q.
    # We can compute the discrete log of h base g in the group of order q.
    # Since q is prime, we can use algorithms like Shanks or Pollard's rho.
    # Let's try to find x.
    # sage: n = 2*q+1
    # sage: F = GF(n)
    # sage: g_sage = F(g)
    # sage: h_sage = F(h)
    # sage: x = h_sage.log(g_sage)
    # This should give x.
    # Let's try to find x by hand.
    # h = 4^x mod n.
    # We know x is in [0, q-1].
    # The Pohlig-Hellman attack is feasible if the order of the group has small prime factors.
    # The order of g is q, which is a large prime.
    # So we need to solve for x in h = g^x mod n.
    # Let's use a known library to solve the discrete logarithm.
    
    x = discrete_log(n, h, g)
    log.info(f"Found x: {x}")

    # Send x
    conn.recvuntil(b'What is my private key: ')
    payload = f'{{"x": "{hex(x)}"}}'
    conn.sendline(payload.encode())
    log.info("Sent x")

    # Receive flag
    response = conn.recvall().decode()
    log.success(f"Received response: {response}")

if __name__ == "__main__":
    solve()
