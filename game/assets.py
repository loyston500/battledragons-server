import os

dragons_path = "game/assets/dragons"

dragons = [f"{dragons_path}/{name}" for name in os.listdir(dragons_path)]

dragons1 = [
    "game/assets/dragons/PygmyWyvernIdleSide.gif",
    "game/assets/dragons/JuvenileBrassDragonIdleSide.gif",
    "game/assets/dragons/BabyWhiteDragonIdleSide.gif",
]


wall1 = "game/assets/walls/wall1.png"

background = "game/assets/backgrounds/Background.png"

attacks_path = "game/assets/attacks"

attacks = [f"{attacks_path}/{name}" for name in os.listdir(attacks_path)]
