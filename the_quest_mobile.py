import pygame

SCREEN_WIDTH = 540  # cislo je delitelne sirkou fontu
SCREEN_HEIGHT = 780  # original=960
FONT_SIZE = 18
LINE_SPACING = 5


class Player:
    def __init__(self, name:str, max_hp, combat, munition, command, credits):
        self.__name = name
        self.__max_hp = max_hp
        self.__actual_hp = max_hp
        self.__combat = combat
        self.__munition = munition
        self.__command = command
        self.__credits = credits


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
player = Player("Jurgen XVII", 20, 0, 0, 0, 0)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("the quest - technological demo, 04.2021")


console_font = pygame.font.Font('lucon.ttf', FONT_SIZE)
TEXT_COLOR = (0, 200, 0)
white = (255, 255, 255)
dark_green = (0, 80, 0)
CURSOR_COLOR = (0, 100, 0)

CONSOLE_FONT_WIDTH, CONSOLE_FONT_HEIGHT = console_font.size("-")

actual_action = 0


def draw_image(y):
    y = y - card1.get_image_shift()
    # draw_text("Forge supply depot", y)
    draw_text(card1.get_name(), y)
    testImg = pygame.image.load(card1.get_image())
    # obrazek vycentrovany na ose x
    screen.blit(testImg, (SCREEN_WIDTH // 2 - testImg.get_width() // 2, y + CONSOLE_FONT_HEIGHT + LINE_SPACING))
    draw_text(card1.get_condition(), y + CONSOLE_FONT_HEIGHT + LINE_SPACING * 2 + testImg.get_height())


def draw_text(text_string, y, color=TEXT_COLOR, background_color=None, center=False):
    text = console_font.render(text_string, True, color, background_color)
    text_rect = text.get_rect()
    text_rect.y = y
    if center:
        text_rect.x = SCREEN_WIDTH // 2 - (len(text_string) * CONSOLE_FONT_WIDTH) // 2
    else:
        text_rect.x = 0
    screen.blit(text, text_rect)


def draw_cursor(y):
    draw_text(" " * (SCREEN_WIDTH // CONSOLE_FONT_WIDTH),
              y + (actual_action + 1) * (CONSOLE_FONT_HEIGHT + LINE_SPACING), background_color=CURSOR_COLOR)

def draw_console(y):
    options = ["take MUNITION", "enlarge COMBAT", "pray for Omnisiah", "SCORE", "None"]
    draw_text("-" * (SCREEN_WIDTH // CONSOLE_FONT_WIDTH), y)
    for i, item in enumerate(options, 1):
        draw_text(f" [{i}] {item}", y + (CONSOLE_FONT_HEIGHT + LINE_SPACING) * i, center=False)


def draw_player_values():
    hp = 123
    max_hp = 123
    combat = 12
    munition = 123
    command = 123
    psychic = 123
    credits = 123456
    corrupt = 12
    max_deck = 30
    deck = 30

    tab_lines = 4
    y = SCREEN_HEIGHT - (tab_lines * 2 + 4) * (CONSOLE_FONT_HEIGHT + LINE_SPACING)

    # draw empty stats tab
    text = "=< stats >" + "=" * (SCREEN_WIDTH // CONSOLE_FONT_WIDTH - 10)
    draw_text(text, y + (CONSOLE_FONT_HEIGHT + LINE_SPACING), color=dark_green)

    free_fields = f"{'':>16}|{'':>16}|{'':>16}"
    separator = f"{'':->16}+{'':->16}+{'':->16}"

    for i in range(2, tab_lines * 2 + 1, 2):
        draw_text(free_fields, y + (CONSOLE_FONT_HEIGHT + LINE_SPACING) * i, color=dark_green)
        if i == tab_lines * 2:
            separator = "=" * (SCREEN_WIDTH // CONSOLE_FONT_WIDTH)
        draw_text(separator, y + (CONSOLE_FONT_HEIGHT + LINE_SPACING) * (i + 1), color=dark_green)

    # draw stats values

    text = f"     {hp:>3}/{max_hp:<3} HP        {combat:>2} COMBAT    {munition:>3} MUNITION "
    draw_text(text, y + (CONSOLE_FONT_HEIGHT + LINE_SPACING) * 2)

    text = f"    {command:>3} COMMAND      {psychic:>3} PSYCHIC       {credits:>6} CR  "
    draw_text(text, y + (CONSOLE_FONT_HEIGHT + LINE_SPACING) * 4)

    text = f"    {corrupt:>3} CORRUPT      void shield"
    draw_text(text, y + (CONSOLE_FONT_HEIGHT + LINE_SPACING) * 6)

    text = f"      inventory                      {deck:>3}/{max_deck:<} DECK  "
    draw_text(text, y + (CONSOLE_FONT_HEIGHT + LINE_SPACING) * 8)


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
            draw_player_values()
            draw_text("add 2 to your combat bonus", SCREEN_HEIGHT - (FONT_SIZE + LINE_SPACING) * 2, color=white,
                      center=True)
            draw_text("second line of text", SCREEN_HEIGHT - (FONT_SIZE + LINE_SPACING), color=white,
                      center=True)

        # zaviraci ikona okna X
        if event.type == pygame.QUIT:
            game_over = True

    pygame.display.flip()
    # pygame.display.update()
    # clock.tick(60)