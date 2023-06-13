from ursina import *


from game.sprites import *
import game.assets
from game.rng import rng

import typing as t
from PIL import Image
from random import Random
import json

app = Ursina()

players: list[Dragon] = []

users = {}

food = []

enemies = []

background = Background(texture=game.assets.background, scale=2, position=(0, 2.5, 1))

right_walls = [
    RightWall(
        texture=game.assets.wall1,
        collider="box",
        scale=3,
        position=(7, 6 - 2.8 * n),
        rotation=(0, 0, 90),
    )
    for n in range(0, 6)
]

left_walls = [
    LeftWall(
        texture=game.assets.wall1,
        collider="box",
        scale=3,
        position=(-7, 6 - 2.8 * n),
        rotation=(0, 0, 270),
    )
    for n in range(0, 7)
]

top_walls = [
    TopWall(
        texture=game.assets.wall1,
        collider="box",
        scale=3,
        position=(6 - 2.8 * n, 4),
        rotation=(0, 0, 0),
    )
    for n in range(0, 6)
]

bottom_walls = [
    BottomWall(
        texture=game.assets.wall1,
        collider="box",
        scale=3,
        position=(6 - 2.8 * n, -4),
    )
    for n in range(0, 6)
]


def add_player(
    pos=(50, 50),
    name=None,
    texture=None,
    hp=30,
    bot=False,
):
    player = (Bot if bot else User)(
        name=texture,
        scale=1,
        xv=rng.random() * 2 - 1,
        yv=rng.random() * 2 - 1,
        collider="box",
        hp=hp,
    )
    players.append(player)


def input(key):
    # test
    if key == "r":
        add_player(
            texture=rng.choice(game.assets.dragons), bot=True, hp=rng.randint(3, 7)
        )
    if key == "f":
        food.append(
            Food(
                texture=rng.choice(game.assets.food),
                position=(rng.randint(-5, 5), rng.randint(-3, 3), 0),
                hp=2,
            )
        )

    if key == "e":
        enemies.append(
            Enemy(
                texture=rng.choice(game.assets.enemies),
                position=(rng.randint(-5, 5), rng.randint(-3, 3), 0),
                hp=-3,
            )
        )
