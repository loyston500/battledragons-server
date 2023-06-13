import game.assets
from game.rng import rng

with open(game.assets.misc_path + "/words.txt") as file:
    random_usernames = file.read().splitlines()


def generate_random_username(*args, **kwargs):
    return "".join(
        [word.title() for word in rng.choices(random_usernames, k=2)]
        + [str(rng.randint(500, 9999))]
    )
