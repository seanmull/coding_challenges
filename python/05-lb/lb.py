#!/usr/bin/env python3
from aiohttp import web, ClientSession
import asyncio

server_is_available = [["localhost:8081", True], [
    "localhost:8082", True], ["localhost:8083", True]]
counter = 0


async def fetch_data(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def update_servers_status():
    while True:
        for i, server in enumerate(server_is_available):
            url, _ = server
            response = None
            try:
                response = await fetch_data(f"http://{url}")
            except Exception:
                pass

            if response:
                server_is_available[i][1] = True
            else:
                server_is_available[i][1] = False

        print(server_is_available)
        await asyncio.sleep(1)


async def start_web_app():
    async def handler(request):
        async with ClientSession() as session:
            global counter
            attempts = 0
            url, health_check = None, False
            while not health_check:
                url, health_check = server_is_available[counter % len(
                    server_is_available)]
                print(
                    f'Current status of server on {url} is {health_check if "Healthy" else "Unhealthy"}')
                if not health_check:
                    attempts += 1
                    counter += 1
                elif attempts > 3:
                    await asyncio.sleep(5)
                    attempts = 0
            async with session.get(f'http://{url}') as resp:
                text = await resp.text()
                counter += 1
        return web.Response(text=text, status=200)

    app = web.Application()
    app.add_routes([web.get('/', handler)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)
    await site.start()


async def main():
    await asyncio.gather(
        start_web_app(),
        update_servers_status()
    )

if __name__ == '__main__':
    asyncio.run(main())
