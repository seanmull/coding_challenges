import pytest
import telnetlib

def test_set_operation_success():
    # Connect to the memcached server
    client = telnetlib.Telnet('localhost', 11211)
    
    # Send set operation command
    set_command = "set test 0 0 4\r\n1234\r\n"
    client.write(set_command.encode('utf-8'))
    response = client.read_until(b"\r\n").decode('utf-8')
    assert response.strip() == "STORED"

    client.close()

def test_get_operation_success():
    # Connect to the memcached server
    client = telnetlib.Telnet('localhost', 11211)
    
    # Send set operation command
    set_command = "set test 0 0 4\r\n1234\r\n"
    client.write(set_command.encode('utf-8'))
    response = client.read_until(b"\r\n").decode('utf-8')
    assert response.strip() == "STORED"

    # Send get operation command
    get_command = "get test\r\n"
    client.write(get_command.encode('utf-8'))
    response = client.read_until(b"\r\nEND\r\n").decode('utf-8')
    expected_response = "VALUE test 0 4\r\n1234\r\nEND\r\n"
    assert response == expected_response

    client.close()

def test_set_operation_noreply():
    # Connect to the memcached server
    client = telnetlib.Telnet('localhost', 11211)
    
    # Send set operation with noreply command
    set_command_noreply = "set test2 1 0 7 noreply\r\ntesting\r\n"
    client.write(set_command_noreply.encode('utf-8'))

    client.close()

def test_get_operation_not_found():
    # Connect to the memcached server
    client = telnetlib.Telnet('localhost', 11211)
    
    # Send get operation for non-existing key
    get_command_test2 = "get test2\r\n"
    client.write(get_command_test2.encode('utf-8'))
    response = client.read_until(b"\r\nEND\r\n").decode('utf-8')
    assert response.strip() == "END"

    client.close()

