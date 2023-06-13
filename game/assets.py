import os

dragons_path = "game/assets/dragons"

dragons = [f"{dragons_path}/{name}" for name in os.listdir(dragons_path)]

print("\n".join(dragons))

dragons_map = {
    name.removesuffix(".gif"): f"{dragons_path}/{name}"
    for name in os.listdir(dragons_path)
}
print(dragons_map)

dragons1 = [
    "game/assets/dragons/PygmyWyvernIdleSide.gif",
    "game/assets/dragons/JuvenileBrassDragonIdleSide.gif",
    "game/assets/dragons/BabyWhiteDragonIdleSide.gif",
]

enemy_path = "game/assets/enemies"
enemies = [f"{enemy_path}/{name}" for name in os.listdir(enemy_path)]


food_path = "game/assets/food"

food = [f"{food_path}/{name}" for name in os.listdir(food_path)]
print(food)

wall1 = "game/assets/walls/wall1.png"

background = "game/assets/backgrounds/Background.png"

attacks_path = "game/assets/attacks"

attacks = [f"{attacks_path}/{name}" for name in os.listdir(attacks_path)]

fonts_path = "game/assets/fonts"

fonts = [f"{fonts_path}/{name}" for name in os.listdir(fonts_path)]

misc_path = "game/assets/misc"

death1 = "game/assets/death/death1.gif"

print(fonts)
