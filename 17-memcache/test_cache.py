import pytest
import telnetlib

def send_command(client, command):
    client.write(command.encode('utf-8'))
    return client.read_until(b"\r\nEND\r\n").decode('utf-8') if command.startswith("get") else client.read_until(b"\r\n").decode('utf-8')

def test_set_operation_success():
    # Connect to the memcached server
    client = telnetlib.Telnet('localhost', 11211)

    # Perform set operation
    set_command = "set test 0 0 4\r\n1234\r\n"
    response = send_command(client, set_command)
    assert response.strip() == "STORED"

    client.close()

def test_get_operation_success():
    # Connect to the memcached server
    client = telnetlib.Telnet('localhost', 11211)

    # Perform set operation
    set_command = "set test 0 0 4\r\n1234\r\n"
    response = send_command(client, set_command)
    assert response.strip() == "STORED"

    # Perform get operation
    get_command = "get test\r\n"
    response = send_command(client, get_command)
    expected_response = "VALUE test 0 4\r\n1234\r\nEND\r\n"
    assert response == expected_response

    client.close()

def test_set_operation_noreply():
    # Connect to the memcached server
    client = telnetlib.Telnet('localhost', 11211)

    # Perform set operation with noreply
    set_command_noreply = "set test2 1 0 7 noreply\r\ntesting\r\n"
    response = send_command(client, set_command_noreply)
    assert response == "\r\n"

    client.close()

def test_get_operation_not_found():
    # Connect to the memcached server
    client = telnetlib.Telnet('localhost', 11211)

    # Perform get operation for non-existing key
    get_command_test2 = "get test3\r\n"
    response = send_command(client, get_command_test2)
    assert response.strip() == "END"

    client.close()

def test_continuous_session():
    # Connect to the memcached server
    client = telnetlib.Telnet('localhost', 11211)

    # Perform set operation
    set_command = "set test 0 0 4\r\n1234\r\n"
    response = send_command(client, set_command)
    assert response.strip() == "STORED"

    # Perform get operation
    get_command = "get test\r\n"
    response = send_command(client, get_command)
    expected_response = "VALUE test 0 4\r\n1234\r\nEND\r\n"
    assert response == expected_response

    # Perform another set operation with noreply
    set_command_noreply = "set test2 1 0 7 noreply\r\ntesting\r\n"
    response = send_command(client, set_command_noreply)
    assert response == ""

    # Perform get operation for the new key
    get_command_test2 = "get test2\r\n"
    response = send_command(client, get_command_test2)
    expected_response_test2 = "VALUE test2 1 7\r\ntesting\r\nEND\r\n"
    assert response == expected_response_test2

    # Perform get operation for a non-existing key
    get_command_non_existing = "get nonexisting\r\n"
    response = send_command(client, get_command_non_existing)
    assert response.strip() == "END"

    client.close()

if __name__ == "__main__":
    pytest.main()

