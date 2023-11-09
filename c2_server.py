import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening for connections on {host}:{port}")

    executed_commands = []  # To store executed commands

    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    while True:
        command = input("Enter command: ")
        executed_commands.append(command)  # Add command to list

        if command == "exit":
            conn.sendall(command.encode())
            print("Executed commands:", " -> ".join(executed_commands))
            conn.close()
            break

        conn.sendall(command.encode())

        if command in ["pwd", "ls"] or command.startswith("cd "):
            output = conn.recv(1024).decode()
            print(f"Received: {output}")

if __name__ == "__main__":
    start_server("localhost", 9999)