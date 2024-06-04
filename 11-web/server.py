import socket
import os

# Define the host and port
HOST, PORT = '127.0.0.1', 8080

# Path to the HTML file
html_file_path = 'index.html'

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
    print(request.decode('utf-8'))
    
    # Read the HTML file
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except Exception as e:
        print(f"Failed to read HTML file: {e}")
        html_content = "<html><body><h1>Internal Server Error</h1></body></html>"

    # Define the HTTP response with proper headers
    http_response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(html_content)}

{html_content}
"""
    
    # Send the HTTP response
    client_connection.sendall(http_response.encode('utf-8'))
    
    # Close the connection
    client_connection.close()

