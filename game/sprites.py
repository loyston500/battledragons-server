from ursina import *


class Player(Sprite):
    def __init__(self, *args, xv=1, yv=1, **kwargs):
        self.xv = xv
        self.yv = yv
        super().__init__(*args, **kwargs)

    def move(self):
        self.x += self.xv * time.dt
        self.y += self.yv * time.dt

    def update(self):
        self.move()
        h = self.intersects()
        if h.hit:
            pass


class Wall(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
