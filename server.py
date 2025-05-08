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