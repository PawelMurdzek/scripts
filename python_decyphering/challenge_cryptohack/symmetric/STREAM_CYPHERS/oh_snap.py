"""
RC4 Partial Key Attack - Flag recovery through statistical analysis
Exploits weak RC4 initialization with long keys to recover the flag byte-by-byte
"""
from random import randrange
import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
NUM_SAMPLES = 120  # Number of nonce samples to collect
KEYSTREAM_LENGTH = 32  # Bytes of keystream to analyze
FLAG_LENGTH = 34  # Expected flag length
NONCE_LENGTH = 256 - FLAG_LENGTH


def create_session():
    """Create a session with retry strategy"""
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def partial_rc4_keystream(partial_key, num_keystream_bytes):
    """
    Generate approximate RC4 keystream from a partial key.
    
    This simulates RC4's Key Scheduling Algorithm (KSA) and Pseudo-Random
    Generation Algorithm (PRGA) with incomplete information. Unknown values
    are marked as -1.
    
    Args:
        partial_key: List of key bytes (known prefix of the full RC4 key)
        num_keystream_bytes: Number of keystream bytes to generate
    
    Returns:
        List of approximated keystream bytes (-1 for unknown values)
    """
    # Initialize permutation array
    state = list(range(256))
    
    # Key Scheduling Algorithm (KSA) - partial execution
    j = 0
    for i in range(len(partial_key)):
        j = (j + state[i] + partial_key[i]) & 0xff
        state[i], state[j] = state[j], state[i]
    
    # Mark unknown positions
    for i in range(len(partial_key), 256):
        state[i] = -1
    
    # Pseudo-Random Generation Algorithm (PRGA) - approximated
    keystream = []
    j = 0
    
    for i in range(1, num_keystream_bytes + 1):
        # Can't proceed if state value is unknown
        if state[i] < 0:
            break
        
        j = (j + state[i]) & 0xff
        state[i], state[j] = state[j], state[i]
        
        # Handle unknown values during keystream generation
        if state[j] < 0:
            keystream.append(-1)
        else:
            sum_index = (state[i] + state[j]) & 0xff
            if state[sum_index] < 0:
                keystream.append(-1)
            else:
                keystream.append(state[sum_index])
    
    return keystream


def fetch_keystream_sample(session, nonce, num_bytes, max_retries=3):
    """
    Fetch a keystream sample from the server
    
    Args:
        session: Requests session
        nonce: Nonce bytes to use
        num_bytes: Number of zero bytes to encrypt
        max_retries: Maximum retry attempts
    
    Returns:
        List of keystream bytes
    """
    url = f"http://aes.cryptohack.org/oh_snap/send_cmd/{'00'*num_bytes}/{nonce.hex()}/"
    
    for attempt in range(max_retries):
        try:
            resp = session.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            # Extract keystream from error message
            keystream_hex = data['error'][17:]
            return list(bytes.fromhex(keystream_hex))
        except requests.exceptions.SSLError:
            try:
                resp = session.get(url, verify=False, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                keystream_hex = data['error'][17:]
                return list(bytes.fromhex(keystream_hex))
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
    
    raise Exception("Failed to fetch keystream sample")


def collect_samples(num_samples, nonce_length, keystream_length):
    """
    Collect multiple nonce-keystream pairs from the server
    
    Args:
        num_samples: Number of samples to collect
        nonce_length: Length of random nonce
        keystream_length: Length of keystream to capture
    
    Returns:
        Tuple of (nonces, keystreams)
    """
    print(f"Collecting {num_samples} samples...")
    session = create_session()
    nonces = []
    keystreams = []
    
    for i in range(num_samples):
        try:
            # Generate random nonce
            nonce = bytes([randrange(256) for _ in range(nonce_length)])
            nonces.append(list(nonce))
            
            # Fetch corresponding keystream
            keystream = fetch_keystream_sample(session, nonce, keystream_length)
            keystreams.append(keystream)
            
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i + 1}/{num_samples}")
        except Exception as e:
            print(f"  Error at sample {i + 1}: {e}")
            # Continue with remaining samples
            continue
    
    print(f"Collected {len(nonces)} samples successfully")
    return nonces, keystreams


def score_guess(nonces, keystreams, partial_flag, guess_byte, num_samples):
    """
    Score a guess for the next flag byte using statistical analysis
    
    Args:
        nonces: List of nonce samples
        keystreams: List of observed keystreams
        partial_flag: Known flag prefix
        guess_byte: Byte value to test
        num_samples: Number of samples to use
    
    Returns:
        Score (higher is better)
    """
    score = 0
    test_key = partial_flag + [guess_byte]
    
    for i in range(min(num_samples, len(nonces))):
        # Generate approximated keystream with this guess
        full_key = nonces[i] + test_key
        predicted_keystream = partial_rc4_keystream(full_key, KEYSTREAM_LENGTH)
        
        # Count matching bytes
        matches = sum(
            pred == actual 
            for pred, actual in zip(predicted_keystream, keystreams[i])
            if pred != -1
        )
        score += matches
    
    return score


def recover_flag(nonces, keystreams, initial_flag=b'crypto{'):
    """
    Recover the full flag byte-by-byte using statistical analysis
    
    Args:
        nonces: List of nonce samples
        keystreams: List of observed keystreams
        initial_flag: Known flag prefix
    
    Returns:
        Recovered flag as string
    """
    print("\nRecovering flag:")
    flag = list(initial_flag)
    num_samples = NUM_SAMPLES
    
    while len(flag) < FLAG_LENGTH:
        best_score = -1
        best_guess = 0
        
        # Try all printable ASCII characters
        for guess in range(32, 128):
            score = score_guess(nonces, keystreams, flag, guess, num_samples)
            
            if score > best_score:
                best_score = score
                best_guess = guess
        
        # Add the best guess to the flag
        flag.append(best_guess)
        current_flag = ''.join(chr(b) for b in flag)
        print(f"  {current_flag} (score: {best_score})")
        
        # Reduce sample size as we get more confident
        num_samples = max(10, num_samples - 2)
    
    return ''.join(chr(b) for b in flag)


def main():
    """Main attack routine"""
    print("="*60)
    print("RC4 Partial Key Attack")
    print("="*60)
    
    # Collect nonce-keystream pairs
    nonces, keystreams = collect_samples(NUM_SAMPLES, NONCE_LENGTH, KEYSTREAM_LENGTH)
    
    if len(nonces) < 10:
        print("Error: Not enough samples collected")
        return
    
    # Recover the flag
    flag = recover_flag(nonces, keystreams)
    
    print("\n" + "="*60)
    print(f"Final flag: {flag}")
    print("="*60)


if __name__ == "__main__":
    main() 