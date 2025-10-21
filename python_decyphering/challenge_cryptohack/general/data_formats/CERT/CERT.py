from cryptography import x509

with open('2048b-rsa-example-cert.der', 'rb') as f:
    der_data = f.read()

# Load the DER-encoded certificate
cert = x509.load_der_x509_certificate(der_data)

# Extract the public key (assuming RSA)
public_key = cert.public_key()

# Get the modulus n as a decimal integer
n = public_key.public_numbers().n

# Print n
print(n)