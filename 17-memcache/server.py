import asyncio
import argparse

async def handle_client(reader, writer):
    while True:
        data = await reader.read(100)
        if not data:
            break

        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message} from {addr}")

        # Process the received data here, e.g., handle memcache commands

        writer.write(data)
        await writer.drain()

    print("Closing connection")
    writer.close()

async def start_server(host, port):
    server = await asyncio.start_server(
        handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server Example")
    parser.add_argument("--port", type=int, default=11211, help="Port to listen on")
    args = parser.parse_args()

    host = "localhost"
    port = args.port

    asyncio.run(start_server(host, port))

