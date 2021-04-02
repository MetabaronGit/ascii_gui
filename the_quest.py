import pygame

SCREEN_WIDTH = 792  # cislo je delitelne sirkou fontu
SCREEN_HEIGHT = 600
FONT_SIZE = 18
LINE_SPACE = FONT_SIZE // 2


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
    def __init__(self, name:str, condition=""):
        self.__name = name
        self.__condition = condition
        self.__actions = ["take MUNITION", "enlarge COMBAT", "pray for Omnisiah", "SCORE"]

    def get_name(self):
        return self.__name

    def get_condition(self):
        return self.__condition


card1 = Card("Forge supply depot", "Mechanic heroes have doubled all effects here.")
card2 = Card("Mechanicum sanctuary", "All Mechanicum heroes increase MAX HP by 2.")
player = Player("Jurgen XVII", 20, 0, 0, 0, 0)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("the quest - technological demo, 04.2021")


console_font = pygame.font.Font('lucon.ttf', FONT_SIZE)
TEXT_COLOR = (0, 200, 0)
white = (255, 255, 255)
CURSOR_COLOR = (0, 100, 0)

CONSOLE_FONT_WIDTH, CONSOLE_FONT_HEIGHT = console_font.size("-")

actual_action = 0


def draw_image(y):
    # draw_text("Forge supply depot", y)
    draw_text(card1.get_name(), y)
    testImg = pygame.image.load('images/cultGreen.png')
    # obrazek vycentrovany na ose x
    screen.blit(testImg, (SCREEN_WIDTH // 2 - testImg.get_width() // 2, y + CONSOLE_FONT_HEIGHT + LINE_SPACE))
    draw_text(card1.get_condition(), y + CONSOLE_FONT_HEIGHT + LINE_SPACE * 2 + testImg.get_height())


def draw_text(text_string, y, color=TEXT_COLOR, background_color=None, center=True):
    text = console_font.render(text_string, True, color, background_color)
    text_rect = text.get_rect()
    text_rect.y = y
    if center:
        text_rect.x = SCREEN_WIDTH // 2 - (len(text_string) * CONSOLE_FONT_WIDTH) // 2
    else:
        text_rect.x = 0
    screen.blit(text, text_rect)


def draw_cursor(y):
    draw_text(" " * (SCREEN_WIDTH // CONSOLE_FONT_WIDTH), y + (actual_action + 1) * (CONSOLE_FONT_HEIGHT + LINE_SPACE), background_color=CURSOR_COLOR)

def draw_console(y):
    options = ["take MUNITION", "enlarge COMBAT", "pray for Omnisiah", "SCORE", "None"]
    draw_text("-" * (SCREEN_WIDTH // CONSOLE_FONT_WIDTH), y)
    for i, item in enumerate(options, 1):
        draw_text(f" [{i}] {item}", y + (CONSOLE_FONT_HEIGHT + LINE_SPACE) * i, center=False)


def draw_player_values(y):
    hp = 20
    max_hp = 20
    combat = 0
    munition = 0
    command = 0
    credits = 0
    max_deck = 30
    deck = 30

    separator = f"{'':-<15}+{'':->12}+{'':->14}+{'':->13}+{'':->16}"
    draw_text(separator, y)

    text = f"{hp:>3}/{max_hp:<3} HP | {combat:>3} COMBAT | {munition:>3} MUNITION | {command:>3} COMMAND | {credits:>6} CR  "
    draw_text(text, y + CONSOLE_FONT_HEIGHT * 1)

    # draw_text("-" * (SCREEN_WIDTH // CONSOLE_FONT_WIDTH), y + CONSOLE_FONT_HEIGHT * 2)
    draw_text(separator, y + CONSOLE_FONT_HEIGHT * 2)

    text = f"  {' ':10} | {' inventory':10} | {' ':12} | {' ':11} | {deck:>3}/{max_deck:<} DECK  "
    draw_text(text, y + CONSOLE_FONT_HEIGHT * 3)

    draw_text(separator, y + CONSOLE_FONT_HEIGHT * 4)

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
            draw_player_values(480)
            draw_text("add 2 to your combat bonus", 600 - FONT_SIZE - CONSOLE_FONT_HEIGHT // 2, color=white)

        # zaviraci ikona okna X
        if event.type == pygame.QUIT:
            game_over = True

    pygame.display.flip()
    # pygame.display.update()
    # clock.tick(60)
