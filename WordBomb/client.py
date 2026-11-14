import socket
import threading

# Server IP address and port number
HOST = "127.0.0.1"  # Change to the server computer's IP if using separate laptops.
PORT = 5050


# Receive and display messages from the server
def receive_messages(client):
    try:
        with client.makefile("r", encoding="utf-8") as reader:
            for message in reader:
                print("\nServer:", message.strip(), flush=True)
    except (ConnectionError, OSError):
        pass


def main():
    # Create a TCP socket and connect to the server
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
    except OSError as error:
        print("Could not connect:", error)
        return

    with client:
        # Send the username to register with the server
        username = input("Enter username: ").strip()
        client.sendall(("JOIN|" + username + "\n").encode("utf-8"))

        # Start a background thread to receive server messages
        threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

        # Continuously accept and send user commands
        while True:
            try:
                command = input("Enter command (LIST or QUIT): ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                command = "QUIT"

            # Send the command to the server
            try:
                client.sendall((command + "\n").encode("utf-8"))
            except OSError:
                break

            # Exit the loop when the user chooses QUIT
            if command == "QUIT":
                break


# Run the client program
if __name__ == "__main__":
    main()

