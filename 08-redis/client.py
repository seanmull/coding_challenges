import aiohttp
import asyncio
import argparse
import utils

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Sends requests to redis server")

parser.add_argument("cmd", type=str, help="cmd")

parser.add_argument("data", type=str, nargs="?", help="data")

args = parser.parse_args()


async def fetch(session, url, cmd, data):
    if not data:
        data = 0
    params = {"cmd": cmd, "data": data}
    async with session.get(url, params=params) as response:
        return await response.text()


async def main():
    url = "http://localhost:6379"

    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url, args.cmd, args.data)
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
