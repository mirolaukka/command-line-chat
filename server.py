import socket
import threading
import datetime

HOST = "127.0.0.1"
PORT = 8080

# Global dictionary to store active chat rooms and their clients
chat_rooms = {
    "general": {
        "messages": [],
        "users": []
    }
}

def handle_client(client_socket, address):

    def get_timestamp():
        # Helper function to get the current timestamp
        return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    # Implement the logic to handle a new client connection here
    user_room = client_socket.recv(1024).decode()

    # Separate the username and room using the delimiter '|'
    username, room = user_room.split('|')
    print(username, room)
    room = room.lower()

    if room not in chat_rooms:
        chat_rooms[room] = {"messages": [f"Welcome to room {room.capitalize()}"], "users": []}
    chat_rooms[room]["users"].append(client_socket)

    # Send the chat log history to the client immediately after joining
    send_chatlog(room, client_socket)
    timestamp = get_timestamp()
    chat_rooms[room]['messages'].append(f'{timestamp} {username} has joined the chat!')
    broadcast_message(room, f'{timestamp} {username} has joined the chat!')
    while True:
        try:
            # Receive and broadcast messages from the client
            message = client_socket.recv(1024).decode()
            if message == 'exit':
                break
            timestamp = get_timestamp()
            chat_rooms[room]['messages'].append(f"{timestamp} {username}: {message}")
            broadcast_message(room, f"{timestamp} {username}: {message}")
        except:
            break

    # Remove the client socket from the chat-room upon disconnection
    chat_rooms[room]["users"].remove(client_socket)
    broadcast_message(room, f"{username} has left the chat.")
    client_socket.close()

def send_chatlog(room, client):
    for message in chat_rooms[room]['messages']:
        try:
            client.send((message + '\n').encode())  # Append a newline character before sending
        except:
            continue

def broadcast_message(room, message):
    for client in chat_rooms[room]['users']:
        try:
            client.send(message.encode())
        except:
            continue

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print("[INFO] Server started. Listening for connections...")

    try:
        while True:
            client_socket, address = server_socket.accept()
            # Implement the logic to handle the new client connection here
            print(address, "Connected")
            new_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            new_thread.start()
    except KeyboardInterrupt:
        print("[INFO] Server shutdown requested.")
    finally:
        server_socket.close()

    


if __name__ == '__main__':
    start_server()