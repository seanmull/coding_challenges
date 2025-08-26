#!/usr/bin/env python3
from aiohttp import web
import utils
import re
import pickle
import asyncio

data = {}


async def load_data(cache_location, is_global):
    if is_global:
        global data
    try:
        with open(cache_location, 'rb') as file:
            return pickle.load(file)  
    except (FileNotFoundError, EOFError):
        print("Cannot find file")
        return {}


async def handle_post(request):
    global data
    try:
        json = await request.json()
    except Exception as e:
        return web.Response(text="Failed to parse JSON", status=400)

    # print(f"Received json: {json}")

    command_parts = re.split('\r\n', json["commands"])
    try:
        command = command_parts[2]
    except IndexError:
        command = ""

    if command.lower() == "save":
        response = await utils.save_data(utils.cache_location, data)
    else:
        response = utils.update_data(json["commands"], data)

    try:
        key, expire, ttl = command_parts[4], command_parts[8], command_parts[10]
    except IndexError:
        key, expire, ttl = "", "", ""

    if command == "set" and expire in ("EX","ex"):
        asyncio.create_task(utils.expire_key(key, data, int(ttl)))

    return web.json_response(response)

app = web.Application()
app.router.add_post('/', handle_post)


async def on_startup(app):
    global data
    data = await load_data(utils.cache_location, True)

if __name__ == '__main__':
    app.on_startup.append(on_startup)
    web.run_app(app, host='localhost', port=6380)
