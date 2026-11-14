
import socket
import threading

# Server IP and port
HOST = "0.0.0.0"
PORT = 5050

players = []  # Stores the names of connected players
lock = threading.Lock()  # Prevents multiple threads from changing the list at the same time


# Handles communication with each connected client
def handle_client(conn, addr):
    username = None
    print("Connected:", addr, flush=True)

    try:
        # Reads messages sent by the client
        with conn.makefile("r", encoding="utf-8") as reader:
            for line in reader:
                message = line.strip()

                # Handles a new player joining the server
                if message.startswith("JOIN|") and username is None:
                    name = message.split("|", 1)[1].strip()

                    with lock:
                        if not name or "|" in name:
                            response = "ERROR|BAD_MESSAGE"
                        elif name in players:
                            response = "ERROR|NAME_TAKEN"
                        else:
                            players.append(name)
                            username = name
                            response = "WELCOME|" + name

                        snapshot = players.copy()

                    # Sends the response back to the client
                    conn.sendall((response + "\n").encode("utf-8"))

                    if username:
                        print(username, "joined", flush=True)
                        print("Connected players:", snapshot, flush=True)
                        conn.sendall(b"WAITING\n")

                # Sends the current list of connected players
                elif message == "LIST" and username is not None:
                    with lock:
                        names = ",".join(players)

                    conn.sendall(("STATUS|waiting=" + names + "\n").encode("utf-8"))

                # Disconnects the client
                elif message == "QUIT":
                    break

                # Handles messages that are not recognized
                else:
                    conn.sendall(b"ERROR|BAD_MESSAGE\n")

    except (ConnectionError, OSError):
        pass

    finally:
        # Removes the player when they disconnect
        with lock:
            if username in players:
                players.remove(username)

        conn.close()
        print("Disconnected:", username, flush=True)


# Starts the server and waits for clients to connect
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Connects the server to the selected IP and port
        server.bind((HOST, PORT))
        server.listen()

        print("Word Bomb server running on port", PORT, flush=True)

        try:
            while True:
                # Accepts a new client connection
                conn, addr = server.accept()

                # Creates a separate thread for each client
                threading.Thread(
                    target=handle_client,
                    args=(conn, addr),
                    daemon=True
                ).start()

        except KeyboardInterrupt:
            print("\nServer stopped")


# Runs the server
if __name__ == "__main__":
    main()
