from ursina import *

import game.assets
import game.utils
from game.rng import rng
import asyncio
import json


class FoodText(Text):
    def __init__(
        self,
        *args,
        font=game.assets.fonts[0],
        position=(0, 0, -1),
        scale=10,
        origin=(0, 0, 0),
        **kwargs,
    ):
        super().__init__(
            *args, font=font, position=position, scale=scale, origin=origin, **kwargs
        )


class Food(Sprite):
    def __init__(self, *args, collider="box", scale=4, hp=5, **kwargs):
        self.hp = hp
        super().__init__(*args, collider=collider, scale=scale, **kwargs)

        # self._text_sprite = FoodText()
        # self._text_sprite.parent = self

        # self._text_sprite.text = f"{self.hp}"


class Enemy(Food):
    def __init__(self, *args, scale=3, **kwargs):
        super().__init__(*args, scale=scale, **kwargs)


class Onion(Food):
    def __init__(self, *args, texture=game.assets.food[0], **kwargs):
        super().__init__(*args, texture=texture, **kwargs)


class Background(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DragonText(Text):
    def __init__(
        self,
        *args,
        font=game.assets.fonts[0],
        position=(0, 0, -1),
        scale=6,
        origin=(0, -4, 0),
        background=True,
        **kwargs,
    ):
        super().__init__(
            *args, font=font, position=position, scale=scale, origin=origin, **kwargs
        )


class Dragon(Animation):
    def __init__(
        self,
        *args,
        username,
        hp_color,
        hp=30,
        xv=None,
        yv=None,
        collider="box",
        scale=1,
        **kwargs,
    ):
        self.xv = xv
        self.yv = yv
        self.hp = hp
        self.hp_color = hp_color
        self.username = username
        self.attacking = False

        super().__init__(*args, collider=collider, scale=scale, **kwargs)

        self._text_sprite = DragonText()
        self._text_sprite.parent = self

    def move(self):
        try:
            self.x += self.xv * time.dt
            self.y += self.yv * time.dt
        except:
            pass

    def update(self):
        if self.hp <= 0:
            death = Animation(
                game.assets.death1,
                loop=False,
                scale=1.2,
                fps=30,
                position=(
                    self.x,
                    self.y,
                    0,
                ),
            )
            destroy(death, delay=death.duration)
            destroy(self)
            return

        try:
            self._text_sprite.text = (
                f"{self.username}  <{self.hp_color}> {self.hp} <{self.hp_color}>"
            )
        except AttributeError:
            self._text_sprite = DragonText()
            self._text_sprite.parent = self
            self._text_sprite.text = (
                f"{self.username}  <{self.hp_color}> {self.hp} <{self.hp_color}>"
            )

        try:
            hitinfo = self.intersects()
        except AssertionError:
            return
        if hitinfo.hit:
            if isinstance(hitinfo.entity, Food):
                if hitinfo.entity.hp > 0:
                    if rng.choice([True, False]):
                        Enemy(
                            texture=rng.choice(game.assets.enemies),
                            position=(rng.randint(-5, 5), rng.randint(-3, 3), 0),
                            hp=-3,
                        )
                else:
                    if rng.choice([True, False]):
                        Food(
                            texture=rng.choice(game.assets.food),
                            position=(rng.randint(-5, 5), rng.randint(-3, 3), 0),
                            hp=2,
                        )
                self.hp += hitinfo.entity.hp
                destroy(hitinfo.entity)

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

            elif isinstance(hitinfo.entity, Dragon):
                if not self.attacking:
                    hitinfo.entity.hp -= 1
                    if rng.choice([True, False]):
                        Food(
                            texture=rng.choice(game.assets.food),
                            position=(rng.randint(-5, 5), rng.randint(-3, 3), 0),
                            hp=2,
                        )
                    if isinstance(hitinfo.entity, User):
                        pass
                        # hitinfo.entity.inform()
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


class User(Dragon):
    def __init__(self, *args, hp_color="red", password=None, **kwargs):
        if password is None:
            raise ValueError("A password is required")

        self.password = password
        self.websocket = None
        super().__init__(*args, hp_color=hp_color, **kwargs)

    def inform(self):
        async def _inform():
            if self.websocket is not None:
                await self.websocket.send_text(json.dumps({"hp": self.hp}))
                print("informed")

        asyncio.run(_inform())

    def give_up(self):
        death = Animation(
            game.assets.death1,
            loop=False,
            scale=1.2,
            fps=30,
            position=(
                self.x,
                self.y,
                0,
            ),
        )
        destroy(death, delay=death.duration)
        destroy(self)


class Bot(Dragon):
    def __init__(self, *args, username=None, hp_color="blue", **kwargs):
        if username is None:
            username = game.utils.generate_random_username()
        super().__init__(*args, username=username, hp_color=hp_color, **kwargs)


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
