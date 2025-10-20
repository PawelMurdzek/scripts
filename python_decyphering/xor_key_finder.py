#!/usr/bin/env python3
"""
Comprehensive XOR Key Finder
Uses known-plaintext attack to find single-byte or repeating XOR keys.
"""

import sys


def repeating_key_xor(ciphertext_bytes, key_bytes):
    """Apply repeating key XOR to decrypt ciphertext."""
    if not key_bytes:
        return ciphertext_bytes
    decrypted_bytes = bytearray()
    for i in range(len(ciphertext_bytes)):
        decrypted_bytes.append(ciphertext_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return bytes(decrypted_bytes)


def find_single_byte_key(cipher_bytes, known_plain, verbose=True):
    """
    Try to find a single-byte XOR key using known plaintext.
    Returns list of (offset, key, decrypted_text) tuples.
    """
    results = []
    
    if verbose:
        print("\n" + "=" * 80)
        print("STEP 1: Testing Single-Byte XOR")
        print("=" * 80)
    
    for offset in range(len(cipher_bytes) - len(known_plain) + 1):
        potential_key_bytes = []
        for i in range(len(known_plain)):
            potential_key_bytes.append(cipher_bytes[offset + i] ^ ord(known_plain[i]))
        
        # Check if all bytes are the same (single-byte key)
        if len(set(potential_key_bytes)) == 1:
            key = potential_key_bytes[0]
            decrypted = bytes([b ^ key for b in cipher_bytes])
            
            try:
                decrypted_str = decrypted.decode('utf-8', errors='strict')
                if verbose:
                    print(f"! Found single-byte XOR key at offset {offset}!")
                    print(f"  Key: {key} (0x{key:02x}, ASCII: '{chr(key) if 32<=key<=126 else '?'}')")
                    print(f"  Decrypted: {decrypted_str}")
                    if known_plain in decrypted_str:
                        print(f"  !!! SUCCESS! Contains '{known_plain}' !!!")
                    print()
                
                results.append((offset, key, decrypted_str))
            except:
                pass
    
    if verbose and not results:
        print("No single-byte key found.")
    
    return results


def analyze_repeating_patterns(cipher_bytes, verbose=True):
    """
    Analyze ciphertext for repeating patterns to determine likely key length.
    Returns list of likely key lengths.
    """
    if verbose:
        print("\n" + "=" * 80)
        print("STEP 2: Analyzing Repeating Patterns")
        print("=" * 80)
    
    likely_key_lengths = set()
    
    # Look for repeating sequences in ciphertext
    for block_size in range(2, 11):
        blocks = {}
        for i in range(0, len(cipher_bytes) - block_size + 1):
            block = cipher_bytes[i:i+block_size]
            if block in blocks:
                blocks[block].append(i)
            else:
                blocks[block] = [i]
        
        repeating = {k: v for k, v in blocks.items() if len(v) > 1}
        if repeating and verbose:
            print(f"\nBlock size {block_size}: Found {len(repeating)} repeating sequences")
            for block, positions in list(repeating.items())[:2]:  # Show first 2
                distances = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
                print(f"  {block.hex()} at positions {positions}, distances: {distances}")
                
                # The distance between repeating patterns likely relates to key length
                for dist in distances:
                    # Key length is likely a divisor of the distance
                    for divisor in range(1, min(dist + 1, 21)):
                        if dist % divisor == 0:
                            likely_key_lengths.add(divisor)
    
    # Sort and return most likely lengths (prioritize common lengths)
    sorted_lengths = sorted(likely_key_lengths)
    if verbose:
        print(f"\nLikely key lengths based on patterns: {sorted_lengths[:10]}")
    
    return sorted_lengths


def find_repeating_key(cipher_bytes, known_plain, max_key_length=20, verbose=True):
    """
    Try to find a repeating XOR key using known plaintext.
    Returns list of (key_length, key, decrypted_text) tuples.
    """
    if verbose:
        print("\n" + "=" * 80)
        print("STEP 3: Finding Repeating Key")
        print("=" * 80)
    
    # Extract potential key bytes from known plaintext at position 0
    partial_key = bytes([cipher_bytes[i] ^ ord(known_plain[i]) 
                        for i in range(min(len(known_plain), len(cipher_bytes)))])
    
    if verbose:
        print(f"\nPartial key from '{known_plain}' at position 0:")
        print(f"  Hex: {partial_key.hex()}")
        print(f"  String: '{partial_key.decode('utf-8', errors='ignore')}'")
        print(f"  Bytes: {list(partial_key)}")
        print(f"\nTesting different key lengths (1-{max_key_length})...")
        print("-" * 80)
    
    results = []
    
    for key_len in range(1, max_key_length + 1):
        # Use the first key_len bytes as the repeating key
        test_key = partial_key[:key_len]
        decrypted = repeating_key_xor(cipher_bytes, test_key)
        
        try:
            decrypted_str = decrypted.decode('utf-8', errors='strict')
            
            # Check if it contains the known plaintext
            if known_plain in decrypted_str:
                # Calculate how "readable" it is
                printable_count = sum(1 for c in decrypted_str if c.isprintable())
                printable_ratio = printable_count / len(decrypted_str)
                
                if verbose:
                    print(f"! Key length {key_len} - VALID!")
                    print(f"  Key (hex): {test_key.hex()}")
                    print(f"  Key (str): '{test_key.decode('utf-8', errors='ignore')}'")
                    print(f"  Decrypted: {decrypted_str}")
                    print(f"  Printable: {printable_count}/{len(decrypted_str)} ({100*printable_ratio:.1f}%)")
                    
                    if decrypted_str.strip().endswith('}'):
                        print(f"  !!! COMPLETE MESSAGE (ends with '}}') !!!")
                    print()
                
                results.append((key_len, test_key, decrypted_str))
        except:
            pass
    
    return results


def try_common_variations(cipher_bytes, partial_key, verbose=True):
    """
    Try common variations of the partial key to find the complete key.
    """
    if verbose:
        print("\n" + "=" * 80)
        print("STEP 4: Trying Common Key Variations")
        print("=" * 80)
    
    partial_str = partial_key.decode('utf-8', errors='ignore')
    
    # Generate common variations
    variations = []
    
    # If partial key is like "myXORke", try adding common endings
    if len(partial_key) >= 4:
        variations.extend([
            partial_key + b'y',
            partial_key + b'Y',
            partial_key + b'!',
            partial_key + b'3y',
            partial_key + b'r',
            partial_key + b'd',
        ])
    
    # Try variations with case changes
    try:
        variations.extend([
            partial_str.upper().encode('utf-8'),
            partial_str.lower().encode('utf-8'),
            partial_str.capitalize().encode('utf-8'),
        ])
    except:
        pass
    
    if verbose:
        print(f"Testing {len(set(variations))} variations based on partial key '{partial_str}'...")
        print("-" * 80)
    
    results = []
    
    for test_key in set(variations):
        decrypted = repeating_key_xor(cipher_bytes, test_key)
        try:
            decrypted_str = decrypted.decode('utf-8', errors='strict')
            
            # Check if it looks valid
            printable_count = sum(1 for c in decrypted_str if c.isprintable())
            printable_ratio = printable_count / len(decrypted_str)
            
            # Calculate score: prefer complete messages with high printability
            score = printable_ratio
            if decrypted_str.strip().endswith('}'):
                score += 0.5  # Bonus for complete message
            
            if printable_ratio > 0.9:  # At least 90% printable
                if verbose:
                    print(f"\n! Key: '{test_key.decode('utf-8', errors='ignore')}' ({test_key.hex()})")
                    print(f"  Decrypted: {decrypted_str}")
                    if decrypted_str.strip().endswith('}'):
                        print(f"  !!! COMPLETE! Ends with '}}' !!!")
                
                results.append((test_key, decrypted_str, score))
        except:
            pass
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x[2], reverse=True)
    
    return results


