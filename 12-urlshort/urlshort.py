from aiohttp import web
from utils import create_hash, add_to_cache, is_in_cache
import json
import string
import random


async def handle_post(request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        response = {"error": "Invalid JSON payload"}
        return web.Response(
            text=json.dumps(response, indent=4),
            content_type="application/json",
            status=400,
        )

    long_url = data.get("long_url")

    if long_url is None:
        response = {"error": "Please provide 'long_url'"}
        return web.Response(
            text=json.dumps(response, indent=4),
            content_type="application/json",
            status=400,
        )

    hash = create_hash(long_url)
    while is_in_cache(set_key="hash_set", set_value=hash):
        hash = create_hash(long_url + random.choice(string.ascii_letters))

    add_to_cache(set_key="hash_set", set_values=[hash])
    short_url = f"http://localhost:8080/{hash}"
    add_to_cache(key=long_url, value=short_url)
    response = {"message": "Added successfully"}

    response_text = json.dumps(response, indent=4)
    return web.Response(text=response_text, content_type="application/json")


async def init_app():
    app = web.Application()
    app.router.add_post("/", handle_post)
    return app


def main():
    app = init_app()
    web.run_app(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
