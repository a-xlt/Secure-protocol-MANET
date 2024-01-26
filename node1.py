import socket

Node_Table = [
    (2, 8807),
    (4, 8805)
]
node_port = 8808
node_host = '127.0.0.1'

node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = node_host
port = node_port
node_socket.bind((host, port))
node_socket.listen()
print(f"Server listening on {host}:{port}")
client_socket, client_address = node_socket.accept()
print(f"Accepted connection from {client_address}")
data = client_socket.recv(1024)
text_received = data.decode('utf-8')
print(f"Received text from client: {text_received}")
