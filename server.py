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