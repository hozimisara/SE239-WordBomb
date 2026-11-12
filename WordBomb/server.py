import socket
import threading

HOST = "0.0.0.0"
PORT = 5050
players = []
lock = threading.Lock()


def handle_client(conn, addr):
    username = None
    print("Connected:", addr, flush=True)
    try:
        with conn.makefile("r", encoding="utf-8") as reader:
            for line in reader:
                message = line.strip()
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
                    conn.sendall((response + "\n").encode("utf-8"))
                    if username:
                        print(username, "joined", flush=True)
                        print("Connected players:", snapshot, flush=True)
                        conn.sendall(b"WAITING\n")
                elif message == "LIST" and username is not None:
                    with lock:
                        names = ",".join(players)
                    conn.sendall(("STATUS|waiting=" + names + "\n").encode("utf-8"))
                elif message == "QUIT":
                    break
                else:
                    conn.sendall(b"ERROR|BAD_MESSAGE\n")
    except (ConnectionError, OSError):
        pass
    finally:
        with lock:
            if username in players:
                players.remove(username)
        conn.close()
        print("Disconnected:", username, flush=True)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print("Word Bomb server running on port", PORT, flush=True)
        try:
            while True:
                conn, addr = server.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServer stopped")


if __name__ == "__main__":
    main()
