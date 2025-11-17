"""
Utility functions for generating RSA keys and exporting them in various formats.
Supports PEM, DER, and SSH key formats.
"""
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime


def generate_rsa_keypair(key_size=2048, public_exponent=65537):
    """
    Generate a new RSA key pair.
    
    Args:
        key_size: Size of the key in bits (default: 2048)
        public_exponent: Public exponent e (default: 65537)
    
    Returns:
        tuple: (private_key, public_key) objects
    """
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_private_key_pem(private_key, filepath, password=None):
    """
    Save RSA private key to PEM format.
    
    Args:
        private_key: RSA private key object
        filepath: Path to save the PEM file
        password: Optional password to encrypt the key (bytes or None)
    """
    if password:
        encryption = serialization.BestAvailableEncryption(password)
    else:
        encryption = serialization.NoEncryption()
    
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=encryption
    )
    
    with open(filepath, 'wb') as f:
        f.write(pem)


def save_public_key_pem(public_key, filepath):
    """
    Save RSA public key to PEM format.
    
    Args:
        public_key: RSA public key object
        filepath: Path to save the PEM file
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open(filepath, 'wb') as f:
        f.write(pem)


def save_public_key_ssh(public_key, filepath, comment=b""):
    """
    Save RSA public key to SSH format.
    
    Args:
        public_key: RSA public key object
        filepath: Path to save the SSH public key file
        comment: Optional comment to append (bytes)
    """
    ssh = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )
    
    with open(filepath, 'wb') as f:
        f.write(ssh)
        if comment:
            f.write(b' ' + comment)


def create_rsa_key_from_parameters(n, e, d=None, p=None, q=None):
    """
    Create RSA key objects from raw parameters.
    
    Args:
        n: Modulus
        e: Public exponent
        d: Private exponent (optional, for private key)
        p: First prime factor (optional, for private key)
        q: Second prime factor (optional, for private key)
    
    Returns:
        RSA public key object, or private key object if d, p, q provided
    """
    from cryptography.hazmat.primitives.asymmetric import rsa
    
    public_numbers = rsa.RSAPublicNumbers(e, n)
    
    if d and p and q:
        # Calculate CRT parameters
        dmp1 = d % (p - 1)
        dmq1 = d % (q - 1)
        iqmp = pow(q, -1, p)
        
        private_numbers = rsa.RSAPrivateNumbers(
            p=p, q=q, d=d,
            dmp1=dmp1, dmq1=dmq1, iqmp=iqmp,
            public_numbers=public_numbers
        )
        return private_numbers.private_key(default_backend())
    else:
        return public_numbers.public_key(default_backend())


def generate_self_signed_cert(private_key, common_name="Test Certificate", days_valid=365):
    """
    Generate a self-signed x509 certificate.
    
    Args:
        private_key: RSA private key object
        common_name: Common name for the certificate
        days_valid: Number of days the certificate is valid
    
    Returns:
        x509.Certificate object
    """
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=days_valid)
    ).sign(private_key, None, default_backend())
    
    return cert


def save_cert_der(cert, filepath):
    """
    Save certificate to DER format.
    
    Args:
        cert: x509.Certificate object
        filepath: Path to save the DER file
    """
    der = cert.public_bytes(serialization.Encoding.DER)
    
    with open(filepath, 'wb') as f:
        f.write(der)


def save_cert_pem(cert, filepath):
    """
    Save certificate to PEM format.
    
    Args:
        cert: x509.Certificate object
        filepath: Path to save the PEM file
    """
    pem = cert.public_bytes(serialization.Encoding.PEM)
    
    with open(filepath, 'wb') as f:
        f.write(pem)


if __name__ == "__main__":
    # Example: Generate a new RSA key pair and save in various formats
    print("Generating RSA key pair (2048 bits)...")
    private_key, public_key = generate_rsa_keypair(2048)
    
    print("Saving keys...")
    save_private_key_pem(private_key, "test_private_key.pem")
    save_public_key_pem(public_key, "test_public_key.pem")
    save_public_key_ssh(public_key, "test_public_key.pub", b"test@example.com")
    
    print("Generating self-signed certificate...")
    cert = generate_self_signed_cert(private_key, "Test Certificate")
    save_cert_pem(cert, "test_cert.pem")
    save_cert_der(cert, "test_cert.der")
    
    print("Done! Generated files:")
    print("  - test_private_key.pem")
    print("  - test_public_key.pem")
    print("  - test_public_key.pub")
    print("  - test_cert.pem")
    print("  - test_cert.der")
