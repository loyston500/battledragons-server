from ursina import *


from game.sprites import *

import typing as t
from PIL import Image
from random import Random

app = Ursina()

rng = Random()
rng.seed(69)


players: t.List[Player] = []

left_wall = Wall(color=color.green, collider="box", scale=(0.6, 10), position=(7, 0))
right_wall = duplicate(left_wall, x=-7)


def add_player(
    pos=(50, 50),
    image=Image.new(size=(32, 32), color=(255, 200, 50, 255), mode="RGBA"),
    init_points=30,
):
    player = Player(
        scale_y=1,
        texture=Texture(image),
        xv=rng.random(),
        yv=rng.random(),
        collider="box",
    )
    players.append(player)


def input(key):
    # test
    if key == "r":
        add_player()


add_player()


async def server_handler(websocket, path):
    async for data in websocket:
        print(f"Received: '{data}'")
        await websocket.send(data)
        add_player()
