import aiohttp
from aiohttp import web

async def handle(request):
    cmd = request.rel_url.query.get('cmd')
    data = request.rel_url.query.get('data')
    if cmd == "PING":
        text = "PONG"
    elif cmd == "ECHO":
        text = f"{data}"
    else:
        text = f"{cmd}, {data}"
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle)])

if __name__ == '__main__':
    web.run_app(app, port=6379)

