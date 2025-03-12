import bcrypt

# Function to hash a password
def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# List of plaintext passwords
plaintext_passwords = [
    '299792458', '2.718281828', '3.141592654', 
    '1.414213562', 'Inuke', 'Silvernuke', 'Jieru'
]

# Generate hashes for the passwords
valid_credentials_hashes = [hash_password(pwd) for pwd in plaintext_passwords]

# Print the hashes
for pwd, hashed in zip(plaintext_passwords, valid_credentials_hashes):
    print(f"Password: {pwd} -> Hash: {hashed}")

for hashed in valid_credentials_hashes:
    print(hashed)