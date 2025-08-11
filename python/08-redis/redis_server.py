#!/usr/bin/env python3
from aiohttp import web
import utils

data = {}

async def handle_post(request):
    try:
        json = await request.json()
    except Exception as e:
        return web.Response(text="Failed to parse JSON", status=400)
    
    print(f"Received json: {json}")

    response = utils.update_data(json["command"], data)

    return web.json_response(response)

app = web.Application()
app.router.add_post('/', handle_post)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=6380)
