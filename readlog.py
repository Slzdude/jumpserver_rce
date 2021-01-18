import asyncio
import re

import websockets
import json

url = "/ws/ops/tasks/log/"


async def main_logic(t):
    print("#######start ws")
    async with websockets.connect(t) as client:
        await client.send(json.dumps({"task": "../../logs/jumpserver"}))
        while True:
            ret = json.loads(await client.recv())
            print(ret["message"], end="")


async def read_gunicorn(t):
    print("#######start ws")
    clean_pattern = re.compile(r"^.+?/(?:v1/terminal/terminals/|health/).+?$", re.M | re.I)
    async with websockets.connect(t) as client:
        await client.send(json.dumps({"task": "../../logs/gunicorn"}))
        while True:
            ret = json.loads(await client.recv())
            print(clean_pattern.sub(ret["message"], ""), end="")


if __name__ == "__main__":
    host = "localhost"
    cmd = "whoami"
    print("##################")
    target = host.replace("https://", "wss://").replace("http://", "ws://") + url
    print("target: %s" % (target,))
    asyncio.get_event_loop().run_until_complete(main_logic(target))
