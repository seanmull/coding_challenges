from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import requests

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Define the response code and headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        response = requests.get("http://localhost:8080")
        # Define the response content
        response_content = str.encode(response.text)
        
        # Write the response content
        self.wfile.write(response_content)

# Create a class that inherits from ThreadingMixIn and HTTPServer
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# Define server address and port
server_address = ('', 8081)

# Create and start the threaded HTTP server
httpd = ThreadingHTTPServer(server_address, SimpleHTTPRequestHandler)
print("Starting threaded server on port 8081...")
httpd.serve_forever()

