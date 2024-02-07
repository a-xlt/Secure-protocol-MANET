import socket
import threading
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from Authority import get_public_key

node_number = 1
node_map = {2: 8807, 4: 8805}
portNum = 8808
with open("keys/9486bd9b-d591-4c52-acf0-3fc214c61611.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )


def encrypt_message(message, public_keyd):
    encrypted_message = public_keyd.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message


def decrypt_message(encrypted_message):
    original_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message


def send_file_to_node(filename, target_node):
    public_key_pem = get_public_key(int(target_node))
    with open(f'keys/{public_key_pem}.pem', 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    exec(f"from node{target_node} import receive_and_decrypt_file as xNode")
    exec(f'my_thread =threading.Thread(target=xNode)')
    exec('my_thread.start()')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', node_map[target_node]))

    with open(filename, 'rb') as file:
        while True:
            bytes_read = file.read(2047)
            if not bytes_read:
                break
            encrypted_data = encrypt_message(bytes_read, public_key)
            client_socket.sendall(encrypted_data)

    client_socket.close()


def receive_and_decrypt_file():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', portNum))
    server_socket.listen(1)
    client_socket, addr = server_socket.accept()

    with open('recvFile.txt', 'a') as file:
        while True:
            encrypted_data = client_socket.recv(2047)
            if not encrypted_data:
                break
            decrypted_datab = decrypt_message(encrypted_data)
            decrypted_data = repr(decrypted_datab)
            decrypted_data = decrypted_data[:-1]
            decrypted_data = decrypted_data.replace('b\'', '')
            file.write(decrypted_data)

    client_socket.close()
    server_socket.close()


def route_message():
    target_node = int(input('Enter receiver Node Number: '))
    filename = (input('Enter File Name: '))
    if target_node in node_map:
        send_file_to_node(filename, target_node)
    else:
        for intermediate_node in node_map:
            send_file_to_node(filename, intermediate_node)
            break

# CreateByA-XLT
