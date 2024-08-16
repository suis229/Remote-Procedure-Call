import socket
import json
import threading
import os
import math

SOCKET_PATH = '/tmp/rpc_socket'

def floor(x):
    return math.floor(x)

def nroot(n, x):
    return x ** (1 / n)

def reverse(s):
    return s[::-1]

def valid_anagram(str1, str2):
    return sorted(str1) == sorted(str2)

def sort_strings(str_arr):
    return sorted(str_arr)

rpc_methods = {
    "floor": floor,
    "nroot": nroot,
    "reverse": reverse,
    "validAnagram": valid_anagram,
    "sort": sort_strings
}

def handle_client(client_socket):
    try:
        request_data = client_socket.recv(1024).decode('utf-8')
        request = json.loads(request_data)

        method_name = request.get("method")
        params = request.get("params")
        param_types = request.get("param_types")
        request_id = request.get("id")

        if method_name in rpc_methods:
            method = rpc_methods[method_name]
            result = method(*params)
            response = {
                "result": result,
                "result_type": str(type(result).__name__),
                "id": request_id
            }
        else:
            response = {
                "error": "Method not found",
                "id": request_id
            }
    except Exception as e:
        response = {
            "error": str(e),
            "id": request_id
        }

    client_socket.sendall(json.dumps(response).encode('utf-8'))
    client_socket.close()

def start_server():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(SOCKET_PATH)
    server_socket.listen(5)
    print("Server is listening...")

    while True:
        client_socket, _ = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
