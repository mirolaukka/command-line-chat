import os
import socket
import threading


HOST = "127.0.0.1"
PORT = 8080

chat_history = []


def receive_messages(s):
    while True:
        message = s.recv(1024).decode()
        if message == 'exit':
            break
        chat_history.append(message)
        print_chat()


def print_chat():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console based on OS

    for chat_msg in chat_history:
        print(chat_msg)

    # Add the input prompt after printing the chat history
    print("\n> ", end="", flush=True)
        

def main():
    # Implement the logic to connect to the server and handle user input here
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        username = input("Enter your username: ")
        room = input("Enter the chatroom name: ")

        # Combine the username and room into a single string
        user_room = f"{username}|{room}"

        s.send(user_room.encode())

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


