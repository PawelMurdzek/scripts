"""
Utility functions for extracting RSA key parameters from various formats.
Supports PEM, DER, and SSH key formats.
"""
from cryptography.hazmat.primitives import serialization
from cryptography import x509


def extract_private_exponent_from_pem(filepath, password=None):
    """
    Extract private exponent d from PEM-formatted RSA private key.
    
    Args:
        filepath: Path to the PEM file
        password: Optional password for encrypted keys (bytes or None)
    
    Returns:
        int: The private exponent d as a decimal integer
    """
    with open(filepath, 'rb') as f:
        pem_data = f.read()
    
    private_key = serialization.load_pem_private_key(pem_data, password=password)
    return private_key.private_numbers().d


def extract_modulus_from_pem_public(filepath):
    """
    Extract modulus n from PEM-formatted RSA public key.
    
    Args:
        filepath: Path to the PEM public key file
    
    Returns:
        int: The modulus n as a decimal integer
    """
    with open(filepath, 'rb') as f:
        pem_data = f.read()
    
    public_key = serialization.load_pem_public_key(pem_data)
    return public_key.public_numbers().n


def extract_modulus_from_der_cert(filepath):
    """
    Extract modulus n from DER-encoded x509 certificate.
    
    Args:
        filepath: Path to the DER certificate file
    
    Returns:
        int: The modulus n as a decimal integer
    """
    with open(filepath, 'rb') as f:
        der_data = f.read()
    
    cert = x509.load_der_x509_certificate(der_data)
    public_key = cert.public_key()
    return public_key.public_numbers().n


def extract_modulus_from_ssh_public(filepath):
    """
    Extract modulus n from SSH public key format.
    
    Args:
        filepath: Path to the SSH public key file
    
    Returns:
        int: The modulus n as a decimal integer
    """
    with open(filepath, 'r') as f:
        ssh_key_data = f.read().strip()
    
    public_key = serialization.load_ssh_public_key(ssh_key_data.encode())
    return public_key.public_numbers().n


def get_rsa_private_numbers(filepath, password=None):
    """
    Extract all RSA private key components from PEM file.
    
    Args:
        filepath: Path to the PEM private key file
        password: Optional password for encrypted keys (bytes or None)
    
    Returns:
        dict: Dictionary containing n, e, d, p, q, dmp1, dmq1, iqmp
    """
    with open(filepath, 'rb') as f:
        pem_data = f.read()
    
    private_key = serialization.load_pem_private_key(pem_data, password=password)
    private_nums = private_key.private_numbers()
    
    return {
        'n': private_nums.public_numbers.n,
        'e': private_nums.public_numbers.e,
        'd': private_nums.d,
        'p': private_nums.p,
        'q': private_nums.q,
        'dmp1': private_nums.dmp1,  # d mod (p-1)
        'dmq1': private_nums.dmq1,  # d mod (q-1)
        'iqmp': private_nums.iqmp   # q^-1 mod p
    }


def get_rsa_public_numbers(filepath, key_format='pem'):
    """
    Extract RSA public key components (n, e) from various formats.
    
    Args:
        filepath: Path to the key file
        key_format: 'pem', 'ssh', or 'der_cert'
    
    Returns:
        dict: Dictionary containing n and e
    """
    if key_format == 'pem':
        with open(filepath, 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())
    elif key_format == 'ssh':
        with open(filepath, 'r') as f:
            public_key = serialization.load_ssh_public_key(f.read().strip().encode())
    elif key_format == 'der_cert':
        with open(filepath, 'rb') as f:
            cert = x509.load_der_x509_certificate(f.read())
            public_key = cert.public_key()
    else:
        raise ValueError(f"Unsupported format: {key_format}. Use 'pem', 'ssh', or 'der_cert'.")
    
    public_nums = public_key.public_numbers()
    return {
        'n': public_nums.n,
        'e': public_nums.e
    }


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python rsa_key_utils.py <path_to_key_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    try:
        # Try to extract as private key
        d = extract_private_exponent_from_pem(filepath)
        print(f"Private exponent d: {d}")
        
        # Get all private numbers
        nums = get_rsa_private_numbers(filepath)
        print(f"\nAll private key components:")
        for key, value in nums.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Not a private key or error: {e}")
        
        # Try as public key
        try:
            n = extract_modulus_from_pem_public(filepath)
            print(f"Modulus n: {n}")
        except Exception as e2:
            print(f"Error reading as public key: {e2}")
