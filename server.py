import socket
import threading
import datetime

HOST = "127.0.0.1"
PORT = 8080

# Global dictionary to store active chat rooms and their clients
chat_rooms = {
    "general": {
        "messages": ["Welcome to room General!"],
        "users": []
    }
}

def handle_client(client_socket, address):
    """
    Function to handle a new client connection and manage the chat.

    :param client_socket: The client's socket.
    :param address: The client's address.
    """
    def get_timestamp():
        """Helper function to get the current timestamp in a specific format."""
        return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    try:
        # Implement the logic to handle a new client connection here
        # Receive the username from the client
        username = client_socket.recv(1024).decode()

        # Send available rooms to the client
        send_available_rooms(client_socket)

        # Receive the room name from the client
        room = client_socket.recv(1024).decode().lower()

        # Create a new room if it doesn't exist
        if room not in chat_rooms:
            chat_rooms[room] = {"messages": [f"Welcome to room {room.capitalize()}!"], "users": []}
        chat_rooms[room]["users"].append(client_socket)

        # Send the chat log history to the client immediately after joining
        send_chatlog(room, client_socket)

        # Notify other users that a new client has joined
        timestamp = get_timestamp()
        chat_rooms[room]['messages'].append(f'{timestamp} {username} has joined the chat!')
        broadcast_message(room, f'{timestamp} {username} has joined the chat!')

        while True:
            # Receive and broadcast messages from the client
            message = client_socket.recv(1024).decode()
            if message == 'exit':
                break
            timestamp = get_timestamp()
            chat_rooms[room]['messages'].append(f"{timestamp} {username}: {message}")
            broadcast_message(room, f"{timestamp} {username}: {message}")

    except (ConnectionResetError, ConnectionAbortedError):
        pass
    finally:
        # Remove the client socket from the chat-room upon disconnection
        if room in chat_rooms:
            chat_rooms[room]["users"].remove(client_socket)
            broadcast_message(room, f"{username} has left the chat.")
            client_socket.close()

def send_available_rooms(client_socket):
    """
    Send a message to the client with the list of available rooms and user counts.

    :param client_socket: The client's socket.
    """
    rooms_info_message = "Available Rooms:\n"
    for room, room_data in chat_rooms.items():
        user_count = len(room_data["users"])
        rooms_info_message += f"- {room.capitalize()} ({user_count} users)\n"

    # Send the message to the specified client
    client_socket.send(rooms_info_message.encode())

def send_chatlog(room, client):
    """
    Send the chat log history to the specified client.

    :param room: The room for which to send the chat log.
    :param client: The client's socket.
    """
    for message in chat_rooms[room]['messages']:
        try:
            # Append a newline character before sending
            client.send((message + '\n').encode())
        except (ConnectionResetError, ConnectionAbortedError):
            continue

def broadcast_message(room, message):
    """
    Broadcast a message to all clients in a specific chat room.

    :param room: The room in which to broadcast the message.
    :param message: The message to be broadcasted.
    """
    for client in chat_rooms[room]['users']:
        try:
            client.send(message.encode())
        except (ConnectionResetError, ConnectionAbortedError):
            continue

def start_server():
    """Function to start the chat server and listen for incoming connections."""
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