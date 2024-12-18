import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 12345        # Server's port

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("[ERROR] Connection closed.")
            break

# Function to send messages to the server
def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

# Main client function
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("[CONNECTED] Connected to the server.")

    # Start threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

# Start the client
if __name__ == "__main__":
    start_client()

