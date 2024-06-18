import asyncio
import argparse
import time

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
        elif command.startswith("add"):
            await handle_add(reader, writer, command)
        elif command.startswith("replace"):
            await handle_replace(reader, writer, command)
        elif command.startswith("append"):
            await handle_append(reader, writer, command)
        elif command.startswith("prepend"):
            await handle_prepend(reader, writer, command)

async def handle_set(reader, writer, command):
    parts = command.split()
    if len(parts) >= 5:
        key = parts[1]
        byte_count = int(parts[4])
        data = await reader.read(byte_count + 2)  # Include \r\n
        value = data[:-2].decode()  # Strip \r\n
        exptime = int(parts[3])

        if exptime <= 0:
            expire_time = None  # Expire immediately
        else:
            expire_time = time.time() + exptime  # Calculate expiry time

        cache[key] = (value, expire_time)

        if "noreply" not in parts:
            writer.write(b"STORED\r\n")
            await writer.drain()

async def handle_get(reader, writer, command):
    parts = command.split()
    if len(parts) >= 2:
        key = parts[1]
        data = cache.get(key)
        if data:
            value, expire_time = data
            if expire_time is None or time.time() < expire_time:
                response = f"VALUE {key} 0 {len(value)}\r\n{value}\r\n"
                writer.write(response.encode())
            else:
                del cache[key]  # Expired key, remove from cache

        writer.write(b"END\r\n")
        await writer.drain()

async def handle_add(reader, writer, command):
    parts = command.split()
    if len(parts) >= 5:
        key = parts[1]
        byte_count = int(parts[4])
        data = await reader.read(byte_count + 2)  # Include \r\n
        value = data[:-2].decode()  # Strip \r\n

        if key not in cache:
            cache[key] = (value, None)  # Add the key if it's not already there
            writer.write(b"STORED\r\n")
        else:
            writer.write(b"NOT_STORED\r\n")

        await writer.drain()

async def handle_replace(reader, writer, command):
    parts = command.split()
    if len(parts) >= 5:
        key = parts[1]
        byte_count = int(parts[4])
        data = await reader.read(byte_count + 2)  # Include \r\n
        value = data[:-2].decode()  # Strip \r\n

        if key in cache:
            cache[key] = (value, None)  # Replace the key if it's already there
            writer.write(b"STORED\r\n")
        else:
            writer.write(b"NOT_STORED\r\n")

        await writer.drain()

async def handle_append(reader, writer, command):
    parts = command.split()
    if len(parts) >= 5:
        key = parts[1]
        byte_count = int(parts[4])
        data = await reader.read(byte_count + 2)  # Include \r\n
        value = data[:-2].decode()  # Strip \r\n

        if key in cache:
            current_value, _ = cache[key]
            cache[key] = (current_value + value, None)  # Append to the value if key exists
            writer.write(b"STORED\r\n")
        else:
            writer.write(b"NOT_STORED\r\n")

        await writer.drain()

async def handle_prepend(reader, writer, command):
    parts = command.split()
    if len(parts) >= 5:
        key = parts[1]
        byte_count = int(parts[4])
        data = await reader.read(byte_count + 2)  # Include \r\n
        value = data[:-2].decode()  # Strip \r\n

        if key in cache:
            current_value, _ = cache[key]
            cache[key] = (value + current_value, None)  # Prepend to the value if key exists
            writer.write(b"STORED\r\n")
        else:
            writer.write(b"NOT_STORED\r\n")

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

