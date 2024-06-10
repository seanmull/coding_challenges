import socket
import threading

cache = {}

def start_server(host='0.0.0.0', port=11211):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Listening on {host}:{port}")

    while True:
        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(connection,))
        client_thread.start()

def handle_get_request(connection, key):
    if key in cache:
        value = cache[key]
        response = f"VALUE {key} {value['flags']} {value['byte_count']}\r\n{value['data_block']}\r\nEND\r\n"
        print(response)
        connection.sendall(response.encode('utf-8'))
    else:
        print("END")
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
                    connection.close()
                    return

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
                    # parse_and_log(command_line, data_block)

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
                        print("STORED")
                        connection.sendall(b"STORED\r\n")

                    connection.close()
                    return
                else:
                    buffer = command_line + '\r\n' + remainder
                    break
    finally:
        connection.close()

def parse_and_log(command_line, data_block):
    try:
        command_parts = command_line.split()
        command_name = command_parts[0]
        key = command_parts[1]
        flags = command_parts[2]
        exptime = command_parts[3]
        byte_count = command_parts[4]
        noreply = False
        if len(command_parts) == 6 and command_parts[5].lower() == 'noreply':
            noreply = True

        print(f"Command: {command_name}")
        print(f"Key: {key}")
        print(f"Flags: {flags}")
        print(f"Exptime: {exptime}")
        print(f"Byte count: {byte_count}")
        print(f"Noreply: {noreply}")
        print(f"Data block: {data_block}")
    except Exception as e:
        print(f"Error parsing data: {e}")

if __name__ == "__main__":
    start_server()

