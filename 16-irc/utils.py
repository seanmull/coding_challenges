import socket
import time

class IRCClient:
    def __init__(self, server, port, nickname, realname, channel):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.realname = realname
        self.channel = channel
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self, password=None):
        self.socket.connect((self.server, self.port))
        if password:
            self.send(f"PASS {password}")
        self.send(f"NICK {self.nickname}")
        self.send(f"USER {self.nickname} 0 * :{self.realname}")
        time.sleep(2)
        self.send(f"JOIN {self.channel}")
    
    def send(self, msg):
        self.socket.send(f"{msg}\r\n".encode('utf-8'))
    
    def receive(self):
        return self.socket.recv(4096).decode('utf-8', errors='ignore')
    
    def run(self):
        while True:
            response = self.receive()
            if response.startswith("PING"):
                self.send(f"PONG {response.split()[1]}")
            else:
                print(response)
            time.sleep(1)
    
    def send_message(self, message):
        self.send(f"PRIVMSG {self.channel} :{message}")

