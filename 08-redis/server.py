import aiohttp
from aiohttp import web
from utils import deserialize_resp, deserialize_req

cache = {}

async def handle(request):
    serialized_request = request.rel_url.query.get('request')
    request = deserialize_req(serialized_request)
    cmd, key, value, text = "", "", "", ""
    if len(request) == 3:
        cmd, key, value = request
        if cmd == "set":
            cache[key] = value
            print(f"{key} is set to {value}.")
    elif len(request) == 2:
        cmd, key = request
        if cmd == "ECHO":
            text = f"{key}"
        elif cmd == "get":
            if cache.get(key):
                pass
                text = f"{cache[key]}"
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

