from cryptography.hazmat.primitives import serialization

# Load the SSH public key from file (assuming it's named 'bruce_rsa.pub')
with open('bruce_rsa.pub', 'r') as f:
    ssh_key_data = f.read().strip()

# Load the public key
public_key = serialization.load_ssh_public_key(ssh_key_data.encode())

# Extract the modulus n as a decimal integer
n = public_key.public_numbers().n

# Print n
print(n)