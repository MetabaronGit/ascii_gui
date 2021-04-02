import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 18

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("the quest technological demo")


console_font = pygame.font.Font('lucon.ttf', FONT_SIZE)
text_color = (0, 200, 0)
background_text_color = (0, 0, 0)

CONSOLE_FONT_WIDTH, CONSOLE_FONT_HEIGHT = console_font.size("-")


def draw_image(y):
    draw_text("Forge supply depot", y)
    testImg = pygame.image.load('images/cultGreen.png')
    # obrazek vycentrovany na ose x
    screen.blit(testImg, (SCREEN_WIDTH // 2 - testImg.get_width() // 2, y + CONSOLE_FONT_HEIGHT))
    draw_text("Mechanic heroes have doubled all effects here.", y + CONSOLE_FONT_HEIGHT * 2 + testImg.get_height())


def draw_text(text, y, center=True):
    text = console_font.render(text, True, text_color, background_text_color)
    textRect = text.get_rect()
    if center:
        textRect.center = (SCREEN_WIDTH // 2, y)
    else:
        textRect.y = y
    screen.blit(text, textRect)


def draw_console(y):
    options = ["take MUNITION", "enlarge COMBAT", "pray for Omnisiah", "SCORE"]
    draw_text("-" * (SCREEN_WIDTH // CONSOLE_FONT_WIDTH), y)
    for i, item in enumerate(options, 1):
        draw_text(f" [{i}] {item}", y + CONSOLE_FONT_HEIGHT * i, center=False)


def draw_player_values(y):
    hp = 8
    max_hp = 10
    draw_text(f" {hp}/{max_hp} HP", y + CONSOLE_FONT_HEIGHT * 1, center=False)


game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            if event.key == pygame.K_SPACE:
                draw_image(40)
            if event.key == pygame.K_RETURN:
                draw_console(300)
                draw_player_values(400)

        # zaviraci ikona okna X
        if event.type == pygame.QUIT:
            game_over = True

    pygame.display.flip()
    # pygame.display.update()
    # clock.tick(60)
