from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Define the response code and headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
         # Define the response content
        response_content = b"Hello, World!"
        
        # Write the response content
        self.wfile.write(response_content)       

# Create a class that inherits from ThreadingMixIn and HTTPServer
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# Define server address and port
server_address = ('', 8080)

# Create and start the threaded HTTP server
httpd = ThreadingHTTPServer(server_address, SimpleHTTPRequestHandler)
print("Starting threaded server on port 8080...")
httpd.serve_forever()

