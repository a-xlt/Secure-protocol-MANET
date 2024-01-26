import os
import sqlite3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import uuid


# Function to generate keys
def generate_keys():
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Generate public key
    public_key = private_key.public_key()

    public_guid = str(uuid.uuid4())
    private_guid = str(uuid.uuid4())
    with open(f"keys/{private_guid}.pem", "wb") as priv_file:
        priv_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open(f"keys/{public_guid}.pem", "wb") as pub_file:
        pub_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    return private_guid, public_guid


# Function to save keys to database
def save_keys_to_db(node_number, private_key, public_key):
    # Connect to the SQLite database
    conn = sqlite3.connect('node_keys.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS keys 
                   (node_number INTEGER PRIMARY KEY, private_key TEXT, public_key TEXT)''')

    # Insert keys into the database
    cursor.execute('''INSERT INTO keys (node_number, private_key, public_key) 
                   VALUES (?, ?, ?)''', (node_number, private_key, public_key))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Ensure the 'keys' directory exists
    if not os.path.exists('keys'):
        os.makedirs('keys')

    # Get node number from user
    node_number = int(input("Enter the node number: "))

    # Generate and save keys
    private_key, public_key = generate_keys()

    # Save keys to the database
    save_keys_to_db(node_number, private_key, public_key)
