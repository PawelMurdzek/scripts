from Crypto.Cipher import AES
from Crypto.Util import Counter
import zlib
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import ssl
import urllib3

# Disable SSL warnings (use with caution)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_{}0123456789abcdefghijklmnopqrstuvwxyz"

def create_session():
    """Create a session with retry strategy and SSL handling"""
    session = requests.Session()
    
    # Configure retry strategy
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

# Create global session
session = create_session()

def encrypt(plaintext, retry_count=3):
    """Encrypt with error handling and retries"""
    url = f'https://aes.cryptohack.org/ctrime/encrypt/{plaintext.hex()}/'
    
    for attempt in range(retry_count):
        try:
            # Try with SSL verification first
            r = session.get(url, timeout=10)
            r.raise_for_status()
            return r.json()['ciphertext']
        except requests.exceptions.SSLError:
            # If SSL error, try without verification
            try:
                r = session.get(url, verify=False, timeout=10)
                r.raise_for_status()
                return r.json()['ciphertext']
            except Exception as e:
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise Exception(f"Failed after {retry_count} attempts: {str(e)}")
        except requests.exceptions.RequestException as e:
            if attempt < retry_count - 1:
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)
                continue
            else:
                raise Exception(f"Failed after {retry_count} attempts: {str(e)}")
    
    raise Exception("Unexpected error in encrypt function")

def main():
    flag = b"crypto{"
    last_chr = b""
    
    print(f"Starting flag extraction...")
    print(f"Initial flag: {flag.decode()}")
    
    while last_chr != b"}":
        try:
            # Get baseline length
            send = flag + b"*"
            out = encrypt(send * 2)
            baseline_len = len(out)
            
            found = False
            for c in alpha:
                send = flag + c.encode()
                out2 = encrypt(send * 2)
                
                # If compressed length is shorter, we found the right character
                if len(out2) < baseline_len:
                    flag += c.encode()
                    last_chr = c.encode()
                    print(f"Found: {flag.decode()}")
                    found = True
                    break
            
            if not found:
                print(f"Warning: No character found for position {len(flag)}")
                break
                
        except KeyboardInterrupt:
            print(f"\nInterrupted. Current flag: {flag.decode()}")
            break
        except Exception as e:
            print(f"\nError occurred: {e}")
            print(f"Current flag: {flag.decode()}")
            raise
    
    print(f"\n{'='*50}")
    print(f"Final flag: {flag.decode()}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()