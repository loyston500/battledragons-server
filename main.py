from ursina import *

import config
import server
import game.battlebounce

server.run(game.battlebounce.server_handler)
game.battlebounce.app.run()
