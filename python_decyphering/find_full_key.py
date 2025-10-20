#!/usr/bin/env python3
"""
Find the FULL XOR key by analyzing patterns and trying to extend it.
"""

hex_cipher = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'
known_plain = 'crypto{'

cipher_bytes = bytes.fromhex(hex_cipher)

print("=" * 80)
print("FULL KEY FINDER")
print("=" * 80)
print(f"Ciphertext: {hex_cipher}")
print(f"Length: {len(cipher_bytes)} bytes")
print(f"Known plaintext: '{known_plain}'")
print()

# The pattern analysis showed repeating at distance 16
# This strongly suggests the key length is a divisor of 16 (1, 2, 4, 8, or 16)

# Extract first 7 bytes from known plaintext
partial_key = bytes([cipher_bytes[i] ^ ord(known_plain[i]) for i in range(len(known_plain))])
print(f"Partial key from 'crypto{{': {partial_key} -> '{partial_key.decode('utf-8', errors='ignore')}'")
print()

# Look for repeating patterns in ciphertext to determine actual key length
print("Looking for repeating patterns (key length hints):")
print("-" * 80)

# The repeating at distance 16 means either:
# - Key length is 16
# - Key length is 8 (and repeats twice to get 16)
# - Key length divides 16

# Let's try to extract more of the key by making assumptions
# If crypto{ is at position 0, and the same plaintext pattern appears elsewhere...

# Try different key lengths that divide into the repeating distance
for key_len in [8, 16]:
    print(f"\nTrying key length: {key_len}")
    
    # Build the key iteratively
    key = bytearray(key_len)
    key_confidence = [0] * key_len  # Track how confident we are about each byte
    
    # Use the known plaintext
    for i in range(min(len(known_plain), key_len)):
        key[i] = cipher_bytes[i] ^ ord(known_plain[i])
        key_confidence[i] += 10
    
    # Now try to decrypt and look for patterns
    decrypted = bytearray()
    for i in range(len(cipher_bytes)):
        decrypted.append(cipher_bytes[i] ^ key[i % key_len])
    
    decrypted_str = bytes(decrypted).decode('utf-8', errors='replace')
    print(f"  Key (hex): {bytes(key).hex()}")
    print(f"  Key (str): '{bytes(key).decode('utf-8', errors='replace')}'")
    print(f"  Decrypted: {decrypted_str}")
    
    # Check if it makes sense
    printable_count = sum(1 for c in decrypted_str if c.isprintable())
    print(f"  Printable chars: {printable_count}/{len(decrypted_str)} ({100*printable_count/len(decrypted_str):.1f}%)")
    
    # If we see "crypto{" and high printability, we might need to extend the key
    if decrypted_str.startswith('crypto{'):
        print(f"  ✓ Starts with 'crypto{{'!")
        
        # Try to guess more bytes by assuming common English words
        # Common patterns: "crypto{", could be followed by common chars
        print(f"  Analyzing character frequency...")
        
print("\n" + "=" * 80)
print("MANUAL KEY EXTENSION")
print("=" * 80)

# Let's assume the key is "myXORkey" (common pattern - "key" at the end)
test_keys = [
    b'myXORkey',
    b'myXORKey',
    b'myXORke!',
    b'myXORk3y',
]

def repeating_key_xor(ciphertext_bytes, key_bytes):
    decrypted_bytes = bytearray()
    for i in range(len(ciphertext_bytes)):
        decrypted_bytes.append(ciphertext_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return bytes(decrypted_bytes)

print("Testing common key variations:")
print("-" * 80)
for test_key in test_keys:
    decrypted = repeating_key_xor(cipher_bytes, test_key)
    try:
        decrypted_str = decrypted.decode('utf-8', errors='strict')
        print(f"\n✓ Key '{test_key.decode()}' ({test_key.hex()}):")
        print(f"  Decrypted: {decrypted_str}")
        if decrypted_str.endswith('}'):
            print(f"  ✓✓✓ COMPLETE! Ends with '}}' ✓✓✓")
    except:
        pass

print("\n" + "=" * 80)
