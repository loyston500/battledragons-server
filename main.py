from ursina import *

import config
import game.battledragons
import game.server
from game.battledragons import *

game.server.run("", config.port)

if not config.only_run_server:
    game.battledragons.app.run()
else:
    while True:
        pass
