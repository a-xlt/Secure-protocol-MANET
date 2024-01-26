import socket
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Authority import get_public_key

# Node configuration
node_number = 2
port = 8807
node_map = {1: 'node1', 4: 'node4'}

# Load the private key
with open("keys/0ed03cd0-25c6-4193-b2ef-4bec4fbd1ca5", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )


# ... [Rest of the functions like encrypt_message, decrypt_message]
def encrypt_message(message, public_key):
    """
    Encrypts a message using the provided public key.
    """
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_message(encrypted_message, private_key):
    """
    Decrypts a message using the provided private key.
    """
    return private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def send_file_to_node(filename, target_node):
    """
    Encrypts and sends a file to the specified target node.
    """
    # Load the target node's public key
    public_key_pem = get_public_key(target_node)
    public_key = serialization.load_pem_public_key(public_key_pem.encode())

    # Read and encrypt the file
    with open(filename, 'rb') as file:
        encrypted_data = encrypt_message(file.read(), public_key)

    # Create a client socket and connect to the target node
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))  # Assuming localhost for simplicity
    client_socket.sendall(encrypted_data)
    client_socket.close()

def receive_and_decrypt_file():
    """
    Receives an encrypted file and decrypts it using the node's private key.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()

    encrypted_data = client_socket.recv(1024)  # Assuming a small file for simplicity
    decrypted_data = decrypt_message(encrypted_data, private_key)

    with open('recvFile.txt', 'wb') as file:
        file.write(decrypted_data)

    client_socket.close()
    server_socket.close()

def route_message(target_node, filename):
    """
    Routes a message to the target node, possibly through intermediate nodes.
    """
    if target_node in node_map:
        send_file_to_node(filename, target_node)
    else:
        # Find an intermediate node to route the message
        for intermediate_node in node_map:
            # This is a very basic routing logic
            send_file_to_node(filename, intermediate_node)
            break  # In this simple example, we just pick the first intermediate node


# Example usage
if __name__ == "__main__":
    # Example: Route a file to node 3 (which is not directly connected)
    route_message(3, 'sample.txt')
