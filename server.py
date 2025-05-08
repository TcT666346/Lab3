import socket
import threading
import time

# 元组空间，使用字典存储
tuple_space = {}
# 操作统计
total_operations = 0
read_operations = 0
get_operations = 0
put_operations = 0
error_count = 0
# 客户端连接总数
client_count = 0

def handle_client(client_socket):
    global total_operations, read_operations, get_operations, put_operations, error_count
    try:
        while True:
            # 接收客户端消息
            message = client_socket.recv(1024).decode()
            if not message:
                break
            # 解析消息
            size_str = message[:3]
            command = message[4]
            key = message[6:].split(' ', 1)[0]
            if command == 'P':
                value = message[6:].split(' ', 1)[1]
            total_operations += 1
            if command == 'R':
                read_operations += 1
                if key in tuple_space:
                    response = f"{len(f'OK ({key}, {tuple_space[key]}) read'):03d} OK ({key}, {tuple_space[key]}) read"
                else:
                    response = f"{len(f'ERR {key} does not exist'):03d} ERR {key} does not exist"
                    error_count += 1
            elif command == 'G':
                get_operations += 1
                if key in tuple_space:
                    value = tuple_space.pop(key)
                    response = f"{len(f'OK ({key}, {value}) removed'):03d} OK ({key}, {value}) removed"
                else:
                    response = f"{len(f'ERR {key} does not exist'):03d} ERR {key} does not exist"
                    error_count += 1
            elif command == 'P':
                put_operations += 1
                if key not in tuple_space:
                    tuple_space[key] = value
                    response = f"{len(f'OK ({key}, {value}) added'):03d} OK ({key}, {value}) added"
                else:
                    response = f"{len(f'ERR {key} already exists'):03d} ERR {key} already exists"
                    error_count += 1
            else:
                response = f"{len('ERR invalid command'):03d} ERR invalid command"
                error_count += 1
            # 发送响应
            client_socket.send(response.encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def print_summary():
    while True:
        time.sleep(10)
        tuple_count = len(tuple_space)
        if tuple_count > 0:
            total_size = sum(len(k) + len(v) for k, v in tuple_space.items())
            avg_tuple_size = total_size / tuple_count
            avg_key_size = sum(len(k) for k in tuple_space.keys()) / tuple_count
            avg_value_size = sum(len(v) for v in tuple_space.values()) / tuple_count
        else:
            avg_tuple_size = 0
            avg_key_size = 0
            avg_value_size = 0
        print(f"Tuple count: {tuple_count}, Avg tuple size: {avg_tuple_size}, "
              f"Avg key size: {avg_key_size}, Avg value size: {avg_value_size}, "
              f"Total clients: {client_count}, Total operations: {total_operations}, "
              f"Read operations: {read_operations}, Get operations: {get_operations}, "
              f"Put operations: {put_operations}, Error count: {error_count}")

def start_server(port):
    global client_count
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    # 启动摘要打印线程
    summary_thread = threading.Thread(target=print_summary)
    summary_thread.daemon = True
    summary_thread.start()
    while True:
        client_socket, client_address = server_socket.accept()
        client_count += 1
        print(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    port = 51234
    start_server(port)
              