import pygame
import pygame_menu
import random

from pygame_menu import Theme

# All my variables and resizing of images or lowering sound volume
background = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
title_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
bg = pygame.image.load('Galaga Picture/Galaga_Background.gif')
pygame.display.set_caption("Galaga")
player = pygame.image.load('Galaga Picture/Galaga_Ship2.png')
player = pygame.transform.scale(player, (125, 75))
player2 = pygame.image.load('Galaga Picture/imageedit_11_7860503718.png')
player2 = pygame.transform.scale(player2, (135, 110))
title = pygame.image.load('Galaga Picture/Galaga_Logo.png')
alienImg = pygame.image.load('img/alien3.png')

clock = pygame.time.Clock()
fps = 60
screen_width = 1400
screen_height = 900

red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

cheatcode = []
killcode = []
surface2 = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# define game variables
rows = 5
cols = 10
alien_cooldown = 100  # bullet cooldown in milliseconds
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0  # 0 is no game over, 1 means player has won, -1 means player has lost

sw = 800
sh = 800

pygame.init()
pygame.font.init()

dist = 3
score_value = 0
score_multiplier = 1
lives = 3
kill_number = 0
cooldown = 500

explosion_fx = pygame.mixer.Sound("img/explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25)

laser_fx2 = pygame.mixer.Sound("img/laser.wav")
laser_fx2.set_volume(0.05)

font = pygame.font.Font('freesansbold.ttf', 15)
font2 = pygame.font.Font('freesansbold.ttf', 40)

# My menu themes and images used in my menus
# I replaced the preset pygame images with mine
cheat_font = pygame_menu.font.FONT_MUNRO
space = pygame_menu.baseimage.BaseImage(
    image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_WALLPAPER,
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

title_image = pygame_menu.baseimage.BaseImage(
    image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_METAL,
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

paused = pygame_menu.baseimage.BaseImage(
    image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

gameover = pygame_menu.baseimage.BaseImage(
    image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU,
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

winner = pygame_menu.baseimage.BaseImage(
    image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER,
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

mytheme = Theme(background_color=(0, 0, 0, 0),
                # Yes, I understand that my theme causes an error but it gives the retro look I want and it still runs
                title_background_color=(0, 0, 0),
                title_font_color=(0, 0, 0),
                title_font_shadow=True,
                widget_padding=25,
                widget_font_color=(255, 0, 0),
                widget_font=cheat_font)

mytheme2 = Theme(background_color=space,
                 # Yes, I understand that my theme causes an error but it gives the retro look I want and it still runs
                 title_background_color=(0, 0, 0),
                 title_font_color=(0, 0, 0),
                 title_font_shadow=True,
                 widget_padding=25,
                 widget_font_color=(255, 255, 255),
                 widget_font=cheat_font)


# The function to update the display after a score is gained or lives are gained
def redrawGameWindow():
    global livesText
    global scoreText
    global killText
    background.blit(bg, (0, 0))
    livesText = font.render('HP: ' + str(lives), True, (255, 255, 255))
    scoreText = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    killText = font.render('Kills: ' + str(kill_number), True, (255, 255, 255))


def draw_bg():
    screen.blit(bg, (0, 0))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# My ship class that controls my ships movement, position, and creation.
class Spaceship(pygame.sprite.Sprite):
    global dist

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        global cooldown
        global lives
        game_over = 0

        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= dist
        if key[pygame.K_RIGHT]:
            self.rect.x += dist

        # record current time
        time_now = pygame.time.get_ticks()
        # shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # update mask
        self.mask = pygame.mask.from_surface(self.image)

        if lives <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over

    def WrapAround(self):
        if self.rect.x == -138:
            self.rect.x = 1478
        elif self.rect.x == 1478:
            self.rect.x = -138

    def rapid(self):
        global cooldown
        cooldown = 0

    def reset(self):
        self.rect.x = 632


# My class to control the bullets of my ship
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Galaga Picture/blast-harrier-laser-1.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


# create Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Galaga Picture/imageedit_16_8043674755.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False):
            self.kill()
            # reduce spaceship health
            global lives
            lives = lives - 1
            explosion2_fx.play()
            redrawGameWindow()


# create Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
            global kill_number
            global score_value
            score_value = score_value + random.randint(1, 10)
            kill_number = kill_number + 1
            redrawGameWindow()


# create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_aliens():
    # generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)


create_aliens()


def more():
    key = pygame.key.get_pressed()
    if key[pygame.K_8]:
        create_aliens()


# create player


spaceship = Spaceship(int(screen_width / 2), screen_height - 100)
spaceship_group.add(spaceship)


# My class of cheats, each cheat has its own menu and set of keys to activate
class Cheats(object):
    global dist

    def Superspeed(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_k]:
            if key[pygame.K_LSHIFT]:
                global dist
                dist = dist + 2
            if key[pygame.K_RSHIFT]:
                cheat_menu = pygame_menu.Menu(
                    height=900,
                    theme=mytheme,
                    title='Cheats',
                    width=1400
                )
                cheat_menu.add.label('You have entered the Speed Up cheatcode.')
                cheat_menu.add.button('Click to resume', start)
                cheat_menu.add.label('You will increase your speed by 2 every time you press: ')
                cheat_menu.add.label('LSHIFT + K')
                cheat_menu.add.label('To decrease your speed by 2 press: ')
                cheat_menu.add.label('LSHIFT + L')
                cheat_menu.add.label('Your starting speed is 3.')

                if __name__ == '__main__':
                    cheat_menu.mainloop(surface2)

    def SlowDown(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_l]:
            if key[pygame.K_LSHIFT]:
                global dist
                dist = dist - 2
            if key[pygame.K_RSHIFT]:
                cheat_menu = pygame_menu.Menu(
                    height=900,
                    theme=mytheme,
                    title='Cheats',
                    width=1400
                )
                cheat_menu.add.label('You have entered the Slow Down cheatcode.')
                cheat_menu.add.button('Click to resume', start)
                cheat_menu.add.label('You will decrease your speed by 2 every time you press: ')
                cheat_menu.add.label('LSHIFT + L')
                cheat_menu.add.label('To increase your speed by 2 press: ')
                cheat_menu.add.label('LSHIFT + K')
                cheat_menu.add.label('Your starting speed is 3.')

                if __name__ == '__main__':
                    cheat_menu.mainloop(surface2)

    def RapidFire(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            if key[pygame.K_LSHIFT]:
                spaceship.rapid()
            if key[pygame.K_RSHIFT]:
                cheat_menu = pygame_menu.Menu(
                    height=900,
                    theme=mytheme,
                    title='Cheats',
                    width=1400
                )
                cheat_menu.add.label('You have entered the Rapid Fire cheatcode.')
                cheat_menu.add.button('Click to resume', start)
                cheat_menu.add.label('You will increase your shooting speed by 1 every time you press: ')
                cheat_menu.add.label('LSHIFT + R')

                if __name__ == '__main__':
                    cheat_menu.mainloop(surface2)

    def InfiniteLives(self):
        global lives
        global livesText
        key = pygame.key.get_pressed()
        if key[pygame.K_i]:
            if key[pygame.K_LSHIFT]:
                lives = lives + 1
                redrawGameWindow()
            if key[pygame.K_RSHIFT]:
                cheat_menu = pygame_menu.Menu(
                    height=900,
                    theme=mytheme,
                    title='Cheats',
                    width=1400
                )
                cheat_menu.add.label('You have entered the Infinite Lives cheatcode.')
                cheat_menu.add.button('Click to resume', start)
                cheat_menu.add.label('You will increase your life count by 1 for every second you press: ')
                cheat_menu.add.label('LSHIFT + I')

                if __name__ == '__main__':
                    cheat_menu.mainloop(surface2)

    def all(self):
        Cheats.Superspeed(cheats)
        Cheats.SlowDown(cheats)
        Cheats.RapidFire(cheats)
        Cheats.InfiniteLives(cheats)


cheats = Cheats()


# My other functions that do what they are titled, I have multiple of the same function due to different menus needing the same information.

def toggle_cheat():
    cheat_menu = pygame_menu.Menu(
        height=900,
        theme=mytheme,
        title='Cheats',
        width=1400
    )
    cheat_menu.add.label('Cheats have been enabled.')
    cheat_menu.add.label('You can use these cheats by clicking: ')
    cheat_menu.add.label('Super Speed (LSHIFT + P)')
    cheat_menu.add.label('Infinite Lives (LSHIFT + I)')
    cheat_menu.add.label('Score Multiplier (LSHIFT + M)')
    cheat_menu.add.label('Slow Speed (LSHIFT + L)')
    cheat_menu.add.label('Double ship (LSHIFT + T)')
    cheat_menu.add.label('Rapid fire (LSHIFT + R)')
    cheat_menu.add.button('Click to resume', start)
    cheat_menu.add.button('Click to disable cheats', cheater)

    if __name__ == '__main__':
        cheat_menu.mainloop(surface2)


def cheater():
    cheat_menu = pygame_menu.Menu(
        height=900,
        theme=mytheme,
        title='Cheats',
        width=1400
    )
    cheat_menu.add.label('You have entered the Konami code and unlocked cheats.')
    cheat_menu.add.button('Click to resume', start)
    cheat_menu.add.button('Click to enable cheats', toggle_cheat)
    cheat_menu.add.label('The cheats are: ')
    cheat_menu.add.label('Super Speed')
    cheat_menu.add.label('Infinite Lives')
    cheat_menu.add.label('Score Multiplier')
    cheat_menu.add.label('Slow Speed')
    cheat_menu.add.label('Double ship ')
    cheat_menu.add.label('Rapid fire')

    if __name__ == '__main__':
        cheat_menu.mainloop(surface2)


def Konami():
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and key[pygame.K_LSHIFT]:
        Up = ["↑"]
        cheatcode.extend(Up)
        print(cheatcode)
    if key[pygame.K_DOWN] and key[pygame.K_LSHIFT]:
        Down = ["↓"]
        cheatcode.extend(Down)
        print(cheatcode)
    if key[pygame.K_RIGHT] and key[pygame.K_LSHIFT]:
        Right = ["→"]
        cheatcode.extend(Right)
        print(cheatcode)
    if key[pygame.K_LEFT] and key[pygame.K_LSHIFT]:
        Left = ["←"]
        cheatcode.extend(Left)
        print(cheatcode)
    if key[pygame.K_a] and key[pygame.K_LSHIFT]:
        A = ['A']
        cheatcode.extend(A)
        print(cheatcode)
    if key[pygame.K_b] and key[pygame.K_LSHIFT]:
        B = ['B']
        cheatcode.extend(B)
        print(cheatcode)
    if key[pygame.K_BACKSPACE] and key[pygame.K_LSHIFT]:
        cheatcode.clear()
        print(cheatcode)
    if key[pygame.K_RETURN] and key[pygame.K_LSHIFT]:
        cheatcode.clear()
        print(cheatcode)
        cheating = ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'A']
        cheatcode.extend(cheating)
        print(cheatcode)
    if cheatcode == ['↑', '↑', '↓', '↓', '←', '→', '←', '→', 'B', 'A']:
        # Yes I know the Konami code only has one B and one A but when the user presses A or B it automatically puts two
        cheater()


def kill():
    global lives
    key = pygame.key.get_pressed()
    if key[pygame.K_0]:
        lives = 0


def End():
    if lives == 0:
        end = pygame_menu.Menu(
            height=900,
            theme=mytheme2,
            title='Game Over',
            width=1400
        )
        end.add.image(gameover)
        end.add.button('Play again', main_menu2)
        end.add.label('Your score was: ')
        end.add.label(score_value)
        end.add.label('Your kill count was: ')
        end.add.label(kill_number)
        end.add.button('Click to quit', pygame_menu.events.EXIT)

        if __name__ == '__main__':
            end.mainloop(surface)


def Win():
    win = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Winner',
        width=1400
    )
    win.add.image(winner)
    win.add.button('Play again', main_menu2)
    win.add.label('Your score was: ')
    win.add.label(score_value)
    win.add.label('Your kill count was: ')
    win.add.label(kill_number)
    win.add.button('Click to quit', pygame_menu.events.EXIT)

    if __name__ == '__main__':
        win.mainloop(surface)


def pause():
    key = pygame.key.get_pressed()
    if key[pygame.K_p]:
        pause_menu = pygame_menu.Menu(
            height=900,
            theme=mytheme2,
            title='Galaga',
            width=1400
        )
        pause_menu.add.image(paused)
        pause_menu.add.button('Resume', start)
        pause_menu.add.button('New Game', main_menu2)
        pause_menu.add.button('Controls', pause_controls)
        pause_menu.add.button('Rules', pause_rules)
        pause_menu.add.button('Quit', pygame_menu.events.EXIT)

        if __name__ == '__main__':
            pause_menu.mainloop(surface)


def pause2():
    pause_menu = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Galaga',
        width=1400
    )
    pause_menu.add.image(paused)
    pause_menu.add.button('Resume', start)
    pause_menu.add.button('New Game', main_menu2)
    pause_menu.add.button('Controls', pause_controls)
    pause_menu.add.button('Rules', pause_rules)
    pause_menu.add.button('Quit', pygame_menu.events.EXIT)

    if __name__ == '__main__':
        pause_menu.mainloop(surface)


livesText = font.render('HP: ' + str(lives), True, (255, 255, 255))
scoreText = font.render('Score: ' + str(score_value), True, (255, 255, 255))
killText = font.render('Kills: ' + str(kill_number), True, (255, 255, 255))


def controls():
    control_menu = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Galaga',
        width=1400
    )
    control_menu.add.image(title_image)
    control_menu.add.label('RSHIFT is for commands.')
    control_menu.add.label('LEFT is to move your ship LEFT.')
    control_menu.add.label('RIGHT is to move your ship RIGHT.')
    control_menu.add.label('P is to open the pause menu.')
    control_menu.add.label('0 is to end the game immediately.')
    control_menu.add.label('8 is to summon another group of enemies.')
    control_menu.add.button('Back', main_menu)

    if __name__ == '__main__':
        control_menu.mainloop(surface)


def rules():
    rule_menu = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Galaga',
        width=1400
    )
    rule_menu.add.image(title_image)
    rule_menu.add.label('You will have 3 lives.')
    rule_menu.add.label('There will be ____ levels for you to complete.')
    rule_menu.add.label('You will lose a life if enemy fire hits you.')
    rule_menu.add.label('You will gain points by hitting enemies with your fire.')
    rule_menu.add.label('There are a few hidden secrets for you to find.')
    rule_menu.add.button('Back', main_menu)

    if __name__ == '__main__':
        rule_menu.mainloop(surface)


def pause_controls():
    control3_menu = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Galaga',
        width=1400
    )
    control3_menu.add.image(title_image)
    control3_menu.add.label('LSHIFT is for commands.')
    control3_menu.add.label('W or UP is to move your ship up.')
    control3_menu.add.label('S or DOWN is to move your ship down.')
    control3_menu.add.label('A or LEFT is to move your ship LEFT.')
    control3_menu.add.label('D or RIGHT is to move your ship RIGHT.')
    control3_menu.add.label('P is to open the pause menu.')
    control3_menu.add.label('0 is to end the game immediately.')
    control3_menu.add.button('Back', pause2)

    if __name__ == '__main__':
        control3_menu.mainloop(surface)


def pause_rules():
    rule3_menu = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Galaga',
        width=1400
    )
    rule3_menu.add.image(title_image)
    rule3_menu.add.label('You will have 3 lives.')
    rule3_menu.add.label('There will be ____ levels for you to complete.')
    rule3_menu.add.label('You will lose a life if enemy fire hits you.')
    rule3_menu.add.label('You will gain points by hitting enemies with your fire.')
    rule3_menu.add.label('There are a few hidden secrets for you to find.')
    rule3_menu.add.button('Back', pause2)

    if __name__ == '__main__':
        rule3_menu.mainloop(surface)


