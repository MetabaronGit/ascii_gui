import random

standart_combat = ["hit", "wound", "power", "miss", "event", "miss"]
turbo_laser = ["hit", "double_hit", "triple_hit", "overheat", "overheat", "miss"]
SCREEN_WIDTH = 100


def roll_dice(dice: list, number=1) -> list:
    return [random.choice(dice) for x in range(number)]


print("-" * SCREEN_WIDTH)
print("combat roll")
print("-" * SCREEN_WIDTH)
print(f"{roll_dice(standart_combat, 6)}")
print(f"{roll_dice(turbo_laser)}")
final_roll = roll_dice(standart_combat, 6) + roll_dice(turbo_laser)
print(final_roll)


def draw_control_panel(mech):
    tab_separator = "+" + "-" * SCREEN_WIDTH + "+"
    tab_reductor = 38
    print(tab_separator)
    print(f"| {mech:<{SCREEN_WIDTH - 1}}|")
    print(tab_separator)
    print("| HP     9/10 [ |||||||||   ]" + " " * 72 + "|")
    print("| power  3/10 [ |||         ]" + " " * 72 + "|")
    print(tab_separator)
    print("| {:<5} | {:<25} | {:<{}} |".format("power", "action", "effect", SCREEN_WIDTH - tab_reductor))
    print(tab_separator)
    print("| {:^5} | {:<25} | {:<{}} |".format("3", "weapon booster", "from one hit make double_hit", SCREEN_WIDTH - tab_reductor))
    print("| {:^5} | {:<25} | {:<{}} |".format("4", "auto repair", "repair 2 HP", SCREEN_WIDTH - tab_reductor))
    print(tab_separator)

    print("| {:<20} | {:<{}} |".format("equipment", "effect", SCREEN_WIDTH - 25))
    print(tab_separator)
    print("| {:<20} | {:<{}} |".format("turbolaser", "in combat add turbolaser dice", SCREEN_WIDTH - 25))
    print("| {:<20} | {:<{}} |".format("ion shield", "on first turn of combat, change up to 3 wounds to miss", SCREEN_WIDTH - 25))
    print(tab_separator)

draw_control_panel("Jaeger Mk.1")