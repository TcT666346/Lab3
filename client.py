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