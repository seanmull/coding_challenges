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
        server.sendall(f"{data}\r\n".encode())
    return server.recv(1024).decode().strip()

def test_set_get_commands(memcache_server):
    # Test set and get commands
    send_command(memcache_server, "set test_set_get 0 0 4", "1234")
    response = send_command(memcache_server, "get test_set_get")
    assert response == "VALUE test_set_get 0 4\r\n1234\r\nEND"

def test_add_command(memcache_server):
    # Test add command for adding a new key
    send_command(memcache_server, "add test_add 0 0 6", "newval")
    response = send_command(memcache_server, "get test_add")
    assert response == "VALUE test_add 0 6\r\nnewval\r\nEND"

def test_replace_command(memcache_server):
    # Test replace command for replacing an existing key
    send_command(memcache_server, "set test_replace 0 0 4", "abcd")
    response = send_command(memcache_server, "replace test_replace 0 0 6", "newval")
    assert response == "STORED"

    response = send_command(memcache_server, "get test_replace")
    assert response == "VALUE test_replace 0 6\r\nnewval\r\nEND"

    response = send_command(memcache_server, "replace test_replace_non_existing 0 0 4", "abcd")
    assert response == "NOT_STORED"

def test_append_command(memcache_server):
    # Test append command for adding to the end of a value
    send_command(memcache_server, "set test_append 0 0 4", "abcd")
    response = send_command(memcache_server, "append test_append 0 0 4", "efgh")
    assert response == "STORED"

    response = send_command(memcache_server, "get test_append")
    assert response == "VALUE test_append 0 8\r\nabcdefgh\r\nEND"

def test_prepend_command(memcache_server):
    # Test prepend command for adding to the beginning of a value
    send_command(memcache_server, "set test_prepend 0 0 4", "abcd")
    response = send_command(memcache_server, "prepend test_prepend 0 0 4", "efgh")
    assert response == "STORED"

    response = send_command(memcache_server, "get test_prepend")
    assert response == "VALUE test_prepend 0 8\r\nefghabcd\r\nEND"


if __name__ == "__main__":
    pytest.main(["-v", "--tb=native", __file__])
