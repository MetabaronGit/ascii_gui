import pygame

pygame.init()
pygame.font.init()

FONT_SIZE_PX = 18
CONSOLE_FONT = pygame.font.Font('lucon.ttf', FONT_SIZE_PX)
CONSOLE_FONT_WIDTH_PX, CONSOLE_FONT_HEIGHT_PX = CONSOLE_FONT.size("-")
LINE_SPACING_PX = 5

SCREEN_WIDTH_PX = 540  # original=540
SCREEN_HEIGHT_PX = 780  # original=960
SCREEN = pygame.display.set_mode((SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX))

TEXT_COLOR = (0, 200, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
DARKEST_GREEN = (0, 50, 0)
LIGHT_GREEN = (0, 255, 0)
CURSOR_COLOR = (0, 100, 0)

VARIABLE_NAMES = ["POWER", "COMBAT", "MUNITION",
                  "COMMAND", "DEFENCE", "VP",
                  "POISON", "SUPPLY", "DECK"]

MAX_VISIBLE_ACTIONS = 6


class PlayerVariable:
    # name_index=None -> nepouziva se, value= -1 -> unlimited, max_value=-1 -> unlimited
    def __init__(self, name_index: any, value=0, max_value=-1):
        if name_index is not None:
            self.__name = VARIABLE_NAMES[name_index]
        else:
            self.__name = None
        self.__value = value
        self.__max_value = max_value

    def get_name(self) -> str:
        return self.__name

    def get_value(self) -> int:
        return self.__value

    def get_max_value(self) -> int:
        return self.__max_value

    def increase_value(self, amount: int) -> None:
        self.__value += amount
        if self.__max_value != -1 and self.__value > self.__max_value:
            self.__value = self.__max_value

    def decrease_value(self, amount: int) -> None:
        if self.__value != -1:
            self.__value -= amount
            if self.__value < 0:
                self.__value = 0


class Player:
    def __init__(self, name: str):
        self.__name = name
        self.__tab_lines = 3
        self.__stats = dict()

        if name == "Necron Lord":
            self.__stats[VARIABLE_NAMES[0]] = PlayerVariable(0, 20, 20)  # power
            self.__stats[VARIABLE_NAMES[1]] = PlayerVariable(1)          # combat
            self.__stats[VARIABLE_NAMES[2]] = PlayerVariable(2, 2)       # munition
            self.__stats[VARIABLE_NAMES[3]] = PlayerVariable(3, -1)      # command
            self.__stats[VARIABLE_NAMES[4]] = PlayerVariable(4)          # defence
            self.__stats[VARIABLE_NAMES[5]] = PlayerVariable(5)          # vp
            self.__stats[VARIABLE_NAMES[6]] = PlayerVariable(None, -1)   # poison
            self.__stats[VARIABLE_NAMES[7]] = PlayerVariable(7, 20)      # supply
            self.__stats[VARIABLE_NAMES[8]] = PlayerVariable(8, 10, 10)  # deck

    def get_variable_value(self, key: str) -> int:
        if self.__stats.get(key):
            return self.__stats.get(key).get_value()
        else:
            return ""

    def get_max_variable_value(self, key: str) -> int:
        if self.__stats.get(key):
            return self.__stats.get(key).get_max_value()
        else:
            return ""

    def get_variable_name(self, key) -> str:
        return self.__stats[key].get_name()

    def get_stats_names(self) -> list:
        return list(self.__stats.keys())

    def get_name(self):
        return self.__name

    def get_tab_lines(self):
        return self.__tab_lines


class Action:
    def __init__(self, name: str, base_manner="x", description=[], base_price=[], discard=False):
        self.__name = name
        self.__base_manner = base_manner
        self.__actual_manner = base_manner
        self.__description = description
        self.__base_price = base_price
        self.__actual_price = base_price
        self.__discard = discard

    def get_name(self):
        return self.__name

    def discard_after_use(self):
        return self.__discard

    def get_base_manner(self):
        return self.__base_manner

    def get_actual_manner(self):
        return self.__actual_manner

    def get_actual_price_list(self) -> list:
        # vrací list tuplů ("jméno proměnné", hodnota)
        return self.__actual_price

    def get_description(self) -> list:
        # vrací list stringů s popisem akce. každý řádek je jeden index v listu
        return self.__description


class Card:
    def __init__(self, name: str, type="event", base_power=0, condition="", image="img_00.jpg", image_shift=0,
                 bounty="", actions=[]):
        self.__name = name
        self.__condition = condition
        self.__actions = actions
        # ToDo: kontrola, jestli obrázek existuje, jinak bude img_00.jpg
        self.__image = "images/" + image
        self.__image_shift = image_shift
        self.__type = type
        self.__base_power = base_power
        self.__actual_power = base_power
        self.__bounty = bounty

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def get_image(self):
        return self.__image

    def get_condition(self):
        return self.__condition

    def get_image_shift(self):
        return self.__image_shift

    def get_actual_power(self):
        return self.__actual_power

    def get_bounty(self):
        return self.__bounty

    def get_base_power(self):
        return self.__base_power

    def get_actions(self) -> list:
        return self.__actions.copy()


def print_card(card):
    # nad prvnim radkem textu je pulradek odsazeni
    y = CONSOLE_FONT_HEIGHT_PX // 2

    if card.get_type() == "enemy":
        print_text(card.get_name(), y, color=WHITE, center=True)
        y += CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX
        print_text(f"power: {card.get_actual_power()}", y, color=WHITE, center=True)

    if card.get_type() == "event":
        y += CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX
        print_text(card.get_name(), y, color=WHITE, center=True)

    # obrazek vycentrovany na ose x
    y -= card.get_image_shift()
    card_img = pygame.image.load(card.get_image())
    SCREEN.blit(card_img, (SCREEN_WIDTH_PX // 2 - card_img.get_width() // 2,
                           y + CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX))

    if card.get_condition():
        y += CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX * 2 + card_img.get_height()
        print_text(card.get_condition(), y, color=LIGHT_GREEN, center=True)

    if card.get_bounty():
        y += CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX
        print_text(card.get_bounty(), y, color=LIGHT_GREEN, center=True)


def print_text(text_string, y, x=0, color=TEXT_COLOR, background_color=None, center=False):
    text = CONSOLE_FONT.render(text_string, True, color, background_color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH_PX // 2, y))
    text_rect.y = y

    if not center:
        text_rect.x = x

    SCREEN.blit(text, text_rect)


# ToDo: barva kurzoru a zvýraznění textu nad ním
def draw_cursor(player: Player, cursor_position):
    y = SCREEN_HEIGHT_PX - (int(player.get_tab_lines()) * 2 + 4) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)
    y -= MAX_VISIBLE_ACTIONS * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) + CONSOLE_FONT_HEIGHT_PX / 2
    y += (cursor_position + 1) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) + LINE_SPACING_PX
    print_text(" " * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX), y, background_color=CURSOR_COLOR)


