import pygame
import pygame_menu
import pygame

from typing import Tuple, Any

background = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
title_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
bg = pygame.image.load('Galaga Picture/Galaga_Background.gif')
pygame.display.set_caption("Galaga")
player = pygame.image.load('Galaga Picture/Galaga_Ship2.png')
player = pygame.transform.scale(player, (250, 150))
title = pygame.image.load('Galaga Picture/Galaga_Logo.png')
dist = 3
cheatcode = []
surface2 = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.init()
pygame.font.init()

score_value = 0
score_multiplier = 1
lives = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_X = 10
score_Y = 10
lives_X = -10
lives_Y = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    background.blit(score, (x, y))


def show_lives(x, y):
    life = font.render("Lives: " + str(lives), True, (255, 255, 255))
    background.blit(life, (x, y))


class Ship(object):
    def __init__(self):
        self.image = player
        self.x = 0
        self.y = 0

    def keyboard_arrows(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.y += dist
        elif key[pygame.K_UP]:
            self.y -= dist
        if key[pygame.K_RIGHT]:
            self.x += dist
        elif key[pygame.K_LEFT]:
            self.x -= dist

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def keyboard_wasd(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_s]:
            self.y += dist
        elif key[pygame.K_w]:
            self.y -= dist
        if key[pygame.K_d]:
            self.x += dist
        elif key[pygame.K_a]:
            self.x -= dist

    def shoot(self):
        global score_value
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            score_value = score_value + 1
            print(score_value)
            print(score_multiplier)


class Cheats(object):
    def Superspeed(self):
        global dist
        key = pygame.key.get_pressed()
        if key[pygame.K_p]:
            if key[pygame.K_LSHIFT]:
                dist = dist + 3

    def SlowDown(self):
        global dist
        key = pygame.key.get_pressed()
        if key[pygame.K_l]:
            if key[pygame.K_LSHIFT]:
                dist = dist - 3

    def ScoreMultiplier(self):
        global score_value
        global score_multiplier
        key = pygame.key.get_pressed()
        if key[pygame.K_m]:
            if key[pygame.K_LSHIFT]:
                score_multiplier = score_multiplier + 1
                score_value = score_value * score_multiplier

    def DoubleShip(self):
        print()  # This will be done later, the print statement is simply to avoid the error for now.

    def RapidFire(self):
        print()  # This will be done later, the print statement is simply to avoid the error for now.

    def InfiniteLives(self):
        global lives
        key = pygame.key.get_pressed()
        if key[pygame.K_i]:
            if key[pygame.K_LSHIFT]:
                lives = lives + 1


ship = Ship()
cheats = Cheats()


def start():
    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            background.blit(bg, (0, 0))
            ship.keyboard_arrows()
            ship.keyboard_wasd()
            ship.shoot()
            Konami()

            show_score(score_X, score_Y)
            show_lives(lives_X, lives_Y)
            ship.draw(background)
            pygame.display.update()

            clock.tick(40)


surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def set_difficulty(selected: Tuple, value: Any):
    global lives
    print('Set difficulty to {} ({})'.format(selected[0], value))
    if value == 1:
        lives = 10
    elif value == 2:
        lives = 5
    elif value == 3:
        lives = 3
    elif value == 4:
        lives = 1


def start_the_game():
    start()
    global user_name


def Konami():
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        if key[pygame.K_LSHIFT]:
            cheatcode.append("↑")
            print(cheatcode)
    elif key[pygame.K_DOWN]:
        if key[pygame.K_LSHIFT]:
            cheatcode.append("↓")
            print(cheatcode)
    if key[pygame.K_RIGHT]:
        if key[pygame.K_LSHIFT]:
            cheatcode.append("→")
            print(cheatcode)
    elif key[pygame.K_LEFT]:
        if key[pygame.K_LSHIFT]:
            cheatcode.append("←")
            print(cheatcode)
    if key[pygame.K_a]:
        if key[pygame.K_LSHIFT]:
            cheatcode.append("A")
            print(cheatcode)
    elif key[pygame.K_b]:
        if key[pygame.K_LSHIFT]:
            cheatcode.append("B")
            print(cheatcode)
    if key[pygame.K_c]:
        if key[pygame.K_LSHIFT]:
            cheatcode.clear()
            print(cheatcode)
    if cheatcode == ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'B', 'A', 'A']:
        # Yes I know the Konami code only has one B and one A but when the user presses A or B it automatically puts two
        def toggle_cheat(selected: Tuple, value: Any):
            print('Set cheats to {} ({})'.format(selected[0], value))
            if value == 1:
                Cheats.Superspeed(cheats)
                print("Super speed enabled.")
            elif value == 2:
                print("Super speed disabled")
            elif value == 3:
                Cheats.InfiniteLives(cheats)
                print("Infinite lives enabled.")
            elif value == 4:
                print("Infinite Lives disabled")
            elif value == 5:
                Cheats.ScoreMultiplier(cheats)
                print("Score multiplier enabled.")
            elif value == 6:
                print("Score multiplier disabled")
            elif value == 7:
                Cheats.SlowDown(cheats)
                print("Slow down enabled.")
            elif value == 8:
                print("Slow down disabled")
            elif value == 9:
                Cheats.DoubleShip(cheats)
                print("Double ship enabled.")
            elif value == 10:
                print("Double ship disabled")
            elif value == 11:
                Cheats.RapidFire(cheats)
                print("Rapid fire enabled.")
            elif value == 12:
                print("Rapid fire disabled")

        cheat_menu = pygame_menu.Menu(
            height=700,
            theme=pygame_menu.themes.THEME_DARK,
            title='Cheats',
            width=800
        )
        cheat_menu.add.button('Resume', pygame_menu.events.BACK)
        cheat_menu.add.selector('Super Speed (LSHIFT + P): ', [('False', 2), ('True', 1)], onchange=toggle_cheat)
        cheat_menu.add.selector('Infinite Lives (LSHIFT + I): ', [('False', 4), ('True', 3)], onchange=toggle_cheat)
        cheat_menu.add.selector('Score Multiplier (LSHIFT + M): ', [('False', 6), ('True', 5)], onchange=toggle_cheat)
        cheat_menu.add.selector('Slow Speed (LSHIFT + L): ', [('False', 8), ('True', 7)], onchange=toggle_cheat)
        cheat_menu.add.selector('Double ship (LSHIFT + N): ', [('False', 10), ('True', 9)], onchange=toggle_cheat)
        cheat_menu.add.selector('Rapid fire (LSHIFT + R): ', [('False', 12), ('True', 11)], onchange=toggle_cheat)


menu = pygame_menu.Menu(
    height=400,
    theme=pygame_menu.themes.THEME_DARK,
    title='Galaga',
    width=600
)
menu.add.button('Play', start_the_game)
user_name = menu.add.text_input('Name: ', default='', maxchar=10)
menu.add.selector('Difficulty: ', [('Easy', 1), ('Medium', 2), ('Hard', 3), ('Tournament', 4)], onchange=set_difficulty)

menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)
