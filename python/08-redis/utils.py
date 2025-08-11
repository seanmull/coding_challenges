import re
from collections import deque
import pickle
import asyncio

cache_location = "/home/s/projects/coding_challenges/python/08-redis/cache.pkl"


async def save_data(cache_location, data):
    with open(cache_location, 'wb') as file:
        await asyncio.to_thread(pickle.dump, data, file, protocol=pickle.HIGHEST_PROTOCOL)
        return "+OK\r\n"


def serialize_commands(s):
    response = []
    commands = s.split(" ")
    response.append(f"*{len(commands)}\r\n")
    for command in commands:
        response.append(f"${len(command)}\r\n{command}\r\n")
    return "".join(response)


async def expire_key(key, store, ttl):
    await asyncio.sleep(ttl)
    if key in store:
        del store[key]


def update_data(serialized_command, data={}):
    commands = [r for r in re.split("\r\n", serialized_command) if not (
        r.startswith("*") or r.startswith("$") or len(r) == 0)]
    command = commands[0].lower()
    if command == "set":
        if len(commands) == 3:
            command, key, value = commands
        elif len(commands) == 5:
            command, key, value, _, ttl = commands
        data[key] = value
        return "+OK\r\n"
    elif command == "get":
        command, key = commands
        if key in data:
            return f'+{data[key]}\r\n'
        else:
            return f'+(nil)\r\n'
    elif command == "exists":
        command, key = commands
        if key in data:
            return f'+(integer) 1\r\n'
        else:
            return f'+(nil)\r\n'
    elif command == "del":
        command, key = commands
        if key in data:
            del data[key]
            return f'+(integer) 1\r\n'
        else:
            return f'+(interer) 0\r\n'
    elif command == "ping":
        return "+pong\r\n"
    elif command == "echo":
        command, string = commands
        return f'+{string}\r\n'
    elif command == "incr":
        command, key = commands
        if key in data:
            if isinstance(data[key], int):
                data[key] += 1
                return f'+(integer) {data[key]}\r\n'
            else:
                return f'-Error key {key} does not have value that is type int.\r\n'
        else:
            if isinstance(data[key], int):
                data[key] = 1
                return f'+(integer) {data[key]}\r\n'
            else:
                return f'-Error key {key} does not have value that is type int.\r\n'
    elif command == "decr":
        command, key = commands
        if key in data:
            if isinstance(data[key], int):
                data[key] -= 1
                return f'+(integer) {data[key]}\r\n'
            else:
                return f'-Error key {key} does not have value that is type int.\r\n'
        else:
            if isinstance(data[key], int):
                data[key] = -1
                return f'+(integer) {data[key]}\r\n'
            else:
                return f'-Error key {key} does not have value that is type int.\r\n'
    elif command == "lpush":
        command = commands[0]
        key = commands[1]
        if key in data:
            a = []
            for c in commands[2:]:
                try:
                    a.append(int(c))
                except:
                    a.append(c)
            data[key].appendleft(*a)
            return f'+(integer) {len(data[key])}\r\n'
        else:
            deque(*commands[2:])
            return f'+(integer) {len(data[key])}\r\n'
    elif command == "rpush":
        command = commands[0]
        key = commands[1]
        if key in data:
            a = []
            for c in commands[2:]:
                try:
                    a.append(int(c))
                except:
                    a.append(c)
            data[key].append(*a)
            return f'+(integer) {len(data[key])}\r\n'
        else:
            deque(*commands[2:])
            return f'+(integer) {len(data[key])}\r\n'
    else:
        return f'-Error: Command {command} is not supported.'
