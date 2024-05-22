import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.port = kwargs.pop('port', None)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Define the response code and headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Define the response content
        response_content = f"Hello from port {self.port}!".encode()
        
        # Write the response content
        self.wfile.write(response_content)

# Create a class that inherits from ThreadingMixIn and HTTPServer
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def make_handler_with_port(port):
    def handler(*args, **kwargs):
        SimpleHTTPRequestHandler(*args, port=port, **kwargs)
    return handler

def start_server(port):
    server_address = ('', port)
    handler = make_handler_with_port(port)
    httpd = ThreadingHTTPServer(server_address, handler)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

# List of ports to start servers on
ports = [8080, 8081, 8082]

# Create and start a thread for each server
threads = []
for port in ports:
    thread = threading.Thread(target=start_server, args=(port,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

