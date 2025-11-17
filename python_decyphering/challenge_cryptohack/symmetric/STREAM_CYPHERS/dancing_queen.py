"""
ChaCha20 cipher implementation with key recovery exploit
"""
from pwn import xor


def bytes_to_words(data):
    """Convert bytes to list of 32-bit little-endian words"""
    return [int.from_bytes(data[i:i+4], 'little') for i in range(0, len(data), 4)]


def words_to_bytes(words):
    """Convert list of 32-bit words to bytes in little-endian"""
    return b''.join([w.to_bytes(4, 'little') for w in words])


def rotate_left(value, n):
    """Rotate a 32-bit value left by n bits"""
    return ((value << n) & 0xffffffff) | ((value >> (32 - n)) & 0xffffffff)


def rotate_right(value, n):
    """Rotate a 32-bit value right by n bits"""
    return rotate_left(value, 32 - n)


def word32(value):
    """Keep value in 32-bit range"""
    return value % (2 ** 32)


class ChaCha20:
    """ChaCha20 stream cipher implementation with inverse operations for cryptanalysis"""
    
    # ChaCha20 constants: "expand 32-byte k"
    CONSTANTS = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    
    def __init__(self):
        self._state = []
        self._counter = 1

    def _quarter_round(self, state, a, b, c, d):
        """ChaCha20 quarter round operation"""
        state[a] = word32(state[a] + state[b])
        state[d] ^= state[a]
        state[d] = rotate_left(state[d], 16)
        
        state[c] = word32(state[c] + state[d])
        state[b] ^= state[c]
        state[b] = rotate_left(state[b], 12)
        
        state[a] = word32(state[a] + state[b])
        state[d] ^= state[a]
        state[d] = rotate_left(state[d], 8)
        
        state[c] = word32(state[c] + state[d])
        state[b] ^= state[c]
        state[b] = rotate_left(state[b], 7)

    def _quarter_round_inv(self, state, a, b, c, d):
        """Inverse of ChaCha20 quarter round for key recovery"""
        state[b] = rotate_right(state[b], 7)
        state[b] ^= state[c]
        state[c] = word32(state[c] - state[d])
        
        state[d] = rotate_right(state[d], 8)
        state[d] ^= state[a]
        state[a] = word32(state[a] - state[b])
        
        state[b] = rotate_right(state[b], 12)
        state[b] ^= state[c]
        state[c] = word32(state[c] - state[d])
        
        state[d] = rotate_right(state[d], 16)
        state[d] ^= state[a]
        state[a] = word32(state[a] - state[b])

    def _inner_block(self, state):
        """ChaCha20 double round (column + diagonal rounds)"""
        # Column rounds
        self._quarter_round(state, 0, 4, 8, 12)
        self._quarter_round(state, 1, 5, 9, 13)
        self._quarter_round(state, 2, 6, 10, 14)
        self._quarter_round(state, 3, 7, 11, 15)
        
        # Diagonal rounds
        self._quarter_round(state, 0, 5, 10, 15)
        self._quarter_round(state, 1, 6, 11, 12)
        self._quarter_round(state, 2, 7, 8, 13)
        self._quarter_round(state, 3, 4, 9, 14)

    def _inner_block_inv(self, state):
        """Inverse of ChaCha20 double round"""
        # Reverse diagonal rounds
        self._quarter_round_inv(state, 3, 4, 9, 14)
        self._quarter_round_inv(state, 2, 7, 8, 13)
        self._quarter_round_inv(state, 1, 6, 11, 12)
        self._quarter_round_inv(state, 0, 5, 10, 15)
        
        # Reverse column rounds
        self._quarter_round_inv(state, 3, 7, 11, 15)
        self._quarter_round_inv(state, 2, 6, 10, 14)
        self._quarter_round_inv(state, 1, 5, 9, 13)
        self._quarter_round_inv(state, 0, 4, 8, 12)

    def _setup_state(self, key, iv):
        """Initialize ChaCha20 state matrix"""
        self._state = list(self.CONSTANTS)  # Constants
        self._state.extend(bytes_to_words(key))  # 256-bit key
        self._state.append(self._counter)  # Block counter
        self._state.extend(bytes_to_words(iv))  # 96-bit nonce

    def encrypt(self, plaintext, key, iv):
        """Encrypt plaintext using ChaCha20"""
        ciphertext = b''
        self._counter = 1

        for i in range(0, len(plaintext), 64):
            self._setup_state(key, iv)
            
            # Apply 10 double rounds (20 rounds total)
            for _ in range(10):
                self._inner_block(self._state)
            
            # XOR plaintext with keystream
            block = plaintext[i:i+64]
            keystream = words_to_bytes(self._state)
            ciphertext += xor(block, keystream)
            
            self._counter += 1
        
        return ciphertext

    def decrypt(self, ciphertext, key, iv):
        """Decrypt ciphertext using ChaCha20 (same as encrypt for stream cipher)"""
        return self.encrypt(ciphertext, key, iv)

    def recover_key(self, known_plaintext, ciphertext):
        """
        Recover the encryption key given a known plaintext-ciphertext pair.
        Requires at least 64 bytes of known plaintext from the first block.
        """
        if len(ciphertext) < 64 or len(known_plaintext) != len(ciphertext):
            raise ValueError("Need at least 64 bytes of matching plaintext and ciphertext")
        
        # XOR plaintext with ciphertext to get the keystream (state after rounds)
        keystream = xor(known_plaintext[:64], ciphertext[:64])
        self._state = bytes_to_words(keystream)
        
        print(f"Recovered keystream state: {self._state}")
        
        # Reverse the 10 double rounds
        for _ in range(10):
            self._inner_block_inv(self._state)
        
        # Verify constants
        if self._state[:4] != self.CONSTANTS:
            raise ValueError("Key recovery failed: invalid constants in state")
        
        # Verify counter is 1 (first block)
        if self._state[12] != 1:
            raise ValueError("Key recovery failed: invalid counter")
        
        # Extract key (words 4-11)
        key = words_to_bytes(self._state[4:12])
        return key


def main():
    """Exploit ChaCha20 key reuse to decrypt the flag"""
    
    # Known plaintext and its encryption
    known_plaintext = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
    plaintext_encrypted = bytes.fromhex(
        'f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c'
        '94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c21'
        '1ef5a52628094f09a30fc692cb25647f'
    )
    
    # Flag ciphertext (encrypted with same key, different IV)
    flag_encrypted = bytes.fromhex(
        'b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0f'
        'e622b32732'
    )
    
    # IVs/nonces used
    iv_plaintext = bytes.fromhex('e42758d6d218013ea63e3c49')
    iv_flag = bytes.fromhex('a99f9a7d097daabd2aa2a235')
    
    # Recover the key
    cipher = ChaCha20()
    print("Recovering encryption key...")
    key = cipher.recover_key(known_plaintext, plaintext_encrypted)
    print(f"Recovered key: {key.hex()}")
    
    # Decrypt the flag
    print("\nDecrypting flag...")
    flag = cipher.decrypt(flag_encrypted, key, iv_flag)
    
    print(f"\n{'='*60}")
    try:
        print(f"Flag: {flag.decode('utf-8')}")
    except UnicodeDecodeError:
        print(f"Flag (hex): {flag.hex()}")
        print(f"Flag (raw): {flag}")
        # Try different encodings
        for encoding in ['latin-1', 'ascii', 'cp1252']:
            try:
                decoded = flag.decode(encoding)
                print(f"Flag ({encoding}): {decoded}")
                break
            except:
                continue
    print(f"{'='*60}")


if __name__ == '__main__':
    main()