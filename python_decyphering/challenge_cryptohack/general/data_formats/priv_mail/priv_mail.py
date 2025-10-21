from cryptography.hazmat.primitives import serialization

# Load the PEM file
with open('privacy_enhanced_mail.pem', 'rb') as f:
    pem_data = f.read()

# Load the private key
private_key = serialization.load_pem_private_key(pem_data, password=None)

# Extract the private exponent d
d = private_key.private_numbers().d

# Print d as a decimal integer
print(d)