def controls2():
    control2_menu = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Galaga',
        width=1400
    )
    control2_menu.add.image(title_image)
    control2_menu.add.label('RSHIFT is for commands.')
    control2_menu.add.label('A or LEFT is to move your ship LEFT.')
    control2_menu.add.label('D or RIGHT is to move your ship RIGHT.')
    control2_menu.add.label('P is to open the pause menu.')
    control2_menu.add.label('0 is to end the game immediately.')
    control2_menu.add.label('8 is to summon another group of enemies.')
    control2_menu.add.button('Back', main_menu2)

    if __name__ == '__main__':
        control2_menu.mainloop(surface)


def rules2():
    rule2_menu = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Galaga',
        width=1400
    )
    rule2_menu.add.image(title_image)
    rule2_menu.add.label('You will have 3 lives.')
    rule2_menu.add.label('There will be ____ levels for you to complete.')
    rule2_menu.add.label('You will lose a life if enemy fire hits you.')
    rule2_menu.add.label('You will gain points by hitting enemies with your fire.')
    rule2_menu.add.label('There are a few hidden secrets for you to find.')
    rule2_menu.add.button('Back', main_menu2)

    if __name__ == '__main__':
        rule2_menu.mainloop(surface)


pygame.init()

surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


# The main function to start the game


