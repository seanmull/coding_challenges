import aiohttp
import asyncio
import argparse
from utils import serialize_resp

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Sends requests to redis server")

parser.add_argument("cmd", type=str, help="cmd")

parser.add_argument("key", type=str, nargs="?", help="data")

parser.add_argument("value", type=str, nargs="?", help="data")

parser.add_argument(
    "-seconds",
    "--EX",
    type=str,
    nargs="?",
    help="Enter timeout for setting key value in seconds",
)

parser.add_argument(
    "-milliseconds",
    "--PX",
    nargs="?",
    help="Enter timeout for setting key value seconds",
)

parser.add_argument(
    "-unix-seconds",
    "--EXAT",
    nargs="?",
    help="Enter timeout for setting key value in seconds unix time",
)

parser.add_argument(
    "-unix-milliseconds",
    "--PXAT",
    nargs="?",
    help="Enter timeout for setting key value in milliseconds unix time",
)

args = parser.parse_args()

delay = {"is_millisecond": "", "is_unixtime": "", "time_delay": 0}

if args.cmd == "set":
    count = 0
    for i in [args.EX, args.PX, args.EXAT, args.PXAT]:
        if i:
            count += 1
    if count > 1:
        print("More then one delay selected. Not allowed.")
        exit()
    elif count == 1:
        if args.EX:
            delay["time_delay"] = args.EX
        elif args.PX:
            delay["time_delay"] = args.PX
            delay["is_millisecond"] = "True"
        elif args.EXAT:
            delay["time_delay"] = args.EXAT
            delay["is_unixtime"] = "True"
        elif args.PXAT:
            delay["time_delay"] = args.PXAT
            delay["is_millisecond"] = "True"
            delay["is_unixtime"] = "True"
    elif count == 0: 
        delay = None
else:
    delay = None

async def fetch(session, url, cmd, key, value):
    bulk_array = []
    if not key and not value:
        bulk_array = [cmd]
    elif not value:
        bulk_array = [cmd, key]
    else:
        bulk_array = [cmd, key, value]
    params = {"request": serialize_resp(bulk_array)}
    if delay:
        params["is_millisecond"] = delay["is_millisecond"]
        params["is_unixtime"] = delay["is_unixtime"]
        params["time_delay"] = delay["time_delay"]
    async with session.get(url, params=params) as response:
        return await response.text()


async def main():
    url = "http://localhost:6379"

    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url, args.cmd, args.key, args.value)
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
