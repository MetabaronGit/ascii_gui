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
LIGHT_GREEN = (0, 255, 0)
CURSOR_COLOR = (0, 100, 0)


class PlayerVariable:
    # name="NONE" -> nepouziva se, value= -1 -> unlimited, max_value=-1 -> unlimited
    def __init__(self, name: str, value=0, max_value=-1):
        self.__name = name
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

            # self.__var1 = PlayerValue("POWER", 20, 20)
            # self.__var2 = PlayerValue("COMBAT")
            # self.__var3 = PlayerValue("MUNITION", 2)
            # self.__var4 = PlayerValue("COMMAND", 4)
            # self.__var5 = PlayerValue("FORTIFICATION")
            # self.__var6 = PlayerValue("VP")
            # self.__var7 = PlayerValue("NONE", -1)
            # self.__var8 = PlayerValue("SUPPLY", 5)
            # self.__var9 = PlayerValue("DECK", 10, 10)
        self.__name = name
        self.__tab_lines = 3
        self.__stats = dict()
        if name == "Necron Lord":
        # self.__stats[self.__var1.get_name()] = self.__var1
        # self.__stats[self.__var2.get_name()] = self.__var2
        # self.__stats[self.__var3.get_name()] = self.__var3
        # self.__stats[self.__var4.get_name()] = self.__var4
        # self.__stats[self.__var5.get_name()] = self.__var5
        # self.__stats[self.__var6.get_name()] = self.__var6
        # self.__stats[self.__var7.get_name()] = self.__var7
        # self.__stats[self.__var8.get_name()] = self.__var8
        # self.__stats[self.__var9.get_name()] = self.__var9
            self.__stats["POWER"] = PlayerVariable("POWER", 20, 20)
            self.__stats["COMBAT"] = PlayerVariable("COMBAT")
            self.__stats["MUNITION"] = PlayerVariable("MUNITION", 2)
            self.__stats["COMMAND"] = PlayerVariable("COMMAND", 4)
            self.__stats["DEFENCES"] = PlayerVariable("DEFENCES")
            self.__stats["VP"] = PlayerVariable("VP")
            self.__stats["POISON"] = PlayerVariable("NONE", -1)
            self.__stats["SUPPLY"] = PlayerVariable("SUPPLY", 5)
            self.__stats["DECK"] = PlayerVariable("DECK", 10, 10)

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


class Card:
    def __init__(self, name:str, type="event", base_power=0, condition="", image="img_00.jpg", image_shift=0,
                 bounty=""):
        self.__name = name
        self.__condition = condition
        self.__actions = ["take MUNITION", "enlarge COMBAT", "pray for Omnisiah", "SCORE"]
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


class GameTable:
    def __init__(self):
        self.__name = "name"


def create_quest_deck():
    pass

# OK
def draw_card(card):
    # nad prvnim radkem textu je pulradek odsazeni
    y = CONSOLE_FONT_HEIGHT_PX // 2

    if card.get_type() == "enemy":
        draw_text(card.get_name(), y, color=WHITE, center=True)
        y += CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX
        draw_text(f"power: {card.get_actual_power()}", y, color=WHITE, center=True)

    if card.get_type() == "event":
        y += CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX
        draw_text(card.get_name(), y, color=WHITE, center=True)

    # obrazek vycentrovany na ose x
    # y = y - card1.get_image_shift()
    card_img = pygame.image.load(card.get_image())
    SCREEN.blit(card_img, (SCREEN_WIDTH_PX // 2 - card_img.get_width() // 2,
                           y + CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX))

    if card.get_condition():
        y += CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX * 2 + card_img.get_height()
        draw_text(card.get_condition(), y, color=LIGHT_GREEN, center=True)

    if card.get_bounty():
        y += CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX
        draw_text(card.get_bounty(), y, color=LIGHT_GREEN, center=True)


# OK
def draw_text(text_string, y, x=0, color=TEXT_COLOR, background_color=None, center=False):
    text = CONSOLE_FONT.render(text_string, True, color, background_color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH_PX // 2, y))
    text_rect.y = y

    if not center:
        text_rect.x = x

    SCREEN.blit(text, text_rect)


def draw_cursor(player: Player, actual_action, options: list):
    y = SCREEN_HEIGHT_PX - (int(player.get_variable_value("tab_lines")) * 2 + 4) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)
    y -= (len(options) + 1) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)
    draw_text(" " * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX),
              y + (actual_action + 1) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX), background_color=CURSOR_COLOR)


def draw_console(player):
    options = ["take MUNITION", "enlarge COMBAT", "pray for Omnisiah", "SCORE", "None", "special hero action"]
    y = SCREEN_HEIGHT_PX - (int(player.get_variable_value("tab_lines")) * 2 + 4) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)
    y -= (len(options) + 1) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)

    text = "=< actions >" + "=" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX - 12)
    draw_text(text, y, color=DARK_GREEN)

    for i, item in enumerate(options, 1):
        draw_text(f" [{i}] {item}", y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * i)


