from ursina import *

import config
import server
import game.battlebounce
from game.battlebounce import *

server.run(game.battlebounce.server_handler)
game.battlebounce.app.run()


def input(key):
    # test
    if key == "r":
        add_player()