def main():
    print("=" * 80)
    print("XOR KEY FINDER - Known Plaintext Attack")
    print("=" * 80)
    print()
    
    # Get input from user
    hex_cipher = input("Enter the ciphertext (in hex format): ").strip()
    
    try:
        cipher_bytes = bytes.fromhex(hex_cipher)
    except ValueError:
        print("Error: Invalid hex string.")
        return
    
    known_plain = input("Enter the known plaintext (e.g., 'crypto{'): ").strip()
    
    if not known_plain:
        print("Error: Known plaintext cannot be empty.")
        return
    
    print(f"\nCiphertext length: {len(cipher_bytes)} bytes")
    print(f"Known plaintext: '{known_plain}'")
    
    # Step 1: Try single-byte XOR
    single_results = find_single_byte_key(cipher_bytes, known_plain)
    
    if single_results:
        print("\n" + "=" * 80)
        print("SINGLE-BYTE KEY FOUND!")
        print("=" * 80)
        for offset, key, decrypted in single_results[:3]:  # Show top 3
            print(f"Key: {key} (0x{key:02x})")
            print(f"Decrypted: {decrypted}")
            print()
        return
    
    # Step 2: Analyze patterns
    likely_lengths = analyze_repeating_patterns(cipher_bytes)
    
    # Step 3: Try repeating key
    repeating_results = find_repeating_key(cipher_bytes, known_plain, max_key_length=20)
    
    if repeating_results:
        # Find the most likely key (shortest that gives valid result)
        best_result = min(repeating_results, key=lambda x: x[0])  # Shortest key
        key_len, key, decrypted = best_result
        
        # Step 4: Try variations if the key seems incomplete
        if len(key) >= 4 and not decrypted.strip().endswith('}'):
            variation_results = try_common_variations(cipher_bytes, key)
            
            if variation_results:
                print("\n" + "=" * 80)
                print("BEST RESULT FROM VARIATIONS")
                print("=" * 80)
                best_var_key, best_var_decrypted, best_score = variation_results[0]
                print(f"Key: '{best_var_key.decode('utf-8', errors='ignore')}' ({best_var_key.hex()})")
                print(f"Key length: {len(best_var_key)} bytes")
                print(f"Decrypted: {best_var_decrypted}")
                return
        
        print("\n" + "=" * 80)
        print("BEST RESULT")
        print("=" * 80)
        print(f"Key: '{key.decode('utf-8', errors='ignore')}' ({key.hex()})")
        print(f"Key length: {key_len} bytes")
        print(f"Decrypted: {decrypted}")
    else:
        # Try variations with just the partial key
        partial_key = bytes([cipher_bytes[i] ^ ord(known_plain[i]) 
                            for i in range(min(len(known_plain), len(cipher_bytes)))])
        variation_results = try_common_variations(cipher_bytes, partial_key)
        
        if variation_results:
            print("\n" + "=" * 80)
            print("RESULTS FROM KEY VARIATIONS")
            print("=" * 80)
            for key, decrypted in variation_results[:3]:
                print(f"Key: '{key.decode('utf-8', errors='ignore')}' ({key.hex()})")
                print(f"Decrypted: {decrypted}")
                print()
        else:
            print("\n" + "=" * 80)
            print("NO VALID KEY FOUND")
            print("=" * 80)
            print("The known plaintext might be incorrect or at a different position.")


if __name__ == "__main__":
    main()
