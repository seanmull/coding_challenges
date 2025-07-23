#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
import time
import http.server
import socketserver
import requests
from http.server import BaseHTTPRequestHandler

server_is_available = [["localhost:8081", True], [
    "localhost:8082", True], ["localhost:8083", True]]
counter = 0

http_session = requests.Session()
health_check_session = requests.Session()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type='text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.handle_root()

    def handle_root(self):
        global counter
        attempts = 0
        url, health_check = None, False
        while not health_check:
            url, health_check = server_is_available[counter % len(
                server_is_available)]
            print(
                f'Current status of server on {url} is {health_check if "Healthy" else "Unhealthy"}')
            if not health_check:
                attempts += 1
                counter += 1
            elif attempts > 3:
                print(
                    f'Made {attempts} attempts to server {url} waiting for 5 seconds')
                time.sleep(5)
                attempts = 0
        with http_session.get(f'http://{url}') as resp:
            text = resp.text
            counter += 1
        self._set_response()
        self.wfile.write(b'%s' % text.encode('utf-8'))


def start_web_app():
    PORT = 8080
    
    with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def update_servers_status():
    while True:
        for i, server in enumerate(server_is_available):
            url, _ = server
            response = None
            status = None
            try:
                with health_check_session as session:
                    response = session.get(f"http://{url}")
            except Exception:
                pass

            if response.status_code in (200, 302):
                server_is_available[i][1] = True
            else:
                server_is_available[i][1] = False
                print(f'Current status of server on {url} is Unhealthy and has a status of {status}')
        time.sleep(5)

def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(start_web_app)
        executor.submit(update_servers_status)

if __name__ == '__main__':
    main()
