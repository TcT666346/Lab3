import socket

def send_request(client_socket, command, key, value=None):
    if command == 'R' or command == 'G':
        message = f"{7 + len(key):03d} {command} {key}"
    elif command == 'P':
        message = f"{7 + len(key) + len(value):03d} {command} {key} {value}"
    else:
        print("Invalid command")
        return
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    print(f"{command} {key} {' ' + value if value else ''}: {response[4:]}")

def run_client(host, port, file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(' ')
                if len(parts) == 2:
                    command, key = parts
                    send_request(client_socket, command, key)
                elif len(parts) == 3:
                    command, key, value = parts
                    send_request(client_socket, command, key, value)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()