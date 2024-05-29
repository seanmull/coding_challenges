import aiohttp
from aiohttp import web
from utils import (
    serialize_resp,
    deserialize_resp,
    deserialize_req,
    remove_key_after_delay,
    is_number,
)
from linkedlist import LinkedList
import json

cache = {}


async def handle(request):
    serialized_request = request.rel_url.query.get("request")
    is_millisecond = request.rel_url.query.get("is_millisecond")
    time_delay = request.rel_url.query.get("time_delay")
    is_unixtime = request.rel_url.query.get("is_unixtime")
    request = deserialize_req(serialized_request)
    cmd, key, value, text = "", "", "", ""
    if len(request) == 3:
        cmd, key, value = request
        cmd = cmd.upper()
        if cmd == "SET":
            cache[key] = serialize_resp(value)
            if time_delay:
                remove_key_after_delay(
                    cache, key, int(time_delay), is_unixtime, is_millisecond
                )
            text = "OK\n"
            text += f"{key} is set to {value}."
        elif cmd == "LPUSH":
             if cache.get(key):
                val = deserialize_resp(cache[key])
                if type(val) is list:
                    ll = LinkedList()
                    ll.array_to_linked_list(val)
                    ll.add_to_front(value)
                    # if we only support array/list data types as part of RESP how can we use linkedlist
                    arr = ll.linked_list_to_array()
                    cache[key] = serialize_resp(arr)
             else:
                cache[key] = serialize_resp([value])
        elif cmd == "RPUSH":
            if cache.get(key):
                val = deserialize_resp(cache[key])
                if type(val) is list:
                    ll = LinkedList()
                    ll.array_to_linked_list(val)
                    ll.add_to_end(value)
                    # if we only support array/list data types as part of RESP how can we use linkedlist
                    arr = ll.linked_list_to_array()
                    cache[key] = serialize_resp(arr)
            else:
                cache[key] = serialize_resp([value])
    elif len(request) == 2:
        cmd, key = request
        cmd = cmd.upper()
        if cmd == "ECHO":
            text = f"{key}"
        elif cmd == "get":
            if cache.get(key):
                text = f"{deserialize_resp(cache[key])}"
            else:
                text = f"{key} is not in cache."
        elif cmd == "EXISTS":
            if cache.get(key):
                text = "1"
            else:
                text = "0"
        elif cmd == "DEL":
            if cache.get(key):
                del cache[key]
                text = f"{key} is removed from cache."
        elif cmd == "INCR":
            if cache.get(key):
                val = deserialize_resp(cache[key])
                if is_number(val):
                    new = 1 + int(val)
                    cache[key] = serialize_resp(new)
        elif cmd == "DECR":
            if cache.get(key):
                val = deserialize_resp(cache[key])
                if is_number(val):
                    new = int(val) - 1
                    cache[key] = serialize_resp(new)
        else:
            text = f"{cmd}, {key}"
    elif len(request) == 1:
        cmd = request
        if cmd[0].upper() == "PING":
            text = "PONG"
        elif cmd[0].upper() == "SAVE":
            with open("cache.json", 'w') as file:
                json.dump(cache, file, indent=4)
        else:
            text = f"{cmd[0]}"
    print(f"cache is {cache}")
    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get("/", handle)])

if __name__ == "__main__":
    web.run_app(app, port=6379)