def draw_player_stats(player):
    tab_columns = 3  # při změně šířky SCREEN_WIDTH se mění jen šířka sloupců
    tab_column_width_chars = SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX // tab_columns

    # muzeme pridavat ci ubirat v objektu Player podle poctu zobrazovanych hodnot
    tab_lines = int(player.get_tab_lines())

    # umisteni se pocita od spodniho okraje SCREENu nad popisky vybranych akci
    y = SCREEN_HEIGHT_PX - (tab_lines * 2 + 4) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)

    # draw empty stats tab
    text = "=< stats >" + "=" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX - 10)
    draw_text(text, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX), color=DARK_GREEN)

    free_fields = f"{'':>{tab_column_width_chars}}|{'':>{tab_column_width_chars}}|"
    separator = f"{'':->{tab_column_width_chars}}+{'':->{tab_column_width_chars}}+" + \
                "-" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX - tab_column_width_chars * 2 - 2)

    for i in range(2, tab_lines * 2 + 1, 2):
        draw_text(free_fields, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * i, color=DARK_GREEN)
        if i == tab_lines * 2:
            separator = "=" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX)
        draw_text(separator, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * (i + 1), color=DARK_GREEN)

    # draw stats values

    # umisteni se pocita od spodniho okraje SCREENu nad popisky vybranych akci
    x = CONSOLE_FONT_WIDTH_PX
    y = SCREEN_HEIGHT_PX - (tab_lines * 2 + 2) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)
    for n, item in enumerate(player.get_stats_names(), 1):
        if player.get_variable_name(item) == "NONE":
            text = ""
        else:
            text = f"{item}: {player.get_variable_value(item)}"
        draw_text(text, y, x=x)
        x += tab_column_width_chars * CONSOLE_FONT_WIDTH_PX + CONSOLE_FONT_WIDTH_PX

        if n % tab_columns == 0:
            x = CONSOLE_FONT_WIDTH_PX
            y += (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * 2


    # for n, row in enumerate(player.get_stats_names(), 1):
    #     x = 0 - CONSOLE_FONT_WIDTH_PX
    #     for i, item in enumerate(row, 1):
    #         if not str(player.get_value(item)):
    #             text = ""
    #         else:
    #             if item == "HP":
    #                 value = str(player.get_value("HP")) + "/" + str(player.get_value("HP_MAX"))
    #             else:
    #                 value = str(player.get_value(item))
    #             value += " "
    #             text = f"{value + item:>{tab_column_width_chars}}"
    #
    #         if i == 2:
    #             x += CONSOLE_FONT_WIDTH_PX
    #
    #         draw_text(text, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * n * 2, x)
    #         x += tab_column_width_chars * CONSOLE_FONT_WIDTH_PX


def main():
    pygame.display.set_caption("the quest - technological demo, since 04.2021")

    card1 = Card("Ambient card", condition="card ability text line one", bounty="VP", image="cultGreen.png")
    card2 = Card("Event card test", image="img_02.jpg", condition="card ability text line one")
    card3 = Card("Enemy card test", type="enemy", base_power=5, image="img_03.jpg",
                 condition="card ability text line one", bounty="VP, COMMAND")
    player = Player("Necron Lord")

    actual_action = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    game_over = True

                if event.key == pygame.K_DOWN:
                    actual_action += 1
                    if actual_action > 4:
                        actual_action = 0

                if event.key == pygame.K_UP:
                    actual_action -= 1
                    if actual_action < 0:
                        actual_action = 4

                if event.key == pygame.K_1 or event.key == pygame.K_KP1:  # NUM 1
                    actual_action = 0

                if event.key == pygame.K_2 or event.key == pygame.K_KP2:  # NUM 2
                    actual_action = 1

                SCREEN.fill((0, 0, 0))
                draw_card(card3)
                # draw_cursor(player, actual_action, [1, 2, 3, 4, 5, 6])
                # draw_console(player)
                draw_player_stats(player)
                draw_text("add 2 to your combat bonus", SCREEN_HEIGHT_PX - (FONT_SIZE_PX + LINE_SPACING_PX) * 2,
                          color=WHITE, center=True)
                draw_text("second line of text", SCREEN_HEIGHT_PX - (FONT_SIZE_PX + LINE_SPACING_PX), color=WHITE,
                          center=True)

            # zaviraci ikona okna X
            if event.type == pygame.QUIT:
                game_over = True

        pygame.display.flip()
        # pygame.display.update()
        # clock.tick(60)


if __name__ == "__main__":
    main()
