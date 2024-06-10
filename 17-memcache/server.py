import socket
import threading

def start_server(host='0.0.0.0', port=11211):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Listen for incoming connections (max 5 connections in queue)
    server_socket.listen(5)
    print(f"Listening on {host}:{port}")

    while True:
        # Wait for a connection
        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Handle each connection in a new thread
        client_thread = threading.Thread(target=handle_client, args=(connection,))
        client_thread.start()

def handle_client(connection):
    try:
        # Buffer for accumulating received data
        buffer = ""

        while True:
            data = connection.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8')

            # Process each complete message in the buffer
            while '\r\n' in buffer:
                # Separate the command line from the rest of the buffer
                command_line, remainder = buffer.split('\r\n', 1)

                # Parse the command line to determine how much more data is expected
                command_parts = command_line.split()
                if len(command_parts) < 5:
                    print("Incomplete command line")
                    buffer = remainder
                    continue

                byte_count = int(command_parts[4])
                expected_length = byte_count + 2  # including the trailing \r\n

                # Check if the remainder contains the entire data block
                if len(remainder) >= expected_length:
                    data_block = remainder[:byte_count]
                    remainder = remainder[expected_length:]
                    buffer = remainder
                    parse_and_log(command_line, data_block)

                    # Send a response back to the client if noreply is not set
                    if len(command_parts) < 6 or command_parts[5].lower() != 'noreply':
                        connection.sendall(b"STORED\r\n")

                    # Close the connection after processing
                    connection.close()
                    return

                else:
                    # Wait for more data to complete the message
                    buffer = command_line + '\r\n' + remainder
                    break

    finally:
        # Clean up the connection if it's still open
        connection.close()

def parse_and_log(command_line, data_block):
    try:
        # Split the command line into its components
        command_parts = command_line.split()

        # Extract command components
        command_name = command_parts[0]
        key = command_parts[1]
        flags = command_parts[2]
        exptime = command_parts[3]
        byte_count = command_parts[4]

        # Check for noreply option
        noreply = False
        if len(command_parts) == 6 and command_parts[5].lower() == 'noreply':
            noreply = True

        # Print debug log
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

