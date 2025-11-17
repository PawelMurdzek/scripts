import requests
import json
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_session():
    """Create a session with retry strategy and SSL handling"""
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


def fetch_ciphertext(session, url, max_retries=3):
    """Fetch a single ciphertext with error handling"""
    for attempt in range(max_retries):
        try:
            r = session.get(url, timeout=10)
            r.raise_for_status()
            return r.json()['ciphertext']
        except requests.exceptions.SSLError:
            try:
                r = session.get(url, verify=False, timeout=10)
                r.raise_for_status()
                return r.json()['ciphertext']
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
    return None


def collect_ciphertexts(num_samples=100):
    """Collect unique ciphertexts from the server"""
    url = "https://aes.cryptohack.org/stream_consciousness/encrypt/"
    session = create_session()
    encryptions = []
    
    print(f"Collecting {num_samples} ciphertexts...")
    for i in range(num_samples):
        try:
            ct = fetch_ciphertext(session, url)
            if ct:
                encryptions.append(ct)
                if i % 10 == 0:
                    print(f"Progress: {i}/{num_samples}")
        except Exception as e:
            print(f"Error at iteration {i}: {e}")
            break
    
    # Remove duplicates and sort by length
    unique_encryptions = list(set(encryptions))
    unique_encryptions.sort(key=lambda x: len(x))
    
    print(f"Collected {len(unique_encryptions)} unique ciphertexts")
    return [bytes.fromhex(ct) for ct in unique_encryptions]


def bytewise_xor(m1, m2):
    """XOR two byte strings up to the length of the shorter one"""
    xor_len = min(len(m1), len(m2))
    return bytes([m1[i] ^ m2[i] for i in range(xor_len)])


def print_decryptions(encryptions, decryptions, text_no, crib):
    """Print all decryptions using the given crib"""
    print("\n" + "="*60)
    print(f"Testing crib: {crib} at position {text_no}")
    print("="*60)
    for i in range(len(encryptions)):
        try:
            decrypted = decryptions[i] + bytewise_xor(
                crib, 
                bytewise_xor(encryptions[i], encryptions[text_no])
            )
            print(f"{i:2d}: {decrypted}")
        except Exception as e:
            print(f"{i:2d}: [Error: {e}]")


def apply_crib(encryptions, decryptions, text_no, crib):
    """Apply a crib to all encryptions and update decryptions"""
    decryptions[text_no] += crib
    for i in range(len(encryptions)):
        if i != text_no:
            decryptions[i] += bytewise_xor(
                crib,
                bytewise_xor(encryptions[i], encryptions[text_no])
            )
    return [enc[len(crib):] for enc in encryptions]


def find_flag_position(encryptions, crib=b'crypto{'):
    """Find which ciphertext contains the flag"""
    for i in range(len(encryptions)):
        try:
            is_printable = all([
                bytewise_xor(crib, bytewise_xor(encryptions[i], encryptions[j]))
                .decode('utf-8', errors='ignore')
                .isprintable()
                for j in range(len(encryptions))
            ])
            if is_printable:
                return i
        except:
            continue
    return None


def interactive_mode(encryptions, decryptions):
    """Interactive mode for manual crib testing"""
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("="*60)
    print("Commands:")
    print("  test <text_no> <crib> - Test a crib without applying")
    print("  apply <text_no> <crib> - Apply a crib permanently")
    print("  show - Show current decryptions")
    print("  flag - Show only the flag line")
    print("  quit - Exit interactive mode")
    print("="*60)
    
    working_encryptions = encryptions.copy()
    working_decryptions = decryptions.copy()
    
    while True:
        try:
            cmd = input("\n> ").strip()
            
            if cmd == "quit":
                break
            elif cmd == "show":
                for i, dec in enumerate(working_decryptions):
                    print(f"{i:2d}: {dec}")
            elif cmd == "flag":
                for i, dec in enumerate(working_decryptions):
                    if b'crypto{' in dec:
                        print(f"{i:2d}: {dec}")
            elif cmd.startswith("test "):
                parts = cmd.split(" ", 2)
                if len(parts) < 3:
                    print("Usage: test <text_no> <crib>")
                    continue
                text_no = int(parts[1])
                crib = parts[2].encode()
                print_decryptions(working_encryptions, working_decryptions, text_no, crib)
            elif cmd.startswith("apply "):
                parts = cmd.split(" ", 2)
                if len(parts) < 3:
                    print("Usage: apply <text_no> <crib>")
                    continue
                text_no = int(parts[1])
                crib = parts[2].encode()
                working_encryptions = apply_crib(working_encryptions, working_decryptions, text_no, crib)
                print(f"Applied crib '{crib.decode()}' at position {text_no}")
                print("\nCurrent state:")
                for i, dec in enumerate(working_decryptions):
                    if b'crypto{' in dec or len(dec) > 0:
                        print(f"{i:2d}: {dec}")
            else:
                print("Unknown command")
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main cryptanalysis routine"""
    # Collect ciphertexts
    encryptions = collect_ciphertexts(100)
    
    if not encryptions:
        print("Failed to collect ciphertexts")
        return
    
    # Initialize decryptions
    decryptions = [b'' for _ in range(len(encryptions))]
    
    # Find and apply initial crib
    print("\nSearching for flag position...")
    crib = b'crypto{'
    text_no = find_flag_position(encryptions)
    
    if text_no is None:
        print("Could not find flag position")
        return
    
    print(f"Flag found at position {text_no}")
    encryptions = apply_crib(encryptions, decryptions, text_no, crib)
    
    print("\nInitial decryptions:")
    for i, dec in enumerate(decryptions):
        print(f"{i:2d}: {dec}")
    
    # Apply cribs from original working solution
    cribs_sequence = [
        (17, b'appy'),
        (18, b'bly'),
        (5, b'mell '),
        (7, b'hing '),
        (13, b'thing '),
        (19, b'ing ')
    ]
    
    for text_no, crib in cribs_sequence:
        try:
            print_decryptions(encryptions, decryptions, text_no, crib)
            encryptions = apply_crib(encryptions, decryptions, text_no, crib)
            print(f"\nApplied: {crib} at position {text_no}")
        except Exception as e:
            print(f"Skipped crib {crib}: {e}")
    
    print("\n" + "="*60)
    print("Current decryptions:")
    print("="*60)
    for i, dec in enumerate(decryptions):
        if len(dec) > 0:
            print(f"{i:2d}: {dec}")
    
    # Show flag
    print("\n" + "="*60)
    print("FLAG:")
    print("="*60)
    for i, dec in enumerate(decryptions):
        if b'crypto{' in dec:
            print(dec)
    
    # Enter interactive mode
    response = input("\nEnter interactive mode? (y/n): ").strip().lower()
    if response == 'y':
        interactive_mode(encryptions, decryptions)


if __name__ == "__main__":
    main()