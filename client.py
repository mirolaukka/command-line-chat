import os
import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

chat_history = []


def receive_messages(s):
    """
    Receive messages from the server and display them to the user.

    :param s: The server socket.
    """
    try:
        while True:
            message = s.recv(1024).decode()
            if message == 'exit':
                break
            chat_history.append(message)
            print_chat()  # Print the updated chat history
    except (ConnectionResetError, ConnectionAbortedError):
        pass


def print_chat():
    """
    Print the entire chat history with newlines and clear the console based on the OS.
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console based on OS

    for chat_msg in chat_history:
        print(chat_msg)

    # Add the input prompt after printing the chat history
    print("\n> ", end="", flush=True)


def main():
    """
    Connect to the server and handle user input.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        username = input("Enter your username: ")
        s.send(username.encode())

        rooms_info = s.recv(1024).decode()
        print(rooms_info)  # Display the list of available rooms and user counts

        room = input("Enter room name: ")
        s.send(room.encode())

        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        receive_thread.start()

        while True:
            # Print the entire chat history with newlines
            message = input("\n\n> ")
            if message == 'exit':
                break

            s.send(message.encode())

        receive_thread.join()
        s.close()


if __name__ == '__main__':
    main()