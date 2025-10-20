#!/usr/bin/env python3
"""
Find XOR key using known plaintext attack.
We know the plaintext contains "crypto{" and can use this to find the key.
"""

hex_cipher = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'
known_plain = 'crypto{'

# Convert hex to bytes
cipher_bytes = bytes.fromhex(hex_cipher)

print("Known-Plaintext Attack")
print("=" * 80)
print(f"Ciphertext (hex): {hex_cipher}")
print(f"Known plaintext: '{known_plain}'")
print(f"Ciphertext length: {len(cipher_bytes)} bytes")
print("=" * 80)
print()

def repeating_key_xor(ciphertext_bytes, key_bytes):
    if not key_bytes:
        return ciphertext_bytes
    decrypted_bytes = bytearray()
    for i in range(len(ciphertext_bytes)):
        decrypted_bytes.append(ciphertext_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return bytes(decrypted_bytes)

# First, try single-byte XOR
print("1. Testing Single-Byte XOR")
print("-" * 80)
for offset in range(len(cipher_bytes) - len(known_plain) + 1):
    potential_key_bytes = []
    for i in range(len(known_plain)):
        potential_key_bytes.append(cipher_bytes[offset + i] ^ ord(known_plain[i]))
    
    # Check if all bytes are the same (single-byte key)
    if len(set(potential_key_bytes)) == 1:
        key = potential_key_bytes[0]
        print(f"! Found single-byte XOR key at offset {offset}!")
        print(f"  Key: {key} (0x{key:02x}, ASCII: '{chr(key) if 32<=key<=126 else '?'}')")
        
        decrypted = bytes([b ^ key for b in cipher_bytes])
        try:
            decrypted_str = decrypted.decode('utf-8')
            print(f"  Decryption: {decrypted_str}")
            if 'crypto{' in decrypted_str:
                print(f"  !!! SUCCESS! !!!")
        except:
            pass
        print()

# Now try repeating key patterns
print("\n2. Analyzing Repeating Key Patterns")
print("-" * 80)

# Extract potential key by XORing known plaintext with ciphertext at position 0
potential_key = bytes([cipher_bytes[i] ^ ord(known_plain[i]) for i in range(len(known_plain))])
print(f"Key bytes from 'crypto{{' at position 0:")
print(f"  Hex: {potential_key.hex()}")
print(f"  As string: '{potential_key.decode('utf-8', errors='ignore')}'")
print(f"  As bytes: {list(potential_key)}")
print()

# Try different key lengths
print("3. Testing Different Key Lengths")
print("-" * 80)

for key_len in range(1, 21):
    # Use the first key_len bytes as the repeating key
    test_key = potential_key[:key_len]
    decrypted = repeating_key_xor(cipher_bytes, test_key)
    
    try:
        decrypted_str = decrypted.decode('utf-8', errors='strict')
        
        # Check if it contains crypto{ and looks like valid text
        if 'crypto{' in decrypted_str:
            print(f"! Key length {key_len} - PROMISING!")
            print(f"  Key (hex): {test_key.hex()}")
            print(f"  Key (str): '{test_key.decode('utf-8', errors='ignore')}'")
            print(f"  Decrypted: {decrypted_str}")
            
            # Check if decryption is complete (ends with })
            if decrypted_str.strip().endswith('}'):
                print(f"  !!! COMPLETE MESSAGE! !!!")
            print()
    except:
        pass

# Advanced: Try to find key by looking for patterns in the ciphertext
print("\n4. Pattern Analysis - Finding Repeating Blocks")
print("-" * 80)

# Look for repeating sequences in ciphertext (might indicate repeating key)
for block_size in range(2, 11):
    blocks = {}
    for i in range(0, len(cipher_bytes) - block_size + 1):
        block = cipher_bytes[i:i+block_size]
        if block in blocks:
            blocks[block].append(i)
        else:
            blocks[block] = [i]
    
    repeating = {k: v for k, v in blocks.items() if len(v) > 1}
    if repeating:
        print(f"Block size {block_size}: Found {len(repeating)} repeating sequences")
        for block, positions in list(repeating.items())[:3]:  # Show first 3
            distances = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
            print(f"  {block.hex()} at positions {positions}, distances: {distances}")

print("\n" + "=" * 80)
print("Analysis complete!")
