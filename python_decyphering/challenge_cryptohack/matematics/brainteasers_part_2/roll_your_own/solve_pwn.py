from pwn import *
import json

def solve():
    # Connect to the challenge server
    conn = remote('socket.cryptohack.org', 13403)

    # Receive the prime q
    conn.recvuntil(b'Prime generated: ')
    q_hex = conn.recvline().strip().decode().strip('"')
    q = int(q_hex, 16)
    log.info(f"Received q: {q}")

    # Choose n and g to make the DLP easy
    # We choose n = q^2 and g = q + 1.
    # This satisfies the server's condition pow(g, q, n) == 1 because:
    # (q+1)^q mod q^2 = 1 + q*q + ... = 1 (mod q^2) by binomial expansion.
    n = q * q
    g = q + 1
    
    log.info(f"Using n = q^2: {n}")
    log.info(f"Using g = q + 1: {g}")

    # Send g and n to the server
    conn.recvuntil(b'Send integers (g,n) such that pow(g,q,n) = 1: ')
    payload = json.dumps({"g": hex(g), "n": hex(n)})
    conn.sendline(payload.encode())
    log.info("Sent g and n")

    # Receive the public key h
    try:
        conn.recvuntil(b'Generated my public key: ')
        h_hex = conn.recvline().strip().decode().strip('"')
        h = int(h_hex, 16)
        log.info(f"Received h: {h}")
    except EOFError:
        log.error("Server closed connection. Parameters were likely rejected.")
        conn.close()
        return

    # Solve for x
    # The server computed h = pow(g, x, n) = pow(q+1, x, q^2).
    # By binomial expansion, (q+1)^x = 1 + x*q (mod q^2).
    # So, h = 1 + x*q (mod q^2).
    # This means h - 1 = x*q.
    # We can find x by x = (h - 1) / q.
    x = (h - 1) // q
    log.info(f"Found x: {x}")

    # Send x to the server
    conn.recvuntil(b'What is my private key: ')
    payload = json.dumps({"x": hex(x)})
    conn.sendline(payload.encode())

    # Receive the flag
    response = conn.recvall()
    log.success(f"Received response: {response.decode()}")
    conn.close()

if __name__ == "__main__":
    solve()
