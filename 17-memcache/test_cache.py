import socket
import pytest
from concurrent.futures import ThreadPoolExecutor
import telnetlib
import time

def send_command(client, command, timeout=2):
    client.write(command.encode('utf-8'))
    if command.startswith("get"):
        response = client.read_until(b"\r\nEND\r\n", timeout).decode('utf-8')
    else:
        response = client.read_until(b"\r\n", timeout).decode('utf-8')
    return response

def test_set_operation():
    with telnetlib.Telnet('localhost', 11211) as client:
        response = send_command(client, 'set test 0 5 4\r\n1234\r\n')
        assert response == "STORED\r\n"

def test_get_operation():
    with telnetlib.Telnet('localhost', 11211) as client:
        send_command(client, 'set test 0 5 4\r\n1234\r\n')
        response = send_command(client, 'get test\r\n')
        expected_response = "VALUE test 0 4\r\n1234\r\nEND\r\n"
        assert response == expected_response

def test_get_operation_not_found():
    with telnetlib.Telnet('localhost', 11211) as client:
        response = send_command(client, 'get nonexistent\r\n')
        assert response == "END\r\n"

def test_set_noreply():
    with telnetlib.Telnet('localhost', 11211) as client:
        send_command(client, 'set test2 1 5 7 noreply\r\ntesting\r\n')
        response = send_command(client, 'get test2\r\n')
        expected_response = "VALUE test2 1 7\r\ntesting\r\nEND\r\n"
        assert response == expected_response

def test_concurrency():
    commands_list = [
        ['set test1 0 5 5\r\nhello\r\n', 'get test1\r\n'],
        ['set test2 1 5 6\r\nworld!\r\n', 'get test2\r\n'],
        ['set test3 2 5 4\r\ntest\r\n', 'get test3\r\n']
    ]

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(client_task, commands) for commands in commands_list]
        results = [future.result() for future in futures]

    expected_results = [
        ["STORED\r\n", "VALUE test1 0 5\r\nhello\r\nEND\r\n"],
        ["STORED\r\n", "VALUE test2 1 6\r\nworld!\r\nEND\r\n"],
        ["STORED\r\n", "VALUE test3 2 4\r\ntest\r\nEND\r\n"]
    ]

    assert results == expected_results

def test_expiry_key_found():
    with telnetlib.Telnet('localhost', 11211) as client:
        send_command(client, 'set test5 0 5 4\r\nabcd\r\n')
        time.sleep(4)  # Wait for expiry
        response = send_command(client, 'get test5\r\n')
        expected_response = "VALUE test5 0 4\r\nabcd\r\nEND\r\n"
        assert response == expected_response

def test_expiry_key_not_found():
    with telnetlib.Telnet('localhost', 11211) as client:
        send_command(client, 'set test6 0 3 4\r\nxyz\r\n')
        time.sleep(4)  # Wait for expiry
        response = send_command(client, 'get test6\r\n')
        assert response == "END\r\n"

def client_task(task_commands):
    responses = []
    with telnetlib.Telnet('localhost', 11211) as client:
        for command in task_commands:
            responses.append(send_command(client, command))
    return responses

if __name__ == "__main__":
    pytest.main(['-sv', __file__])

