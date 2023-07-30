# Chat Room Server and Client

This is a simple chat room application that consists of a server (`server.py`) and a client (`client.py`) written in Python. The server allows multiple clients to connect and communicate with each other in different chat rooms.

## How to Run the Chat Room Application

### Requirements
- Python 3.x

### Running the Server
1. Open a terminal or command prompt.
2. Navigate to the directory containing `server.py`.
3. Execute the following command to start the server:

```bash
python server.py
```

The server will start running and listen for incoming connections.

### Running the Client
1. Open another terminal or command prompt (or a separate terminal window).
2. Navigate to the directory containing `client.py`.
3. Execute the following command to start the client:

```bash
python client.py
```

The client will prompt you to enter a username and the name of the chat room you want to join. Once connected, you can start chatting with other users in the room.

## How the Chat Room Application Works

### Server (`server.py`)
- The server listens for incoming connections on IP address `127.0.0.1` and port `8080`.
- Upon connection, the client sends its chosen username to the server.
- The server sends the list of available rooms and their user counts to the client.
- The client chooses a chat room and sends its name back to the server.
- If the chosen chat room doesn't exist, the server creates it.
- The server sends the chat log history of the chosen room to the client.
- Once connected, the client can send messages to the server, which will be broadcasted to all clients in the same chat room.
- If a client sends the message "exit," the server will remove the client from the chat room and close the connection.

### Client (`client.py`)
- The client connects to the server on IP address `127.0.0.1` and port `8080`.
- The user is prompted to enter a username.
- The client receives the list of available rooms and their user counts from the server and displays them to the user.
- The user is prompted to enter the name of the chat room they want to join.
- Once connected, the client starts a separate thread to receive and display messages from the server.
- The user can type messages and send them to the server, which will be broadcasted to all clients in the same chat room.
- If the user types "exit," the client will disconnect from the server and close the connection.


### Example
```
Welcome to room General!
[2023-07-30 15:00:00] Alice has joined the chat!
[2023-07-30 15:00:10] Bob has joined the chat!
[2023-07-30 15:00:05] Alice: Donec pulvinar erat.
[2023-07-30 15:00:10] Bob: Cras eu lectus.
[2023-07-30 15:00:10] Alice: Suspendisse feugiat sit amet nunc.
[2023-07-30 15:00:15] Bob: Pellentesque feugiat nulla ac magna faucibus tincidunt at sed.
> 
```

## Important Notes

- This is a basic chat room application designed for educational purposes and may not be suitable for production use.
- The server and client are both designed to run on the same machine (`127.0.0.1`). If you want to run them on different machines, you'll need to modify the `HOST` variable in both `server.py` and `client.py`.
- The application uses a simple text-based interface for interaction.
- The chat history on the client-side is stored in the `chat_history` list. When the client receives new messages from the server, it appends them to this list and displays the updated chat history.


## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues. Any feedback or suggestions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.