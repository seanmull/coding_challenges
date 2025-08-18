from utils import serialize_commands, update_data, save_data, expire_key
from redis_server import load_data
from collections import deque
import asyncio
import pytest
from time import sleep

SET_TEST = "set hello world"
GET_TEST = "get hello"
PING_TEST = "ping"
ECHO_TEST = "echo message"
SET_TEST_WITH_INT = "set foo 4"
INCR_TEST = "incr foo"
LPUSH_TEST = 'LPUSH mylist "item1" "item2" "item3"'

cache_location = "/home/s/projects/coding_challenges/python/08-redis/test_cache.pkl"


def test_set():
    assert serialize_commands(
        SET_TEST) == "*3\r\n$3\r\nset\r\n$5\r\nhello\r\n$5\r\nworld\r\n"


def test_get():
    assert serialize_commands(GET_TEST) == "*2\r\n$3\r\nget\r\n$5\r\nhello\r\n"


def test_ping():
    assert serialize_commands(PING_TEST) == "*1\r\n$4\r\nping\r\n"


def test_echo():
    assert serialize_commands(
        ECHO_TEST) == "*2\r\n$4\r\necho\r\n$7\r\nmessage\r\n"


def test_set_with_int():
    assert serialize_commands(
        SET_TEST_WITH_INT) == "*3\r\n$3\r\nset\r\n$3\r\nfoo\r\n$1\r\n4\r\n"


def test_incr():
    assert serialize_commands(INCR_TEST) == "*2\r\n$4\r\nincr\r\n$3\r\nfoo\r\n"


def test_push():
    assert serialize_commands(
        LPUSH_TEST) == '*5\r\n$5\r\nLPUSH\r\n$6\r\nmylist\r\n$7\r\n"item1"\r\n$7\r\n"item2"\r\n$7\r\n"item3"\r\n'


def test_set_command_state():
    data = {}
    update_data("*3\r\n$3\r\nset\r\n$5\r\nhello\r\n$5\r\nworld\r\n", data)
    assert data["hello"] == "world"


def test_set_command_response():
    response = update_data("*3\r\n$3\r\nset\r\n$5\r\nhello\r\n$5\r\nworld\r\n")
    assert response == "+OK\r\n"


def test_get_command_response():
    data = {"hello": "world"}
    response = update_data("*2\r\n$3\r\nget\r\n$5\r\nhello\r\n", data)
    assert response == "+world\r\n"


def test_ping_command_response():
    response = update_data("*1\r\n$4\r\nping\r\n")
    assert response == "+pong\r\n"


def test_exists_state():
    data = {"hello": "world"}
    response = update_data("*2\r\n$6\r\nexists\r\n$5\r\nhello\r\n", data)
    assert response == "+(integer) 1\r\n"


def test_does_not_exist_state():
    response = update_data("*2\r\n$6\r\nexists\r\n$5\r\nhello\r\n", {})
    assert response == "+(nil)\r\n"


def test_delete_state():
    data = {"hello": "world"}
    update_data("*2\r\n$3\r\ndel\r\n$5\r\nhello\r\n", data)
    assert "hello" not in data


def test_echo_response():
    response = update_data("*2\r\n$4\r\necho\r\n$5\r\nhello\r\n")
    assert response == "+hello\r\n"


def test_incr_state():
    data = {"hello": 1}
    update_data("*2\r\n$4\r\nincr\r\n$5\r\nhello\r\n", data)
    assert data["hello"] == 2


def test_decr_state():
    data = {"hello": 1}
    update_data("*2\r\n$4\r\ndecr\r\n$5\r\nhello\r\n", data)
    assert data["hello"] == 0


def test_lpush_state_for_numbers():
    data = {"hello": deque([1, 2, 3])}
    update_data("*2\r\n$4\r\nlpush\r\n$5\r\nhello\r\n$1\r\n8\r\n", data)
    assert data["hello"] == deque([8, 1, 2, 3])


def test_lpush_state_for_strings():
    data = {"hello": deque([1, 2, 3])}
    update_data("*2\r\n$4\r\nlpush\r\n$5\r\nhello\r\n$1\r\nham\r\n", data)
    assert data["hello"] == deque(["ham", 1, 2, 3])


def test_rpush_state_for_numbers():
    data = {"hello": deque([1, 2, 3])}
    update_data("*2\r\n$4\r\nrpush\r\n$5\r\nhello\r\n$1\r\n8\r\n", data)
    assert data["hello"] == deque([1, 2, 3, 8])


def test_rpush_state_for_strings():
    data = {"hello": deque([1, 2, 3])}
    update_data("*2\r\n$4\r\nrpush\r\n$5\r\nhello\r\n$1\r\nham\r\n", data)
    assert data["hello"] == deque([1, 2, 3, "ham"])


@pytest.mark.asyncio
async def test_save_and_load_data():
    data = {"hello": "world"}
    _ = await save_data(cache_location, data)
    loaded_data = await load_data(cache_location, False)
    assert loaded_data == data


@pytest.mark.asyncio
async def test_my_async_function():
    await asyncio.sleep(0.1)
    assert True


@pytest.mark.asyncio
async def test_set_expiry():
    data = {"hello": 1}
    await expire_key("hello", data, 0.1)
    assert not "hello" in data
