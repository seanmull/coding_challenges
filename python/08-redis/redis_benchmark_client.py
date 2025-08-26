import utils
import asyncio
import aiohttp
import time

number_of_concurrent_requests = 10000
set_commands = "set hello world"
get_commands = "get hello"

serialized_set_commands = utils.serialize_commands(set_commands)
serialized_get_commands = utils.serialize_commands(get_commands)

headers = {"Content-Type": "application/json"}


async def make_post_request(session, commands, headers):
    try:
        async with session.post('http://localhost:6380', json={'commands': commands}, headers=headers) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f'HTTP request failed: {e}')
        return None


async def main():
    async with aiohttp.ClientSession() as session:
        set_start_time = time.time()
        tasks = [
            make_post_request(session, serialized_set_commands, headers)
            for _ in range(number_of_concurrent_requests)
        ]

        await asyncio.gather(*tasks)
        set_end_time = time.time()
        print(
            f'SET: {int(number_of_concurrent_requests / (set_end_time - set_start_time))} number of requests')

        get_start_time = time.time()
        tasks = [
            make_post_request(session, serialized_get_commands, headers)
            for _ in range(number_of_concurrent_requests)
        ]

        await asyncio.gather(*tasks)
        get_end_time = time.time()
        print(
            f'GET: {int(number_of_concurrent_requests / (get_end_time - get_start_time))} number of requests')

asyncio.run(main())
