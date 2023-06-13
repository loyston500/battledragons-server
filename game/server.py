from ursina import *

from fastapi import FastAPI, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import threading
from functools import partial
import uvicorn

from game.sprites import *
from game.rng import rng
import game.assets
import game.battledragons
from game.battledragons import users

app = FastAPI()

app.mount(
    "/site",
    StaticFiles(directory="../battledragons/build/web", html=True),
    name="site",
)


class DummyUser:
    def __init__(self, password=None, websocket=None):
        self.password = password
        self.websocket = websocket


@app.post("/rest/check_account_exist")
async def check_account_exist(req: Request):
    data = await req.json()
    print(data)

    match data:
        case {"username": username}:
            print("done 1", username in users)
            return dict(result=username in users)


@app.post("/rest/create_account")
async def create_account(req: Request):
    data = await req.json()
    print(data)

    match data:
        case {"username": username, "password": password}:
            if username in users:
                return dict(result="already_exists")

            if not username.isalnum():
                return dict(result="bad_username")

            users[username] = DummyUser(password=password)

            print("account created")
            return dict(result="account_created")


@app.get("/rest/create_random_bot")
@app.post("/rest/create_random_bot")
async def create_random_bot(username: str = None):
    player = Bot(
        name=rng.choice(game.assets.dragons),
        scale=1,
        xv=rng.random() * 2 - 1,
        yv=rng.random() * 2 - 1,
        collider="box",
        hp=30,
        username=username,
    )


@app.post("/rest/pass_check")
async def pass_check(req: Request):
    data = await req.json()
    print(data)

    match data:
        case {"username": username, "password": password}:
            if username not in users:
                return dict(result="does_not_exist")
            if users[username].password == password:
                return dict(result="possible")
            else:
                return dict(result="not_possible")


@app.post("/rest/give_up")
async def give_up(req: Request):
    data = await req.json()
    print(data)

    match data:
        case {"username": username, "password": password}:
            if username not in users:
                return dict(result="does_not_exist")
            if users[username].password == password and isinstance(
                users[username], User
            ):
                users[username].give_up()
                users[username] = DummyUser(users[username].password)
                return dict(result="success")
            else:
                return dict(result="not_possible")


@app.post("/rest/move")
async def move(req: Request):
    data = await req.json()

    print(data)

    match data:
        case {"username": username, "password": password, "direction": direction}:
            if username not in users:
                return dict(result="does_not_exist")
            if users[username].password == password and isinstance(
                users[username], User
            ):
                user = users[username]

                match direction:
                    case "^":
                        if user.yv < 0:
                            user.yv = -user.yv
                    case "v":
                        if user.yv > 0:
                            user.yv = -user.yv
                    case "<":
                        if user.xv > 0:
                            user.xv = -user.xv
                    case ">":
                        if user.xv < 0:
                            user.xv = -user.xv
                return dict(result="success")
            else:
                return dict(result="not_possible")


@app.post("/rest/spawn_user")
async def spawn_user(req: Request):
    data = await req.json()
    print(data)

    match data:
        case {"username": username, "password": password, "hp": hp, "dragon": dragon}:
            if username in users and users[username].password == password:
                if isinstance(users[username], DummyUser):
                    users[username] = User(
                        username=username,
                        password=password,
                        hp=hp,
                        name=game.assets.dragons_map[dragon],
                        xv=(0.7 + rng.random()) * rng.choice([1, -1]),
                        yv=(0.7 + rng.random()) * rng.choice([1, -1]),
                    )
                    return dict(result="success")
                else:
                    return dict(result="already_spawned")
            else:
                return dict(result="does_not_exist_or_wrong_password")


class ConnectionManager:
    def __init__(self):
        self.active_users = []

    async def connect(self, websocket: WebSocket, username, password):
        if username in users and users[username].password == password:
            user = users[username]
            user.websocket = websocket

            await websocket.accept()
            self.active_users.append(user)
            return user
        else:
            raise ValueError("username does not exist or wrong password")

    def disconnect(self, user):
        user.websocket = None
        self.active_users.remove(user)

    async def send(self, message: str, user):
        await user.websocket.send_text(message)

    async def broadcast(self, message: str):
        for user in self.active_users:
            await user.websocket.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str, password: str):
    user = await manager.connect(websocket, username, password)

    try:
        while True:
            data = await user.websocket.receive_text()
            data = json.loads(data)

    except WebSocketDisconnect:
        manager.disconnect(user)
        await manager.broadcast(
            json.dumps({"global_msg": f"{user.username} left the game"})
        )


def run_app(host, port):
    print("fastapi running")
    uvicorn.run(app, host=host, port=port)


def run(host, port):
    thread = threading.Thread(target=partial(run_app, host, port), daemon=True)
    thread.start()