def print_action_console(player, action_list: list, cursor_position: int, max_cursor_position: int):
    y = SCREEN_HEIGHT_PX - (int(player.get_tab_lines()) * 2 + 4) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)
    y -= MAX_VISIBLE_ACTIONS * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) + CONSOLE_FONT_HEIGHT_PX / 2

    text = "=< actions >" + "=" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX - 15)
    print_text(text, y, color=DARK_GREEN)

    if cursor_position > 0:
        color = WHITE
    else:
        color = DARKEST_GREEN
    print_text("^", y, SCREEN_WIDTH_PX - CONSOLE_FONT_WIDTH_PX * 3, color=color)

    if (cursor_position + len(action_list) - 1) < max_cursor_position:
        color = WHITE
    else:
        color = DARKEST_GREEN
    print_text("v", y, SCREEN_WIDTH_PX - CONSOLE_FONT_WIDTH_PX * 2, color=color)

    print_text("=", y, SCREEN_WIDTH_PX - CONSOLE_FONT_WIDTH_PX, color=DARK_GREEN)

    y += LINE_SPACING_PX
    for i, action in enumerate(action_list, 1):
        text = f" [{action.get_actual_manner()}]"

        if text == " [ ]":
            text_color = DARKEST_GREEN
        else:
            text_color = TEXT_COLOR

        if action.discard_after_use():
            text += "[DISCARD]"
        for price in action.get_actual_price_list():
            text += f"[{price[1]} {price[0]}]"
        text += f" {action.get_name()}"
        print_text(text, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * i, color=text_color)


