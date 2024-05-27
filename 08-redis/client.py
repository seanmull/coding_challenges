import aiohttp
import asyncio
import argparse
from utils import serialize_resp

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Sends requests to redis server")

parser.add_argument("cmd", type=str, help="cmd")

parser.add_argument("key", type=str, nargs="?", help="data")

parser.add_argument("value", type=str, nargs="?", help="data")

args = parser.parse_args()


async def fetch(session, url, cmd, key, value):
    bulk_array = []
    if not key and not value:
        bulk_array = [cmd]
    elif not value:
        bulk_array = [cmd, key]
    else:
        bulk_array = [cmd, key, value]
    params = {"request": serialize_resp(bulk_array)}
    async with session.get(url, params=params) as response:
        return await response.text()


async def main():
    url = "http://localhost:6379"

    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url, args.cmd, args.key, args.value)
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
