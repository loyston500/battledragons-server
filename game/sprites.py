from ursina import *

import game.assets
from game.rng import rng


class Background(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Player(Animation):
    def __init__(self, *args, xv=1, yv=1, **kwargs):
        self.xv = xv
        self.yv = yv
        self.attacking = False
        super().__init__(*args, **kwargs)

    def move(self):
        self.x += self.xv * time.dt
        self.y += self.yv * time.dt

    def update(self):
        hitinfo = self.intersects()
        if hitinfo.hit:
            if isinstance(hitinfo.entity, XWall):
                if isinstance(hitinfo.entity, LeftWall):
                    self.x = hitinfo.entity.x + 1
                else:
                    self.x = hitinfo.entity.x - 1
                self.xv *= -1

            elif isinstance(hitinfo.entity, YWall):
                if isinstance(hitinfo.entity, BottomWall):
                    self.y = hitinfo.entity.y + 1
                else:
                    self.y = hitinfo.entity.y - 1
                self.yv *= -1

            elif isinstance(hitinfo.entity, Player):
                if not self.attacking:
                    self.attacking = True
                    attack = Animation(
                        rng.choice(game.assets.attacks),
                        loop=False,
                        scale=1.2,
                        fps=30,
                        position=(
                            (self.x + hitinfo.entity.x) / 2,
                            (self.y + hitinfo.entity.y) / 2,
                            0,
                        ),
                    )
                    destroy(attack, delay=attack.duration)
        else:
            self.attacking = False

        self.move()


class Wall(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class YWall(Wall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class XWall(Wall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LeftWall(XWall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RightWall(XWall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TopWall(YWall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BottomWall(YWall):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
