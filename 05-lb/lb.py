from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import requests

ports = [8080, 8081, 8082]
ticker_lock = threading.Lock()
global ticker
ticker = 0


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


health_status = {"8080": True, "8081": True, "8082": True}


def set_status():
    for key, value in health_status.items():
        try:
            requests.get(f"http://localhost:{key}")
        except requests.RequestException:
            health_status[key] = False

def get_num_of_healthy_servers():
    n = 0
    for key, value in health_status.items():
        if value:
            n += 1
    return n

set_interval(set_status, 5)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global ticker
        global port

        # Use a lock to ensure that ticker is updated correctly
        with ticker_lock:
            num_healthy_servers = get_num_of_healthy_servers()
            port = ports[ticker]
            i = 0
            if not health_status[str(port)]:
                i += 1
                ticker = (ticker + 1) % num_healthy_servers
                port = ports[ticker]
                if i == len(ports):
                    print("All ports are unhealthy")
                    exit()
            else:
                ticker = (ticker + 1) % num_healthy_servers

        # Forward the request to the selected backend server
        response = requests.get(f"http://localhost:{port}")

        # Define the response code and headers
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Write the response content
        self.wfile.write(response.content)


# Create a class that inherits from ThreadingMixIn and HTTPServer
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


# Define server address and port for the load balancer
server_address = ("", 8079)

# Create and start the threaded HTTP server
httpd = ThreadingHTTPServer(server_address, SimpleHTTPRequestHandler)
print("Starting load balancer on port 8079...")
httpd.serve_forever()