def print_action_description(text_lines: list) -> None:
    # vypíše popis akce
    if len(text_lines) == 1:
        y = SCREEN_HEIGHT_PX - LINE_SPACING_PX - (FONT_SIZE_PX + LINE_SPACING_PX) * 1.5
    else:
        y = SCREEN_HEIGHT_PX - LINE_SPACING_PX - (FONT_SIZE_PX + LINE_SPACING_PX) * 1.9

    for line in text_lines:
        print_text(line, y, color=WHITE, center=True)
        y += FONT_SIZE_PX + LINE_SPACING_PX


def print_player_stats(player):
    tab_columns = 3  # při změně šířky SCREEN_WIDTH se mění jen šířka sloupců
    tab_column_width_chars = SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX // tab_columns

    # muzeme pridavat ci ubirat v objektu Player podle poctu zobrazovanych hodnot
    tab_lines = int(player.get_tab_lines())

    # umisteni se pocita od spodniho okraje SCREENu nad popisky vybranych akci
    y = SCREEN_HEIGHT_PX - (tab_lines * 2 + 4) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)

    # draw empty stats tab
    text = "=< stats >" + "=" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX - 10)
    print_text(text, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX), color=DARK_GREEN)

    free_fields = f"{'':>{tab_column_width_chars}}|{'':>{tab_column_width_chars}}|"
    separator = f"{'':->{tab_column_width_chars}}+{'':->{tab_column_width_chars}}+" + \
                "-" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX - tab_column_width_chars * 2 - 2)

    for i in range(2, tab_lines * 2 + 1, 2):
        print_text(free_fields, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * i, color=DARK_GREEN)
        if i == tab_lines * 2:
            separator = "=" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX)
        print_text(separator, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * (i + 1), color=DARK_GREEN)

    # draw stats values

    # umisteni se pocita od spodniho okraje SCREENu nad popisky vybranych akci
    x = CONSOLE_FONT_WIDTH_PX
    y = SCREEN_HEIGHT_PX - (tab_lines * 2 + 2) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)
    for n, item in enumerate(player.get_stats_names(), 1):
        if player.get_variable_name(item) == None:
            text = ""
        else:
            if player.get_variable_value(item) != -1:
                text = f"{item}: {player.get_variable_value(item)}"
            else:
                text = f"{item}: ∞"
            if player.get_max_variable_value(item) != -1:
                text += f"/{player.get_max_variable_value(item)}"
        print_text(text, y, x=x)
        x += tab_column_width_chars * CONSOLE_FONT_WIDTH_PX + CONSOLE_FONT_WIDTH_PX

        if n % tab_columns == 0:
            x = CONSOLE_FONT_WIDTH_PX
            y += (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * 2


def get_visible_actions(total_actions: list, total_actions_cursor_position: int) -> list:
    result = []
    for i, item in enumerate(total_actions[total_actions_cursor_position:]):
        if i > MAX_VISIBLE_ACTIONS - 1:
            break
        else:
            result.append(item)
    return result


def main():
    pygame.display.set_caption("the quest - technological demo, since 04.2021")

    player = Player("Necron Lord")

    card1 = Card("Ambient card", condition="event", bounty="second line", image="img_21_test.jpg",
                 actions=[Action("pass", "x", ["continue"])]
                 )

    card2 = Card("Event card test", image="testImg_540x300.png", condition="card ability text line one",
                 image_shift=20,
                 actions=[Action("pass"),
                          Action("fire support", "+", ["deal DAMAGE 3"], base_price=[("MUNITION", 2), ("COMMAND", 3)])]
                 )

    card3 = Card("Enemy card test", type="enemy", base_power=5, image="img_03.jpg",
                 condition="card ability text line one", bounty="VP, COMMAND",
                 actions=[Action("pass", "x", ["continue"]),
                          Action("reinforcements", "+", ["SUPPLY - 2 and DEFENCE + 1"]),
                          Action("fire support", "+", ["deal DAMAGE 3"], base_price=[("MUNITION", 2)])]
                 )

    card4 = Card("Tomb of tests", type="event", image="img_12.jpg",
                 condition="event",
                 actions=[Action("secret passage", "+", ["double any gains here"], base_price=[(VARIABLE_NAMES[3], 1)]),
                          Action("pass", "x", ["VP + 50"]),
                          Action("second pass", " ", ["double your VP", "and SUPPLY + 1"], discard=True),
                          Action(f"take {VARIABLE_NAMES[2]}", "x", [f"{VARIABLE_NAMES[2]} + 2"]),
                          Action(f"take {VARIABLE_NAMES[7]}", "x", [f"{VARIABLE_NAMES[7]} + 2"]),
                          Action("reforge", "R", [f"{VARIABLE_NAMES[2]} + 2"], base_price=[(VARIABLE_NAMES[7], 2)]),
                          Action("heal poison", " ", [f"remove all {VARIABLE_NAMES[6]}"], base_price=[(VARIABLE_NAMES[0], 2)]),
                          Action(f"spare {VARIABLE_NAMES[2]}", "x", ["put card back to the deck", "and shuffle it"], base_price=[(VARIABLE_NAMES[2], 4)])]
                          # next time when will be draw, automaticly add 4 MUNITION
                 )

    card_01 = Card("Energetic weaponry", type="event", image="img_20.jpg", condition="event",
                   actions=[Action("use", "x", ["all other your units with COMBAT", "have + 1 COMBAT bonus"], base_price=[(VARIABLE_NAMES[7], 6)]),
                            Action("take SUPPLY", "x", ["SUPPLY + 4"]),
                            Action("initiative", "x", ["VP + 5"])]
                   )

    card_02 = Card("Supply tomb", type="event", image="img_12.jpg", condition="event",
                   actions=[Action("reforge", "R", ["MUNITION + 2"],
                                   base_price=[(VARIABLE_NAMES[7], 2)]),
                            Action("take SUPPLY", "x", ["SUPPLY + 3"]),
                            Action("initiative", "x", ["VP + 5"])]
                   )

    total_actions = []
    visible_actions = []
    game_over = False

    # draw new card
    # ToDo: odečet počtu karet z DECKu
    actual_card = card_02

    # prvotní vytvoření listu všech dostupných akcí
    total_actions_cursor_position = 0
    total_actions = actual_card.get_actions()
    # total_actions.append(players action list)

    # kontrola vlastností akcí

    # prvotní vytvoření listu viditelných akcí
    visible_actions_cursor_position = 0
    visible_actions = get_visible_actions(total_actions, total_actions_cursor_position)


    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    game_over = True

                if event.key == pygame.K_DOWN:
                    if visible_actions_cursor_position < len(visible_actions) - 1:
                        visible_actions_cursor_position += 1
                    elif visible_actions_cursor_position == len(visible_actions) - 1:
                        if visible_actions_cursor_position + total_actions_cursor_position < len(total_actions) - 1:
                            total_actions_cursor_position += 1
                            visible_actions = get_visible_actions(total_actions, total_actions_cursor_position)

                if event.key == pygame.K_UP:
                    if visible_actions_cursor_position > 0:
                        visible_actions_cursor_position -= 1
                    elif visible_actions_cursor_position == 0:
                        if visible_actions_cursor_position + total_actions_cursor_position > 0:
                            total_actions_cursor_position -= 1
                            visible_actions = get_visible_actions(total_actions, total_actions_cursor_position)

                # if event.key == pygame.K_1 or event.key == pygame.K_KP1:  # NUM 1
                #     cursor_position = 0

                # if event.key == pygame.K_2 or event.key == pygame.K_KP2:  # NUM 2
                #     cursor_position = 1

                SCREEN.fill((0, 0, 0))

                print_card(actual_card)

                draw_cursor(player, visible_actions_cursor_position)
                print_action_console(player, visible_actions, total_actions_cursor_position, len(total_actions) - 1)

                print_action_description(visible_actions[visible_actions_cursor_position].get_description())
                print_player_stats(player)


            # zaviraci ikona okna X
            if event.type == pygame.QUIT:
                game_over = True

        pygame.display.flip()
        # pygame.display.update()
        # clock.tick(60)


if __name__ == "__main__":
    main()
