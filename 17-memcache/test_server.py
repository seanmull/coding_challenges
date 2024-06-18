import pytest
import socket

@pytest.fixture
def memcache_server():
    # Assuming the memcache server is running locally on port 11211
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("localhost", 11211))
    yield server
    server.close()

def send_command(server, command, data=None):
    if data is None:
        server.sendall((command + "\r\n").encode())
    else:
        server.sendall((command + "\r\n").encode())
        server.sendall(f'{data}\r\n'.encode())
    return server.recv(1024).decode().strip()

def test_set_get_commands(memcache_server):
    # Test set and get commands
    send_command(memcache_server, "set test 0 2 4", "1234")
    response = send_command(memcache_server, "get test")
    assert response == "VALUE test 0 4\r\n1234\r\nEND"

if __name__ == "__main__":
    pytest.main(["-v", "--tb=native", __file__])

