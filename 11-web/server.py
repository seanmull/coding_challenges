import os
import socket
import threading

# Define the host and port
HOST, PORT = '127.0.0.1', 8080

# Base directory for serving files
base_dir = os.path.join(os.getcwd(), 'www')

# Function to handle client connections
def handle_client(client_connection):
    try:
        # Receive the request data
        request = client_connection.recv(1024).decode('utf-8')
        print(request)
        
        # Extract the requested path from the request
        try:
            request_line = request.splitlines()[0]
            request_path = request_line.split(' ')[1]
            if request_path == '/':
                request_path = '/index.html'
        except IndexError:
            request_path = '/index.html'

        # Sanitize the requested path to prevent directory traversal
        sanitized_path = os.path.normpath(request_path).lstrip('/')
        full_path = os.path.join(base_dir, sanitized_path)

        # Ensure the path is within the base directory
        if os.path.commonpath([base_dir, full_path]) != base_dir:
            raise ValueError("Attempted directory traversal attack")

        # Read the requested file
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            status_line = "HTTP/1.1 200 OK"
        except (FileNotFoundError, IsADirectoryError):
            html_content = "<html><body><h1>404 Not Found</h1></body></html>"
            status_line = "HTTP/1.1 404 Not Found"

        # Define the HTTP response with proper headers
        http_response = f"""{status_line}
Content-Type: text/html
Content-Length: {len(html_content)}

{html_content}
"""
        
        # Send the HTTP response
        client_connection.sendall(http_response.encode('utf-8'))
    
    except Exception as e:
        print(f"Error handling request: {e}")
        error_response = "HTTP/1.1 500 Internal Server Error\r\n\r\n<html><body><h1>500 Internal Server Error</h1></body></html>"
        client_connection.sendall(error_response.encode('utf-8'))
    
    finally:
        # Close the connection
        client_connection.close()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections (up to 5 connections can wait)
server_socket.listen(5)
print(f"Serving HTTP on {HOST} port {PORT} (http://{HOST}:{PORT}/) ...")

while True:
    # Accept a connection
    client_connection, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    
    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_connection,))
    client_thread.start()

