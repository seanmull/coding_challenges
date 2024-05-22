import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Define the response code and headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Get the port number from the server
        port_number = self.server.port
        
        # Define the response content
        response_content = f"Hello from port {port_number}!".encode()
        
        # Write the response content
        self.wfile.write(response_content)

# Create a class that inherits from ThreadingMixIn and HTTPServer
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, port):
        super().__init__(server_address, RequestHandlerClass)
        self.port = port  # Store the port number

def start_server(port):
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, SimpleHTTPRequestHandler, port)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

# List of ports to start servers on
ports = [8080, 8081]

# Create and start a thread for each server
threads = []
for port in ports:
    thread = threading.Thread(target=start_server, args=(port,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

