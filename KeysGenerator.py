import sqlite3
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import uuid


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem, public_key_pem


def save_private_key(key, filename):
    with open('private_keys\\'+filename, 'wb') as f:
        f.write(key)


def save_public_key(key, filename):
    with open('public_keys\\'+filename, 'wb') as f:
        f.write(key)


def save_key_names_to_db(private_key_name, public_key_name, nodeNumber):
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()
    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS key_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            private_key_name TEXT,
            public_key_name TEXT,
            nodeNumber INTEGER
        )
    ''')
    # Insert the key names into the database
    cursor.execute('INSERT INTO key_pairs (private_key_name, public_key_name,nodeNumber) VALUES (?, ?,?)',
                   (private_key_name, public_key_name, nodeNumber))
    conn.commit()
    conn.close()


# Create keys
private_key, public_key = generate_key_pair()

publicGuid = str(uuid.uuid4())+'.pem'
privateGuid = str(uuid.uuid4())+'.pem'

# Save keys to files
nodeNumber = input("Enter Node number: ")
if nodeNumber.isdigit():
    save_private_key(private_key, privateGuid)
    save_public_key(public_key, publicGuid)
    save_key_names_to_db(privateGuid, publicGuid, nodeNumber)
else:
    try:
        number = int(nodeNumber)
    except ValueError:
        print("The input is not a node number.")




