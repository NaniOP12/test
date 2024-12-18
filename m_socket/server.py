import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

# List to store connected clients
clients = []

# Function to handle client communication
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[{client_address}] {message}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break
    
    # Remove client when disconnected
    print(f"[DISCONNECTED] {client_address} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

# Function to broadcast messages to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

# Main server function
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

# Start the server
if __name__ == "__main__":
    start_server()

