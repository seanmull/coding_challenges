import socket
import threading

cache = {}

def handle_get_request(connection, key):
    if key in cache:
        value = cache[key]
        response = f"VALUE {key} {value['flags']} {value['byte_count']}\r\n{value['data_block']}\r\nEND\r\n"
        connection.sendall(response.encode('utf-8'))
    else:
        connection.sendall(b"END\r\n")

def handle_client(connection):
    try:
        buffer = ""
        while True:
            data = connection.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8')

            while '\r\n' in buffer:
                command_line, remainder = buffer.split('\r\n', 1)
                command_parts = command_line.split()

                if command_parts[0] == 'get' and len(command_parts) == 2:
                    key = command_parts[1]
                    handle_get_request(connection, key)
                    buffer = remainder
                    continue

                if len(command_parts) < 5:
                    print("Incomplete command line")
                    buffer = remainder
                    continue

                byte_count = int(command_parts[4])
                expected_length = byte_count + 2  # 2 for the trailing \r\n

                if len(remainder) >= expected_length:
                    data_block = remainder[:byte_count]
                    remainder = remainder[expected_length:]
                    buffer = remainder

                    key = command_parts[1]
                    value = {
                        "command_name": command_parts[0],
                        "flags": command_parts[2],
                        "exptime": command_parts[3],
                        "byte_count": command_parts[4],
                        "data_block": data_block,
                        "noreply": len(command_parts) == 6 and command_parts[5].lower() == 'noreply'
                    }
                    cache[key] = value

                    print(command_line)
                    print(data_block)

                    if not value["noreply"]:
                        connection.sendall(b"STORED\r\n")
                    else:
                        connection.sendall(b"\r\n")

                    buffer = remainder
                else:
                    buffer = command_line + '\r\n' + remainder
                    break
    finally:
        connection.close()

def start_server(host='localhost', port=11211):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()

