import aiohttp
from aiohttp import web
from utils import serialize_resp, deserialize_resp, deserialize_req, remove_key_after_delay

cache = {}

async def handle(request):
    serialized_request = request.rel_url.query.get('request')
    is_millisecond = request.rel_url.query.get('is_millisecond')
    time_delay = request.rel_url.query.get('time_delay')
    is_unixtime = request.rel_url.query.get('is_unixtime')
    request = deserialize_req(serialized_request)
    cmd, key, value, text = "", "", "", ""
    if len(request) == 3:
        cmd, key, value = request
        if cmd == "set":
            cache[key] = serialize_resp(value)
            if time_delay:
                remove_key_after_delay(cache, key, int(time_delay), is_unixtime, is_millisecond)
            print(f"{key} is set to {value}.")
    elif len(request) == 2:
        cmd, key = request
        if cmd == "ECHO":
            text = f"{key}"
        elif cmd == "get":
            if cache.get(key):
                text = f"{deserialize_resp(cache[key])}"
            else:
                print(f"{key} is not in cache.")
        else:
            text = f"{cmd}, {key}"
    elif len(request) == 1:
        cmd = request
        if cmd[0] == "PING":
            text = "PONG"
        else:
            text = f"{cmd[0]}"
    print(f"cache is {cache}")
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app, port=6379)

