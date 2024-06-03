import socket

# Define the host and port
HOST, PORT = "127.0.0.1", 8080

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections (1 connection at a time)
server_socket.listen(1)
print(f"Serving HTTP on {HOST} port {PORT} (http://{HOST}:{PORT}/) ...")

while True:
    # Accept a connection
    client_connection, client_address = server_socket.accept()

    # Receive the request data
    request = client_connection.recv(1024)
    print(request.decode("utf-8"))

    # Define the HTTP response
    http_response = b"""\
HTTP/1.1 200 OK

<html>
<head>
    <title>Hello World</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
"""

    # Send the HTTP response
    client_connection.sendall(http_response)

    # Close the connection
    client_connection.close()
