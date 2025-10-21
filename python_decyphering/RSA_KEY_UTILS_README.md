# RSA Key Utilities

This module provides utilities for working with RSA keys in various formats.

## Installation

These utilities require the `cryptography` library:

```bash
pip install cryptography
```

## Deciphering Module (`python_decyphering/rsa_key_utils.py`)

Extract RSA key parameters from various formats:

### Functions

- `extract_private_exponent_from_pem(filepath, password=None)` - Extract private exponent `d` from PEM private key
- `extract_modulus_from_pem_public(filepath)` - Extract modulus `n` from PEM public key
- `extract_modulus_from_der_cert(filepath)` - Extract modulus `n` from DER certificate
- `extract_modulus_from_ssh_public(filepath)` - Extract modulus `n` from SSH public key
- `get_rsa_private_numbers(filepath, password=None)` - Extract all private key components (n, e, d, p, q, dmp1, dmq1, iqmp)
- `get_rsa_public_numbers(filepath, key_format='pem')` - Extract public key components (n, e)

### Usage Examples

```python
from rsa_key_utils import extract_private_exponent_from_pem, get_rsa_public_numbers

# Extract d from private key
d = extract_private_exponent_from_pem('private_key.pem')
print(f"Private exponent d: {d}")

# Get n and e from SSH public key
pub_nums = get_rsa_public_numbers('id_rsa.pub', key_format='ssh')
print(f"Modulus n: {pub_nums['n']}")
print(f"Public exponent e: {pub_nums['e']}")

# Get all components from private key
all_nums = get_rsa_private_numbers('private_key.pem')
print(f"p: {all_nums['p']}")
print(f"q: {all_nums['q']}")
```

## Ciphering Module (`python_cyphering/rsa_key_generator.py`)

Generate and export RSA keys in various formats:

### Functions

- `generate_rsa_keypair(key_size=2048, public_exponent=65537)` - Generate new RSA key pair
- `save_private_key_pem(private_key, filepath, password=None)` - Save private key to PEM
- `save_public_key_pem(public_key, filepath)` - Save public key to PEM
- `save_public_key_ssh(public_key, filepath, comment=b"")` - Save public key to SSH format
- `create_rsa_key_from_parameters(n, e, d=None, p=None, q=None)` - Create key from raw parameters
- `generate_self_signed_cert(private_key, common_name="Test", days_valid=365)` - Generate x509 certificate
- `save_cert_der(cert, filepath)` - Save certificate to DER format
- `save_cert_pem(cert, filepath)` - Save certificate to PEM format

### Usage Examples

```python
from rsa_key_generator import generate_rsa_keypair, save_private_key_pem, save_public_key_pem

# Generate a new key pair
private_key, public_key = generate_rsa_keypair(key_size=2048)

# Save keys
save_private_key_pem(private_key, 'my_private_key.pem')
save_public_key_pem(public_key, 'my_public_key.pem')

# Create key from known parameters
from rsa_key_generator import create_rsa_key_from_parameters

# If you only have n and e (public key)
public_key = create_rsa_key_from_parameters(n=12345..., e=65537)

# If you have all parameters (private key)
private_key = create_rsa_key_from_parameters(n=12345..., e=65537, d=98765..., p=111..., q=222...)
```

## Command-line Usage

Both modules can be run directly:

```bash
# Extract parameters from a key file
python rsa_key_utils.py path/to/key_file.pem

# Generate test keys and certificates
python rsa_key_generator.py
```
