import asyncio
import time
import aiohttp
# from scheduler import Scheduler
from scheduler.asyncio import Scheduler
import datetime as dt
import requests

# async def main():
#     start_time = time.time()
#     # print('Hello ...')
#     # time.sleep(2)
#     await asyncio.sleep(1)
#     await asyncio.sleep(1)
#     print('... World!')
#     print(f"Done in {time.time() - start_time} seconds")

# asyncio.run(main())

# async def fetch(url):
#     print("something")
#     reponse = requests.get("http://localhost:8081").text
#     pass


# async def main():
#     schedule = Scheduler()

#     schedule.cyclic(dt.timedelta(seconds=1), fetch)

#     while True:
#         await asyncio.sleep(1)


# asyncio.run(main())

import asyncio
import datetime as dt

from scheduler.asyncio import Scheduler

counter = 0

server_is_available = [["localhost:8081", True], ["localhost:8082", True], ["localhost:8083", True]]

async def update_servers_status():
    for i, server in enumerate(server_is_available):
        url, health_check = server
        response = None
        try:
            response = requests.get(f"http://{url}")
        except Exception:
            pass

        if response:
            server_is_available[i][1] = response.ok
        else:
            server_is_available[i][1] = False
    print(server_is_available)

async def scheduler():
    schedule = Scheduler()
    schedule.cyclic(dt.timedelta(seconds=5), update_servers_status)
    while True:
        await asyncio.sleep(5)


asyncio.run(scheduler())
