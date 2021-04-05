import pygame

SCREEN_WIDTH_PX = 540  # original=540
SCREEN_HEIGHT_PX = 780  # original=960
FONT_SIZE_PX = 18
LINE_SPACING_PX = 5


class Player:
    def __init__(self, name:str, hp_max, combat, munition, command, credits):
        self.__name = name
        self.__stats = {"HP": str(hp_max),
                        "HP_MAX": str(hp_max),
                        "COMBAT": str(combat),
                        "MUNITION": str(munition),
                        "COMMAND": str(command),
                        "CR": str(credits)}

    def get_value(self, key: str):
        if self.__stats.get(key):
            return self.__stats.get(key)
        else:
            return ""

class Card:
    def __init__(self, name:str, condition="", image="cultGreen", image_shift=0):
        self.__name = name
        self.__condition = condition
        self.__actions = ["take MUNITION", "enlarge COMBAT", "pray for Omnisiah", "SCORE"]
        self.__image = "images/" + image + ".png"
        self.__image_shift = image_shift

    def get_name(self):
        return self.__name

    def get_image(self):
        return self.__image

    def get_condition(self):
        return self.__condition

    def get_image_shift(self):
        return self.__image_shift


card1 = Card("Forge supply depot", condition="Mechanic heroes have doubled all effects here.", image="enemy03", image_shift=40)
card2 = Card("Mechanicum sanctuary", "All Mechanicum heroes increase MAX HP by 2.")
player = Player("Jurgen XVII", 20, 0, 0, 0, 10)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX))
pygame.display.set_caption("the quest - technological demo, 04.2021")


console_font = pygame.font.Font('lucon.ttf', FONT_SIZE_PX)
TEXT_COLOR = (0, 200, 0)
white = (255, 255, 255)
dark_green = (0, 80, 0)
CURSOR_COLOR = (0, 100, 0)

CONSOLE_FONT_WIDTH_PX, CONSOLE_FONT_HEIGHT_PX = console_font.size("-")

actual_action = 0


def draw_image(y):
    y = y - card1.get_image_shift()
    # draw_text("Forge supply depot", y)
    draw_text(card1.get_name(), y)
    testImg = pygame.image.load(card1.get_image())
    # obrazek vycentrovany na ose x
    screen.blit(testImg, (SCREEN_WIDTH_PX // 2 - testImg.get_width() // 2, y + CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX))
    draw_text(card1.get_condition(), y + CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX * 2 + testImg.get_height())


def draw_text(text_string, y, x=0, color=TEXT_COLOR, background_color=None, center=False):
    text = console_font.render(text_string, True, color, background_color)
    text_rect = text.get_rect()
    text_rect.y = y
    if center:
        text_rect.x = SCREEN_WIDTH_PX // 2 - (len(text_string) * CONSOLE_FONT_WIDTH_PX) // 2
    else:
        text_rect.x = x
    screen.blit(text, text_rect)


def draw_cursor(y):
    draw_text(" " * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX),
              y + (actual_action + 1) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX), background_color=CURSOR_COLOR)

def draw_console(y):
    options = ["take MUNITION", "enlarge COMBAT", "pray for Omnisiah", "SCORE", "None"]
    draw_text("-" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX), y)
    for i, item in enumerate(options, 1):
        draw_text(f" [{i}] {item}", y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * i, center=False)


def draw_player_stats(player):
    tab_columns = 3  # při změně šířky SCREEN_WIDTH se mění jen šířka sloupců
    tab_column_width_chars = SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX // tab_columns

    tab_lines = 4  # muzeme pridavat ci ubirat podle poctu zobrazovanych hodnot

    # umisteni se pocita od spodniho okraje SCREENu nad popisky vybranych akci
    y = SCREEN_HEIGHT_PX - (tab_lines * 2 + 4) * (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX)

    # draw empty stats tab
    text = "=< stats >" + "=" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX - 10)
    draw_text(text, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX), color=dark_green)

    free_fields = f"{'':>{tab_column_width_chars}}|{'':>{tab_column_width_chars}}|"
    separator = f"{'':->{tab_column_width_chars}}+{'':->{tab_column_width_chars}}+" + \
                "-" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX - tab_column_width_chars * 2 - 2)

    for i in range(2, tab_lines * 2 + 1, 2):
        draw_text(free_fields, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * i, color=dark_green)
        if i == tab_lines * 2:
            separator = "=" * (SCREEN_WIDTH_PX // CONSOLE_FONT_WIDTH_PX)
        draw_text(separator, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * (i + 1), color=dark_green)

    # draw stats values
    player_values = [["HP", "COMBAT", "MUNITION"],
                     ["COMMAND", "psychic", "CR"],
                     ["shield", "corrupt", ""],
                     ["inventory", "", "DECK"]]

    for n, row in enumerate(player_values, 1):
        x = 0 - CONSOLE_FONT_WIDTH_PX
        for i, item in enumerate(row, 1):
            if not str(player.get_value(item)):
                text = ""
            else:
                if item == "HP":
                    value = str(player.get_value("HP")) + "/" + str(player.get_value("HP_MAX"))
                else:
                    value = str(player.get_value(item))
                value += " "
                text = f"{value + item:>{tab_column_width_chars}}"

            if i == 2:
                x += CONSOLE_FONT_WIDTH_PX

            draw_text(text, y + (CONSOLE_FONT_HEIGHT_PX + LINE_SPACING_PX) * n * 2, x)
            x += tab_column_width_chars * CONSOLE_FONT_WIDTH_PX


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

            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                actual_action = 0

            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                actual_action = 1


            screen.fill((0, 0, 0))
            draw_image(50)
            draw_cursor(320)
            draw_console(320)
            draw_player_stats(player)
            draw_text("add 2 to your combat bonus", SCREEN_HEIGHT_PX - (FONT_SIZE_PX + LINE_SPACING_PX) * 2, color=white,
                      center=True)
            draw_text("second line of text", SCREEN_HEIGHT_PX - (FONT_SIZE_PX + LINE_SPACING_PX), color=white,
                      center=True)

        # zaviraci ikona okna X
        if event.type == pygame.QUIT:
            game_over = True

    pygame.display.flip()
    # pygame.display.update()
    # clock.tick(60)