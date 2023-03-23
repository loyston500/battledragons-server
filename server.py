import asyncio
import websockets
import threading
from functools import partial
import config


def _callback(fun):
    print("server started")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws_server = websockets.serve(fun, "", config.port)

    loop.run_until_complete(ws_server)
    loop.run_forever()
    loop.close()


def run(fun):
    server = threading.Thread(target=partial(_callback, fun), daemon=True)
    server.start()