def start():
    global countdown
    global last_alien_shot
    global game_over
    global last_count
    global lives
    run = True
    while run:

        clock.tick(fps)

        draw_bg()
        spaceship.WrapAround()
        pause()
        kill()
        Cheats.all(cheats)
        more()
        background.blit(killText, (sw - killText.get_width() - 25, 0))
        background.blit(livesText, (25, 0))
        background.blit(scoreText, (sw - scoreText.get_width() + 600, 0))

        if countdown == 0:
            # create random alien bullets
            # record current time
            time_now = pygame.time.get_ticks()
            # shoot
            if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 10 and len(alien_group) > 0:
                attacking_alien = random.choice(alien_group.sprites())
                alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
                alien_bullet_group.add(alien_bullet)
                laser_fx2.play()
                last_alien_shot = time_now

            # check if all the aliens have been killed
            if len(alien_group) == 0:
                game_over = 1

            if game_over == 0:
                # update spaceship
                game_over = spaceship.update()

                # update sprite groups
                bullet_group.update()
                alien_group.update()
                alien_bullet_group.update()
            else:
                if game_over == -1:
                    lives = 0
                    End()
                if game_over == 1:
                    Win()

        if countdown > 0:
            draw_text('GET READY!', font2, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
            draw_text(str(countdown), font2, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer

        # update explosion group
        explosion_group.update()

        # draw sprite groups
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)

        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


def restart():
    global score_value
    global score_multiplier
    global lives
    global kill_number
    lives = 3
    score_value = 0
    score_multiplier = 1
    kill_number = -1
    global countdown
    global last_alien_shot
    global game_over
    global last_count
    countdown = 3
    game_over = 0
    spaceship.reset()
    spaceship_group.add(spaceship)
    alien_group.empty()
    create_aliens()
    run = True
    while run:

        clock.tick(fps)

        draw_bg()
        spaceship.WrapAround()
        pause()
        kill()
        Cheats.all(cheats)
        more()
        background.blit(killText, (sw - killText.get_width() - 25, 0))
        background.blit(livesText, (25, 0))
        background.blit(scoreText, (sw - scoreText.get_width() + 600, 0))

        if countdown == 0:
            # create random alien bullets
            # record current time
            time_now = pygame.time.get_ticks()
            # shoot
            if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 10 and len(alien_group) > 0:
                attacking_alien = random.choice(alien_group.sprites())
                alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
                alien_bullet_group.add(alien_bullet)
                last_alien_shot = time_now

            # check if all the aliens have been killed
            if len(alien_group) == 0:
                game_over = 1

            if game_over == 0:
                # update spaceship
                game_over = spaceship.update()

                # update sprite groups
                bullet_group.update()
                alien_group.update()
                alien_bullet_group.update()
            else:
                if game_over == -1:
                    lives = 0
                    End()
                if game_over == 1:
                    Win()

        if countdown > 0:
            draw_text('GET READY!', font2, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
            draw_text(str(countdown), font2, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer

        # update explosion group
        explosion_group.update()

        # draw sprite groups
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        alien_group.draw(screen)
        alien_bullet_group.draw(screen)
        explosion_group.draw(screen)

        # event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


# The title screen menu upon launch of the program


def main_menu():
    menu = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Galaga',
        width=1400
    )
    menu.add.image(title_image)
    menu.add.label('Welcome Player One.')
    menu.add.button('Click to start', start)
    menu.add.button('Controls', controls)
    menu.add.button('Rules', rules)
    menu.add.button('Quit the game', pygame_menu.events.EXIT)

    if __name__ == '__main__':
        menu.mainloop(surface)


# The title screen upon a restart of the game


def main_menu2():
    menu2 = pygame_menu.Menu(
        height=900,
        theme=mytheme2,
        title='Galaga',
        width=1400
    )
    menu2.add.image(title_image)
    menu2.add.label('Welcome Player One.')
    menu2.add.button('Click to start', restart)
    menu2.add.button('Controls', controls2)
    menu2.add.button('Rules', rules2)
    menu2.add.button('Quit the game', pygame_menu.events.EXIT)

    if __name__ == '__main__':
        menu2.mainloop(surface)


# The function to call the main menu, which calls the start function when 'click to start' is clicked
main_menu()
