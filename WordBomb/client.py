import socket
import threading

HOST = "127.0.0.1"  # Change to the server computer's IP if using separate laptops.
PORT = 5050


def receive_messages(client):
    try:
        with client.makefile("r", encoding="utf-8") as reader:
            for message in reader:
                print("\nServer:", message.strip(), flush=True)
    except (ConnectionError, OSError):
        pass


def main():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
    except OSError as error:
        print("Could not connect:", error)
        return

    with client:
        username = input("Enter username: ").strip()
        client.sendall(("JOIN|" + username + "\n").encode("utf-8"))
        threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
        while True:
            try:
                command = input("Enter command (LIST or QUIT): ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                command = "QUIT"
            try:
                client.sendall((command + "\n").encode("utf-8"))
            except OSError:
                break
            if command == "QUIT":
                break


if __name__ == "__main__":
    main()
