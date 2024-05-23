import asyncio
from aiohttp import web

async def handle(request):
    # Define the response content
    port = request.app['port']
    response_content = f"Hello from port {port}!"

    # Return the response
    return web.Response(text=response_content)

async def start_server(port):
    app = web.Application()
    app['port'] = port  # Store the port in the app context
    app.router.add_get('/', handle)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', port)
    await site.start()
    print(f"Starting server on port {port}...")
    await asyncio.Event().wait()  # Keep the server running

if __name__ == '__main__':
    ports = [8080, 8081, 8082]

    loop = asyncio.get_event_loop()
    tasks = [start_server(port) for port in ports]
    loop.run_until_complete(asyncio.gather(*tasks))

