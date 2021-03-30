import random

backgrounds = ["dark corridor", "rusted wall", "broken supports", "old statue", "long corridor", "open doors"]
foregrounds = ["old support", "empty boxes", "rubble", "rusted portal", "broken control panel"]
enemies = ["radioactive rat", "cultist", "bounty hunter"]

while True:
    print()
    print(f"background: {random.choice(backgrounds)}")
    print(f"foreground: {random.choice(foregrounds)}")
    print(f"enemy: {random.choice(enemies)}")
    print("-" * 40)
    print("actions:")
    print("[1] attack")
    print("[2] run")
    input()

