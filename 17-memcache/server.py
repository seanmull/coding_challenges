import asyncio
import argparse

cache = {}

async def handle_client(reader, writer):
    while True:
        data = await reader.readline()
        if not data:
            break

        command = data.decode().strip()
        if command.startswith("set"):
            await handle_set(reader, writer, command)
        elif command.startswith("get"):
            await handle_get(reader, writer, command)

async def handle_set(reader, writer, command):
    parts = command.split()
    if len(parts) >= 5:
        key = parts[1]
        byte_count = int(parts[4])
        data = await reader.read(byte_count + 2)  # Include \r\n
        value = data[:-2].decode()  # Strip \r\n
        cache[key] = value

        if "noreply" not in parts:
            writer.write(b"STORED\r\n")
            await writer.drain()

async def handle_get(reader, writer, command):
    parts = command.split()
    if len(parts) >= 2:
        key = parts[1]
        value = cache.get(key)
        if value:
            response = f"VALUE {key} 0 {len(value)}\r\n{value}\r\n"
            writer.write(response.encode())
            await writer.drain()

    writer.write(b"END\r\n")
    await writer.drain()

async def start_server(host, port):
    server = await asyncio.start_server(
        handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Memcache Server Example")
    parser.add_argument("--port", type=int, default=11211, help="Port to listen on")
    args = parser.parse_args()

    host = "localhost"
    port = args.port

    asyncio.run(start_server(host, port))

