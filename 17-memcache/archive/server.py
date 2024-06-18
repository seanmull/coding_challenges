import socket
import threading
import time

cache = {}

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
                    break

                if len(command_parts) < 5:
                    print("Incomplete command line")
                    buffer = remainder
                    continue

                byte_count = int(command_parts[4])
                expected_length = byte_count + 2

                if len(remainder) >= expected_length:
                    data_block = remainder[:byte_count]
                    remainder = remainder[expected_length:]
                    buffer = remainder

                    key = command_parts[1]
                    value = {
                        "command_name": command_parts[0],
                        "flags": command_parts[2],
                        "exptime": int(command_parts[3]),
                        "byte_count": command_parts[4],
                        "data_block": data_block,
                        "noreply": len(command_parts) == 6 and command_parts[5].lower() == 'noreply'
                    }
                    store_in_cache(key, value)

                    print(command_line)
                    print(data_block)

                    if not value["noreply"]:
                        print("STORED")
                        connection.sendall(b"STORED\r\n")

                    break
                else:
                    buffer = command_line + '\r\n' + remainder
                    break
    finally:
        connection.close()

def handle_get_request(connection, key):
    if key in cache:
        value = cache[key]
        if value['exptime'] != 0 and time.time() > value['exptime']:
            del cache[key]
            response = "END\r\n"
        else:
            response = f"VALUE {key} {value['flags']} {value['byte_count']}\r\n{value['data_block']}\r\nEND\r\n"
    else:
        response = "END\r\n"
    connection.sendall(response.encode('utf-8'))

def store_in_cache(key, value):
    if value["exptime"] <= 0:
        value["exptime"] = time.time()
    else:
        value["exptime"] = time.time() + value["exptime"]
    cache[key] = value

def manage_expiry():
    while True:
        time.sleep(10)
        current_time = time.time()
        keys_to_delete = [key for key, value in cache.items() if value['exptime'] != 0 and current_time > value['exptime']]
        for key in keys_to_delete:
            del cache[key]

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 11211))
    server_socket.listen()

    expiry_thread = threading.Thread(target=manage_expiry)
    expiry_thread.daemon = True
    expiry_thread.start()

    print("Server listening on port 11211")

    while True:
        connection, _ = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection,))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    start_server()

