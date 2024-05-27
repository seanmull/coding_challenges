import pytest

from utils import deserialize_resp, serialize_resp

def test_null_bulk_string():
    assert deserialize_resp("$-1\r\n") is None

def test_array_one_bulk_string():
    assert deserialize_resp("*1\r\n$4\r\nping\r\n") == ["ping"]

def test_array_two_bulk_strings():
    assert deserialize_resp("*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n") == ["echo", "hello world"]

def test_array_two_bulk_strings_get_key():
    assert deserialize_resp("*2\r\n$3\r\nget\r\n$3\r\nkey\r\n") == ["get", "key"]

def test_simple_string_ok():
    assert deserialize_resp("+OK\r\n") == "OK"

def test_error_message():
    assert deserialize_resp("-Error message\r\n") == {"error": "Error message"}

def test_empty_bulk_string():
    assert deserialize_resp("$0\r\n\r\n") == ""

def test_simple_bulk_string():
    assert deserialize_resp("$5\r\nhello\r\n") == "hello"

def test_simple_string_hello_world():
    assert deserialize_resp("+hello world\r\n") == "hello world"

def test_positive_int():
    assert deserialize_resp(":100\r\n") == 100

def test_negative_int():
    assert deserialize_resp(":-100\r\n") == -100


def test_null_bulk_string_serialize():
    assert serialize_resp(None) == "$-1\r\n"

def test_array_one_bulk_string_serialize():
    assert serialize_resp(["ping"]) == "*1\r\n$4\r\nping\r\n"

def test_array_two_bulk_strings_serialize():
    assert serialize_resp(["echo", "hello world"]) == "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n"

def test_array_two_bulk_strings_get_key_serialize():
    assert serialize_resp(["get", "key"]) == "*2\r\n$3\r\nget\r\n$3\r\nkey\r\n"

def test_simple_string_ok_serialize():
    assert serialize_resp("OK") == "+OK\r\n"

def test_error_message_serialize():
    assert serialize_resp({"error": "Error message"}) == "-Error message\r\n"

def test_empty_bulk_string_serialize():
    assert serialize_resp("", "bulk") == "$0\r\n\r\n"

def test_simple_bulk_string_serialize():
    assert serialize_resp("hello","bulk") == "$5\r\nhello\r\n"

def test_simple_string_hello_world_serialize():
    assert serialize_resp("hello world") == "+hello world\r\n"

def test_positive_int_serialize():
    assert serialize_resp(100) == ":100\r\n"

def test_negative_int_serialize():
    assert serialize_resp(-100) == ":-100\r\n"

if __name__ == "__main__":
    pytest.main()

