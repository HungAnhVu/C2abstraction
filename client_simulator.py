import socket
import os

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")

    executed_commands = []  # To store executed commands

    while True:
        command = client_socket.recv(1024).decode()
        executed_commands.append(command)  # Add command to list

        if command == "exit":
            print("Exiting")
            print("Executed commands:", " -> ".join(executed_commands))
            break
        elif command == "pwd":
            pwd = os.getcwd()
            client_socket.sendall(pwd.encode())
        elif command == "ls":
            ls_output = "\n".join(os.listdir())
            client_socket.sendall(ls_output.encode())
        elif command.startswith("cd "):
            directory = command[3:]
            try:
                os.chdir(directory)
                client_socket.sendall(f"Changed directory to {os.getcwd()}".encode())
            except FileNotFoundError:
                client_socket.sendall("Directory not found".encode())

if __name__ == "__main__":
    start_client("localhost", 9999)